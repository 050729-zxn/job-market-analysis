# -*- coding: utf-8 -*-
"""数据清洗：把爬取/示例数据统一格式，输出 cleaned.csv。

优先读取 data/raw/boss.csv（真实爬取），没有则退回 sample.csv（示例数据）。
运行：python analysis/clean.py
"""
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")
OUT_FILE = os.path.join(CLEANED_DIR, "cleaned.csv")

# 技能关键词（与 viz.py 保持一致，用于从描述中提取）
SKILLS = ["Python", "SQL", "Excel", "Pandas", "NumPy", "Tableau", "Power BI",
          "Machine Learning", "Data Mining", "Statistics", "Web Scraping",
          "Spark", "Hadoop", "Hive", "ETL", "Data Warehouse",
          "MySQL", "PostgreSQL", "Airflow", "A/B Testing"]


def pick_raw_file():
    """优先用 global.csv（全球真实数据），其次 boss.csv、sample.csv。"""
    for name in ("global.csv", "boss.csv", "sample.csv"):
        p = os.path.join(RAW_DIR, name)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(
        "data/raw 下没有数据文件，请先运行 python crawler/make_sample_data.py 生成示例数据。"
    )


def clean_salary(df):
    """薪资：转数值、补缺失、算中位月薪。"""
    df["salary_low"] = pd.to_numeric(df["salary_low"], errors="coerce").fillna(0)
    df["salary_high"] = pd.to_numeric(df["salary_high"], errors="coerce").fillna(0)
    df["salary_mid"] = (df["salary_low"] + df["salary_high"]) / 2
    return df


def extract_skills(df):
    """从职位描述里提取技能关键词，生成 skill_ 开头的 0/1 列。

    若数据已带 skill_ 列（parse_global_data.py 已从完整描述提取），则跳过。
    """
    if "skill_Python" in df.columns:
        return df
    desc = df["description"].fillna("").astype(str)
    for skill in SKILLS:
        df["skill_" + skill] = desc.str.contains(skill, regex=False, case=False).astype(int)
    return df


def clean_experience(df):
    """经验要求统一为几档。"""
    def norm(x):
        x = str(x)
        if "应届" in x:
            return "应届生"
        if "不限" in x:
            return "经验不限"
        if "1-3" in x or "1~3" in x:
            return "1-3年"
        if "3-5" in x or "3~5" in x:
            return "3-5年"
        if "5" in x or "10" in x:
            return "5年以上"
        return "其他"

    df["experience"] = df["experience"].apply(norm)
    return df


def main():
    raw = pick_raw_file()
    df = pd.read_csv(raw)
    print(f"读取 {raw}，共 {len(df)} 条")

    df = clean_salary(df)
    df = extract_skills(df)
    df = clean_experience(df)

    # 去除薪资为 0 的无效记录
    df = df[df["salary_mid"] > 0].reset_index(drop=True)

    os.makedirs(CLEANED_DIR, exist_ok=True)
    df.to_csv(OUT_FILE, index=False, encoding="utf-8-sig")
    print(f"清洗完成 -> {OUT_FILE}，有效 {len(df)} 条")


if __name__ == "__main__":
    main()
