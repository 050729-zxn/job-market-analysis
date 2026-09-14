# -*- coding: utf-8 -*-
"""数据清洗：合并中国 + 美国真实岗位数据，输出 cleaned.csv（含 country 列）。

数据来源（均 gitignore，不上传）：
  data/raw/boss.csv     —— 中国样本（300 条，BOSS直聘公开数据集，月薪·人民币）
  data/raw/global.csv   —— 美国样本（5553 条，公开数据集，年薪·美元）
运行：python analysis/clean.py
"""
import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from skills import SKILLS, SKILL_PATTERNS  # noqa: E402

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
CLEANED_DIR = os.path.join(BASE_DIR, "data", "cleaned")
OUT_FILE = os.path.join(CLEANED_DIR, "cleaned.csv")

# 中国数据经验档位 → 与美国口径对齐
CN_EXP_MAP = {
    "在校/应届": "应届生", "应届生": "应届生", "应届": "应届生",
    "经验不限": "经验不限", "不限": "经验不限",
    "1-3年": "1-3年", "3-5年": "3-5年",
    "5-10年": "5年以上", "10年以上": "5年以上", "10年": "5年以上",
}

# 最终输出列顺序
BASE_COLS = ["job_name", "company_name", "salary_low", "salary_high", "salary_mid",
             "location", "experience", "education", "company_size", "industry",
             "country", "description"]


def norm_exp(x):
    x = str(x)
    return CN_EXP_MAP.get(x, "5年以上")


def extract_skills_cn(df):
    """从中文描述里提取技能（双语词表，大小写不敏感、子串匹配）。"""
    desc = df["description"].fillna("").astype(str).str.lower()
    for skill in SKILLS:
        hit = pd.Series(False, index=df.index)
        for p in SKILL_PATTERNS[skill]:
            hit = hit | desc.str.contains(p, regex=False)
        df["skill_" + skill] = hit.astype(int)
    return df


def clean_salary(df):
    """薪资转数值、补缺失、算中值。"""
    df["salary_low"] = pd.to_numeric(df["salary_low"], errors="coerce").fillna(0)
    df["salary_high"] = pd.to_numeric(df["salary_high"], errors="coerce").fillna(0)
    df["salary_mid"] = (df["salary_low"] + df["salary_high"]) / 2
    return df


def load_cn():
    """加载中国样本，加 country、归一经验、提取技能。"""
    p = os.path.join(RAW_DIR, "boss.csv")
    if not os.path.exists(p):
        return None
    df = pd.read_csv(p)
    df["country"] = "CN"
    df["experience"] = df["experience"].map(norm_exp)
    df = extract_skills_cn(df)
    return df


def load_us():
    """加载美国样本，加 country（技能列已在解析阶段从完整描述提取好）。"""
    p = os.path.join(RAW_DIR, "global.csv")
    if not os.path.exists(p):
        return None
    df = pd.read_csv(p)
    df["country"] = "US"
    return df


def main():
    frames = []
    cn = load_cn()
    if cn is not None:
        frames.append(cn)
        print(f"中国样本：{len(cn)} 条")
    us = load_us()
    if us is not None:
        frames.append(us)
        print(f"美国样本：{len(us)} 条")

    if not frames:
        raise FileNotFoundError(
            "data/raw 下没有 boss.csv / global.csv，请先运行数据解析脚本。"
        )

    df = pd.concat(frames, ignore_index=True)
    df = clean_salary(df)

    # 去除薪资为 0 的无效记录
    df = df[df["salary_mid"] > 0].reset_index(drop=True)

    # 统一列顺序
    skill_cols = ["skill_" + s for s in SKILLS]
    df = df[[c for c in BASE_COLS + skill_cols if c in df.columns]]

    os.makedirs(CLEANED_DIR, exist_ok=True)
    df.to_csv(OUT_FILE, index=False, encoding="utf-8-sig")
    print(f"清洗完成 -> {OUT_FILE}，有效 {len(df)} 条")

    print("\n=== 按国家 ===")
    print(df["country"].value_counts().to_string())
    print("\n=== 中国技能 Top 8 ===")
    cn_sub = df[df["country"] == "CN"]
    top = {s: int(cn_sub["skill_" + s].sum()) for s in SKILLS}
    print(sorted(top.items(), key=lambda x: x[1], reverse=True)[:8])


if __name__ == "__main__":
    main()
