# -*- coding: utf-8 -*-
"""把公开的 BOSS 直聘真实数据（SQL dump）解析成 pipeline 需要的 CSV。

数据来源：GitHub 仓库 Luxuryend/Boss 的 sqlfile/（jobs.sql / companies.sql / words.sql），
为已公开的脱敏岗位数据。运行后生成 data/raw/boss.csv，供 analysis/clean.py 清洗。

运行：python crawler/parse_boss_sql.py  <SQL目录>
"""
import os
import re
import ast
import sys
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_FILE = os.path.join(BASE_DIR, "data", "raw", "boss.csv")


def parse_inserts(path):
    """解析 MySQL INSERT dump（可含多行字符串），返回 DataFrame。"""
    text = open(path, encoding="utf-8").read()
    m = re.search(r"INSERT INTO `\w+` \((.*?)\) VALUES", text, re.DOTALL)
    cols = [c.strip("` ") for c in m.group(1).split(",")]

    rows = []
    i = 0
    while True:
        j = text.find("VALUES", i)
        if j == -1:
            break
        k = text.find("(", j)
        if k == -1:
            break
        # 引号感知的括号平衡扫描
        depth, in_str, esc, p = 0, False, False, k
        while p < len(text):
            c = text[p]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == "'":
                    if p + 1 < len(text) and text[p + 1] == "'":
                        p += 1  # 转义的单引号 ''
                    else:
                        in_str = False
            else:
                if c == "'":
                    in_str = True
                elif c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                    if depth == 0:
                        break
            p += 1
        tup = text[k:p + 1]
        try:
            rows.append(list(ast.literal_eval(tup)))
        except Exception as e:
            print(f"[warn] 解析失败跳过一条: {e}")
        i = p + 1
    return pd.DataFrame(rows, columns=cols)


def parse_salary(s):
    """'14-15K' / '14-28K·15薪' -> (low, high) 月薪 K；解析不出返回 (None, None)。"""
    s = str(s)
    m = re.search(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*[kK]", s)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r"(\d+(?:\.\d+)?)\s*[kK]", s)
    if m:
        return float(m.group(1)), float(m.group(1))
    return None, None


def main(sql_dir):
    jobs = parse_inserts(os.path.join(sql_dir, "jobs.sql"))
    comps = parse_inserts(os.path.join(sql_dir, "companies.sql"))
    words = parse_inserts(os.path.join(sql_dir, "words.sql"))
    print(f"jobs={len(jobs)}  companies={len(comps)}  words={len(words)}")

    # 公司表按 brandName 去重（同名公司只留第一条行业/规模信息）
    comps = comps.drop_duplicates(subset="brandName", keep="first")
    # 职位描述表按 id 去重并 rename
    words = words.rename(columns={"word": "description"})
    if "id" in words.columns:
        words = words[["id", "description"]].drop_duplicates(subset="id", keep="first")

    # join：公司行业/规模 + 职位描述
    df = jobs.merge(comps[["brandName", "brandIndustry", "brandScaleName"]],
                    on="brandName", how="left")
    if "id" in jobs.columns and "id" in words.columns:
        df = df.merge(words, on="id", how="left")

    # 薪资解析
    parsed = df["salaryDesc"].map(parse_salary)
    df["salary_low"] = parsed.map(lambda x: x[0])
    df["salary_high"] = parsed.map(lambda x: x[1])

    # 经验轻微预归一（1年以内 -> 1-3年，其余交给 clean.py 归一）
    df["jobExperience"] = df["jobExperience"].replace("1年以内", "1-3年")

    # 拼装 pipeline 字段
    desc = df["skills"].fillna("").astype(str) + " " + df["description"].fillna("").astype(str)
    out = pd.DataFrame({
        "job_name": df["jobName"],
        "company_name": df["brandName"],
        "salary_low": df["salary_low"],
        "salary_high": df["salary_high"],
        "location": df["areaDistrict"].fillna("").astype(str).replace("", "上海"),
        "experience": df["jobExperience"],
        "education": df["jobDegree"],
        "company_size": df["brandScaleName"],
        "industry": df["brandIndustry"],
        "description": desc,
    })

    # 丢弃薪资解析失败的行（无薪资无法进薪资图表）
    before = len(out)
    out = out.dropna(subset=["salary_low", "salary_high"]).reset_index(drop=True)
    print(f"薪资有效 {len(out)}/{before} 条")

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    out.to_csv(OUT_FILE, index=False, encoding="utf-8-sig")
    print(f"已写入 -> {OUT_FILE}")

    # 简要画像
    print("\n=== 岗位名 TOP 10 ===")
    print(out["job_name"].value_counts().head(10).to_string())
    print("\n=== 行业 TOP 8 ===")
    print(out["industry"].value_counts().head(8).to_string())
    print("\n=== 学历 / 经验 / 规模 ===")
    print(out["education"].value_counts().to_string())
    print(out["experience"].value_counts().to_string())
    print(out["company_size"].value_counts().to_string())


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else r"E:\projects\boss_data_tmp\sqlfile"
    main(src)
