# -*- coding: utf-8 -*-
"""生成示例招聘数据。

用途：在拿到真实爬取数据之前，先用示例数据把「清洗 -> 分析 -> 看板」
整条链路跑通，方便验证流程、截图演示、写进简历。

运行：python crawler/make_sample_data.py
"""
import os
import random
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_FILE = os.path.join(BASE_DIR, "data", "raw", "sample.csv")

# 工作地点（示例数据）
LOCATIONS = ["南山区", "福田区", "龙岗区", "宝安区", "罗湖区", "龙华区", "光明区", "盐田区", "坪山区"]

# 岗位名（数据分析方向）
JOB_NAMES = ["数据分析师", "数据分析实习生", "数据运营", "商业分析", "BI分析师", "数据产品经理", "数据挖掘工程师"]

# 公司（真实大厂 + 虚构中小厂混排，仅示例用）
COMPANIES = ["腾讯科技", "华为技术", "平安科技", "招商银行", "顺丰速运", "比亚迪", "大疆创新", "中兴通讯",
             "华润置地", "万科集团", "智联科技", "云帆数据", "星辰互联网", "极光智能", "深蓝信息"]

# 经验要求（应届/1-3年为主，更贴近实习生求职视角）
EXPERIENCE = ["应届生", "经验不限", "1-3年", "3-5年", "5-10年"]
EXP_WEIGHTS = [0.20, 0.15, 0.40, 0.18, 0.07]

# 学历要求
EDUCATION = ["大专", "本科", "硕士", "博士"]
EDU_WEIGHTS = [0.15, 0.65, 0.17, 0.03]

# 公司规模
COMPANY_SIZE = ["0-20人", "20-99人", "100-499人", "500-999人", "1000-9999人", "10000人以上"]
SIZE_WEIGHTS = [0.05, 0.20, 0.30, 0.15, 0.20, 0.10]

# 行业 -> (岗位占比权重, 薪资下限, 薪资上限)
# 权重让热门行业岗位更多，薪资范围让不同行业有明显区分，便于做行业对比分析
INDUSTRY_PROFILE = {
    "互联网":   (0.22, 12, 20),
    "软件服务": (0.15, 11, 18),
    "金融":     (0.14, 14, 25),
    "人工智能": (0.10, 15, 28),
    "电子商务": (0.09, 10, 16),
    "通信":     (0.07, 11, 18),
    "教育":     (0.06, 7, 11),
    "医疗健康": (0.06, 9, 15),
    "制造":     (0.06, 8, 13),
    "物流":     (0.05, 7, 12),
}
INDUSTRY = list(INDUSTRY_PROFILE.keys())
INDUSTRY_WEIGHTS = [p[0] for p in INDUSTRY_PROFILE.values()]

# 技能关键词池（用于拼装职位描述，与分析脚本保持一致）
SKILLS = ["Python", "SQL", "Excel", "Pandas", "NumPy", "Tableau", "PowerBI", "机器学习",
          "数据挖掘", "爬虫", "Spark", "Hadoop", "统计分析", "可视化", "A/B测试", "MySQL",
          "Hive", "ETL", "数据仓库", "FineBI"]

random.seed(42)


def make_description():
    """随机拼装一条职位描述，含 2~5 个技能关键词。

    注意 base 文本不能包含任何技能关键词，否则会导致该词出现率虚高（接近 100%）。
    """
    k = random.randint(2, 5)
    chosen = random.sample(SKILLS, k)
    base = "负责业务数据的采集与清洗，输出分析报告与数据看板，支撑运营决策。"
    return base + " 要求熟练使用 " + "、".join(chosen) + "。"


def make_salary(industry):
    """按行业基础薪资生成月薪区间（K），再加随机扰动。"""
    _, base_low, base_high = INDUSTRY_PROFILE[industry]
    low = base_low + random.randint(-2, 2)
    high = base_high + random.randint(-2, 4)
    return max(low, 5), high


def main(n=500):
    rows = []
    for _ in range(n):
        industry = random.choices(INDUSTRY, weights=INDUSTRY_WEIGHTS)[0]
        low, high = make_salary(industry)
        rows.append({
            "job_name": random.choice(JOB_NAMES),
            "company_name": random.choice(COMPANIES),
            "salary_low": low,
            "salary_high": high,
            "location": random.choice(LOCATIONS),
            "experience": random.choices(EXPERIENCE, weights=EXP_WEIGHTS)[0],
            "education": random.choices(EDUCATION, weights=EDU_WEIGHTS)[0],
            "company_size": random.choices(COMPANY_SIZE, weights=SIZE_WEIGHTS)[0],
            "industry": industry,
            "description": make_description(),
        })
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    df.to_csv(OUT_FILE, index=False, encoding="utf-8-sig")
    print(f"已生成示例数据 {n} 条 -> {OUT_FILE}")


if __name__ == "__main__":
    main(500)
