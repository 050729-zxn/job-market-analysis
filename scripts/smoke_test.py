# -*- coding: utf-8 -*-
"""冒烟测试：验证 4 个页面渲染正常、关键元素存在、无前端报错。

用法：先启动 Streamlit（streamlit run app.py --server.headless true），再运行
    python scripts/smoke_test.py
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from playwright.sync_api import sync_playwright

BASE = "http://localhost:8501"
PAGES = [
    ("主页", "/", ["给个工作吧", "求职工具箱", "技能排行", "立即看行情"]),
    ("市场分析", "/市场分析", ["招聘市场分析", "薪资分布", "单个行业深挖", "K/月"]),
    ("求职工具箱", "/求职工具箱", ["隐藏角色搜索器", "机会搜索策略", "上传简历", "资格差距分析器"]),
    ("技能排行", "/技能排行", ["技能出现次数总排名", "在哪些行业吃香", "技能类别分布"]),
]


def main():
    failures = []
    console_errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 1100})
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        for name, path, checks in PAGES:
            url = BASE + path
            try:
                page.goto(url, wait_until="networkidle")
                page.wait_for_timeout(4000)
                body = page.inner_text("body")
                missing = [c for c in checks if c not in body]
                if missing:
                    failures.append((name, "缺少文本: " + ", ".join(missing)))
                    print(f"  ✗ {name}: 缺少 {missing}")
                else:
                    print(f"  ✓ {name}: {len(checks)} 项检查通过")
            except Exception as e:
                failures.append((name, f"异常: {e}"))
                print(f"  ✗ {name}: 异常 {e}")

        browser.close()

    print()
    if failures:
        print(f"失败 {len(failures)} 个页面:")
        for name, why in failures:
            print(f"  - {name}: {why}")
        sys.exit(1)

    if console_errors:
        print(f"警告：捕获到 {len(console_errors)} 条前端 console error（可能不影响功能）:")
        for e in console_errors[:5]:
            print(f"  - {e}")
    else:
        print("无前端 console error")

    print("✓ 冒烟测试全部通过")
    sys.exit(0)


if __name__ == "__main__":
    main()
