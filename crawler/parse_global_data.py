# -*- coding: utf-8 -*-
"""把公开的全球数据岗位数据集（Kaggle 系）抽样清洗成 pipeline 需要的 CSV。

数据来源：GitHub 仓库 picklesueat/data_jobs_data 的 data/*.csv
（BusinessAnalyst / DataAnalyst / DataEngineer / DataScientist，共约 55 万条美国岗位）。
运行后生成 data/raw/global.csv，供 analysis/clean.py 清洗。

字段映射：
  Job Title -> job_name        Salary Estimate -> salary_low/high（年薪，千美元）
  Job Description -> description（截断，同时用于提取经验/学历）
  Company Name -> company_name  Location -> location  Size -> company_size
  Industry -> industry
"""
import os
import re
import random
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = r"E:\projects\datajobs_tmp\data"
OUT_FILE = os.path.join(BASE_DIR, "data", "raw", "global.csv")

FILES = ["BusinessAnalyst.csv", "DataAnalyst.csv", "DataEngineer.csv", "DataScientist.csv"]
PER_FILE = 1500          # 每个岗位类型抽样条数
DESC_MAX = 500           # 描述最大字符数（仅用于"原始数据"展示；技能从完整描述提取）

# 技能关键词（与 viz.py / analysis/clean.py 保持一致，从完整描述提取）
SKILLS = ["Python", "SQL", "Excel", "Pandas", "NumPy", "Tableau", "Power BI",
          "Machine Learning", "Data Mining", "Statistics", "Web Scraping",
          "Spark", "Hadoop", "Hive", "ETL", "Data Warehouse",
          "MySQL", "PostgreSQL", "Airflow", "A/B Testing"]


def parse_salary(s):
    """'$37K-$66K (Glassdoor est.)' -> (37, 66)；单值/时薪返回 None。"""
    s = str(s)
    if s.lower() in ("-1", "nan", ""):
        return None, None
    m = re.search(r"\$(\d+)\s*[kK]\s*-\s*\$?(\d+)\s*[kK]", s)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r"\$(\d+)\s*[kK]", s)
    if m and "hour" not in s.lower():
        return float(m.group(1)), float(m.group(1))
    return None, None


def extract_experience(desc):
    """从描述里估算经验档位（取提到的最高年限，"X+" 按 X+2 计）。"""
    s = desc.lower()
    best = 0
    for m in re.finditer(r"(\d+)(\+)?\s*years?", s):
        y = int(m.group(1))
        if m.group(2):        # 带 '+' 表示"至少 X 年"，向上抬一档
            y += 2
        best = max(best, y)
    if best <= 0:
        return "经验不限"
    if best <= 1:
        return "应届生"
    if best <= 3:
        return "1-3年"
    if best <= 5:
        return "3-5年"
    return "5年以上"


def extract_education(desc):
    """从描述里估算学历要求（取提到的最高学历）。"""
    s = desc.lower()
    if re.search(r"ph\.?d|doctorate", s):
        return "博士"
    if re.search(r"master|m\.s\.|msc", s):
        return "硕士"
    if re.search(r"bachelor|b\.s\.|undergraduate", s):
        return "本科"
    if re.search(r"associate|high school|diploma", s):
        return "大专"
    return "学历不限"


def normalize_size(s):
    s = str(s)
    if "10000" in s:
        return "10000人以上"
    if "5001" in s:
        return "5001-10000人"
    if "1001" in s:
        return "1001-5000人"
    if "501" in s:
        return "501-1000人"
    if "201" in s:
        return "201-500人"
    if "51" in s:
        return "51-200人"
    if "1 to 50" in s:
        return "1-50人"
    return "未知"


def main():
    random.seed(42)
    frames = []
    for f in FILES:
        p = os.path.join(SRC_DIR, f)
        if not os.path.exists(p):
            print(f"[warn] 找不到 {p}，跳过")
            continue
        df = pd.read_csv(p, usecols=["Job Title", "Salary Estimate", "Job Description",
                                     "Company Name", "Location", "Size", "Industry"])
        df = df.dropna(subset=["Job Description"])
        df = df[df["Industry"].astype(str) != "-1"]
        # 去掉 -1 / 时薪，保留年薪
        parsed = df["Salary Estimate"].map(parse_salary)
        df["low"], df["high"] = parsed.map(lambda x: x[0]), parsed.map(lambda x: x[1])
        df = df.dropna(subset=["low", "high"])
        if len(df) > PER_FILE:
            df = df.sample(PER_FILE, random_state=42)
        frames.append(df)
        print(f"{f}: 抽样 {len(df)} 条")

    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset=["Job Title", "Company Name", "Location"]).reset_index(drop=True)
    print(f"去重后共 {len(df)} 条")

    full_desc = df["Job Description"].astype(str)
    desc = full_desc.str.slice(0, DESC_MAX)
    out = pd.DataFrame({
        "job_name": df["Job Title"].astype(str).str.slice(0, 80),
        "company_name": df["Company Name"].fillna("").astype(str),
        "salary_low": df["low"],
        "salary_high": df["high"],
        "location": df["Location"].fillna("").astype(str),
        "experience": full_desc.map(extract_experience),
        "education": full_desc.map(extract_education),
        "company_size": df["Size"].fillna("").map(normalize_size),
        "industry": df["Industry"].fillna("其他").astype(str),
        "description": desc,
    })

    # 技能列：从完整描述提取（截断后的描述会丢掉 Requirements 段落里的技能词）
    for skill in SKILLS:
        out["skill_" + skill] = full_desc.str.contains(skill, regex=False, case=False).astype(int)

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    out.to_csv(OUT_FILE, index=False, encoding="utf-8-sig")
    print(f"已写入 -> {OUT_FILE}，共 {len(out)} 条")

    print("\n=== 行业 TOP 15 ===")
    print(out["industry"].value_counts().head(15).to_string())
    print("\n=== 学历 / 经验 / 规模 ===")
    print(out["education"].value_counts().to_string())
    print(out["experience"].value_counts().to_string())
    print(out["company_size"].value_counts().head(8).to_string())
    print("\n薪资中位（年薪K美元）:", round(out["salary_low"].median(), 1), "~",
          round(out["salary_high"].median(), 1))


if __name__ == "__main__":
    main()
