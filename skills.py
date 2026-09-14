# -*- coding: utf-8 -*-
"""技能词表（数据方向 20 项）：供 analysis/clean.py 与 viz.py 共用。"""

# 英文规范 key（顺序即默认排名顺序）
SKILLS = ["Python", "SQL", "Excel", "Pandas", "NumPy", "Tableau", "Power BI",
          "Machine Learning", "Data Mining", "Statistics", "Web Scraping",
          "Spark", "Hadoop", "Hive", "ETL", "Data Warehouse",
          "MySQL", "PostgreSQL", "Airflow", "A/B Testing"]

# 每个技能的匹配词表（英文 + 中文别名），大小写不敏感、子串匹配。
# 仅用于中文数据提取；英文数据已在 parse_global_data.py 阶段从完整描述提取好。
SKILL_PATTERNS = {
    "Python": ["python"],
    "SQL": ["sql"],
    "Excel": ["excel"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Tableau": ["tableau"],
    "Power BI": ["power bi", "powerbi"],
    "Machine Learning": ["machine learning", "机器学习", "深度学习"],
    "Data Mining": ["data mining", "数据挖掘"],
    "Statistics": ["statistic", "统计"],
    "Web Scraping": ["web scraping", "scraping", "爬虫", "scrapy"],
    "Spark": ["spark"],
    "Hadoop": ["hadoop"],
    "Hive": ["hive"],
    "ETL": ["etl"],
    "Data Warehouse": ["data warehouse", "数据仓库", "数仓"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "Airflow": ["airflow"],
    "A/B Testing": ["a/b testing", "ab testing", "ab测试", "a/b测试"],
}

# 显示名（双语）
SKILL_LABEL = {
    "Python": {"zh": "Python", "en": "Python"},
    "SQL": {"zh": "SQL", "en": "SQL"},
    "Excel": {"zh": "Excel", "en": "Excel"},
    "Pandas": {"zh": "Pandas", "en": "Pandas"},
    "NumPy": {"zh": "NumPy", "en": "NumPy"},
    "Tableau": {"zh": "Tableau", "en": "Tableau"},
    "Power BI": {"zh": "Power BI", "en": "Power BI"},
    "Machine Learning": {"zh": "机器学习", "en": "Machine Learning"},
    "Data Mining": {"zh": "数据挖掘", "en": "Data Mining"},
    "Statistics": {"zh": "统计分析", "en": "Statistics"},
    "Web Scraping": {"zh": "爬虫", "en": "Web Scraping"},
    "Spark": {"zh": "Spark", "en": "Spark"},
    "Hadoop": {"zh": "Hadoop", "en": "Hadoop"},
    "Hive": {"zh": "Hive", "en": "Hive"},
    "ETL": {"zh": "ETL", "en": "ETL"},
    "Data Warehouse": {"zh": "数据仓库", "en": "Data Warehouse"},
    "MySQL": {"zh": "MySQL", "en": "MySQL"},
    "PostgreSQL": {"zh": "PostgreSQL", "en": "PostgreSQL"},
    "Airflow": {"zh": "Airflow", "en": "Airflow"},
    "A/B Testing": {"zh": "A/B 测试", "en": "A/B Testing"},
}

# 技能类别（类别 key，显示名走 CATEGORY_LABEL）
SKILL_CATEGORY = {
    "Python": "prog",
    "Pandas": "data", "NumPy": "data", "Excel": "data",
    "Statistics": "data", "Data Mining": "data", "Web Scraping": "data", "A/B Testing": "data",
    "SQL": "db", "MySQL": "db", "PostgreSQL": "db",
    "Tableau": "viz", "Power BI": "viz",
    "Spark": "bigdata", "Hadoop": "bigdata", "Hive": "bigdata", "ETL": "bigdata",
    "Data Warehouse": "bigdata", "Airflow": "bigdata",
    "Machine Learning": "ml",
}

CATEGORY_LABEL = {
    "prog": {"zh": "编程语言", "en": "Programming"},
    "data": {"zh": "数据处理", "en": "Data Processing"},
    "db": {"zh": "数据库", "en": "Database"},
    "viz": {"zh": "可视化", "en": "Visualization"},
    "bigdata": {"zh": "大数据", "en": "Big Data"},
    "ml": {"zh": "机器学习", "en": "Machine Learning"},
}
