# -*- coding: utf-8 -*-
"""BOSS 直聘爬虫（仅个人学习用途）。

BOSS 直聘网页版有较强反爬，需登录后从浏览器复制 Cookie 才能访问接口。
使用步骤：
1. 浏览器登录 www.zhipin.com
2. F12 打开开发者工具 -> Network -> 刷新页面 -> 找到任意请求
3. 复制请求头里的 Cookie 值，填入下方 COOKIE 变量
4. 控制请求频率（脚本已内置随机延时），尊重网站 robots 协议

免责声明：本脚本仅供个人学习，请勿大规模抓取或用于任何商业用途。
字段名可能随网站改版而变化，若返回为空，请按实际返回的 JSON 调整 parse_jobs。
"""
import time
import random
import csv
import os
import requests

# TODO: 替换为你浏览器复制的 Cookie
COOKIE = "在这里填入你浏览器复制的 Cookie"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": COOKIE,
    "Referer": "https://www.zhipin.com/",
}

QUERY = "数据分析"        # 搜索关键词
CITY_CODE = "101280600"   # 目标城市码（可改为其他城市）
BASE_URL = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_FILE = os.path.join(BASE_DIR, "data", "raw", "boss.csv")


def fetch_page(page=1, keyword=QUERY, city=CITY_CODE):
    params = {
        "query": keyword,
        "city": city,
        "page": page,
        "pageSize": 30,
    }
    resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()


def parse_jobs(data):
    """从接口返回里解析岗位字段，字段名若与网站实际不符需自行调整。"""
    jobs = []
    for item in data.get("zpData", {}).get("jobList", []):
        jobs.append({
            "job_name": item.get("jobName", ""),
            "company_name": item.get("brandName", ""),
            "salary_low": item.get("salaryMin", 0),
            "salary_high": item.get("salaryMax", 0),
            "location": str(item.get("cityName", "")) + str(item.get("areaDistrict", "")),
            "experience": item.get("experienceName", ""),
            "education": item.get("educationName", ""),
            "company_size": item.get("brandScaleName", ""),
            "industry": item.get("brandIndustry", ""),
            "description": " ".join(item.get("jobLabels", [])),
        })
    return jobs


def main(pages=10, delay=3):
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    all_jobs = []
    for page in range(1, pages + 1):
        print(f"抓取第 {page} 页...")
        try:
            data = fetch_page(page)
            jobs = parse_jobs(data)
            if not jobs:
                print("没有更多数据，停止。")
                break
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"第 {page} 页失败: {e}")
            print("提示：BOSS 反爬会返回 302 或验证码，此时需要重新登录并更新 Cookie。")
        time.sleep(delay + random.uniform(0, 2))

    if all_jobs:
        with open(OUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=all_jobs[0].keys())
            writer.writeheader()
            writer.writerows(all_jobs)
        print(f"共抓取 {len(all_jobs)} 条 -> {OUT_FILE}")
    else:
        print("未抓到数据，请检查 Cookie 是否有效，或按实际返回 JSON 调整 parse_jobs。")


if __name__ == "__main__":
    main()
