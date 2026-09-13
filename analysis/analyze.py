# -*- coding: utf-8 -*-
"""分析：对清洗后的数据做统计，输出图表到 output/，并打印核心结论。

运行：python analysis/analyze.py
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # 无界面环境也能保存图片
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED = os.path.join(BASE_DIR, "data", "cleaned", "cleaned.csv")
OUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]  # 中文字体
plt.rcParams["axes.unicode_minus"] = False

SKILLS = ["Python", "SQL", "Excel", "Pandas", "NumPy", "Tableau", "PowerBI", "机器学习",
          "数据挖掘", "爬虫", "Spark", "Hadoop", "统计分析", "可视化", "A/B测试", "MySQL",
          "Hive", "ETL", "数据仓库", "FineBI"]

# 技能分类（skill -> 类别），用于各行业排行榜按类别展示
SKILL_CATEGORY = {
    "Python": "编程语言",
    "Pandas": "数据处理", "NumPy": "数据处理", "Excel": "数据处理",
    "统计分析": "数据处理", "数据挖掘": "数据处理", "A/B测试": "数据处理", "爬虫": "数据处理",
    "SQL": "数据库", "MySQL": "数据库",
    "Tableau": "可视化", "PowerBI": "可视化", "FineBI": "可视化", "可视化": "可视化",
    "Spark": "大数据", "Hadoop": "大数据", "Hive": "大数据", "ETL": "大数据", "数据仓库": "大数据",
    "机器学习": "机器学习",
}


def save_fig(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print("已生成图表:", name)


def plot_salary_dist(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["salary_mid"], bins=20, color="#1F4E79", edgecolor="white")
    ax.set_title("薪资分布（月薪 K）")
    ax.set_xlabel("月薪(K)")
    ax.set_ylabel("岗位数")
    save_fig(fig, "salary_dist.png")


def plot_skill_top(df):
    counts = {s: int(df["skill_" + s].sum()) for s in SKILLS}
    counts = dict(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10])
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(list(counts.keys())[::-1], list(counts.values())[::-1], color="#2E75B6")
    ax.set_title("技能要求 Top10")
    ax.set_xlabel("出现次数")
    save_fig(fig, "skill_top.png")


def plot_education(df):
    counts = df["education"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("学历要求分布")
    save_fig(fig, "education.png")


def plot_location(df):
    counts = df["location"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(counts.index, counts.values, color="#1F4E79")
    ax.set_title("岗位地区分布 Top10")
    ax.set_xlabel("地区")
    ax.set_ylabel("岗位数")
    plt.xticks(rotation=45)
    save_fig(fig, "location.png")


def plot_industry_dist(df):
    """各行业岗位数量分布。"""
    counts = df["industry"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(counts.index, counts.values, color="#1F4E79")
    ax.set_title("各行业岗位数量分布")
    ax.set_xlabel("行业")
    ax.set_ylabel("岗位数")
    plt.xticks(rotation=45)
    save_fig(fig, "industry_dist.png")


def plot_industry_salary(df):
    """各行业平均月薪对比。"""
    avg = df.groupby("industry")["salary_mid"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(avg.index, avg.values, color="#2E75B6")
    ax.set_title("各行业平均月薪对比")
    ax.set_xlabel("平均月薪(K)")
    save_fig(fig, "industry_salary.png")


def export_industry_skill_rank(df):
    """各行业技能出现率排行榜：每个行业独立统计，输出 CSV。

    出现率 = 该技能在本行业岗位描述中出现次数 ÷ 本行业岗位数 × 100%。
    同一技能在不同行业时，分别按各自行业的岗位数计算，互不混淆。
    """
    rows = []
    for industry, sub in df.groupby("industry"):
        n = len(sub)
        for skill in SKILLS:
            count = int(sub["skill_" + skill].sum())
            rate = round(count / n * 100, 1) if n else 0.0
            rows.append({
                "industry": industry,
                "skill": skill,
                "category": SKILL_CATEGORY.get(skill, "其他"),
                "count": count,
                "rate": rate,
            })
    rank = pd.DataFrame(rows)
    rank = rank.sort_values(["industry", "rate"], ascending=[True, False]).reset_index(drop=True)
    out = os.path.join(OUT_DIR, "industry_skill_rank.csv")
    rank.to_csv(out, index=False, encoding="utf-8-sig")
    print("已生成各行业技能出现率排行榜:", out)
    return rank


def print_conclusions(df):
    print("\n===== 核心结论 =====")
    print(f"有效岗位数：{len(df)}")
    print(f"平均月薪：{df['salary_mid'].mean():.1f} K，中位数：{df['salary_mid'].median():.1f} K")
    top_skills = sorted(SKILLS, key=lambda s: df["skill_" + s].sum(), reverse=True)[:5]
    print("最吃香的技能 Top5：", "、".join(top_skills))
    print("学历要求分布：", dict(df["education"].value_counts()))
    print("经验要求分布：", dict(df["experience"].value_counts()))
    ind_salary = df.groupby("industry")["salary_mid"].mean().sort_values(ascending=False)
    print("各行业平均月薪排行：", " > ".join([f"{k}{v:.1f}K" for k, v in ind_salary.items()]))


def main():
    if not os.path.exists(CLEANED):
        raise FileNotFoundError("找不到 cleaned.csv，请先运行 python analysis/clean.py")
    df = pd.read_csv(CLEANED)
    plot_salary_dist(df)
    plot_skill_top(df)
    plot_education(df)
    plot_location(df)
    plot_industry_dist(df)
    plot_industry_salary(df)
    export_industry_skill_rank(df)
    print_conclusions(df)


if __name__ == "__main__":
    main()
