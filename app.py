# -*- coding: utf-8 -*-
"""主页：给个工作吧。"""
import os
import streamlit as st
from styles import inject_css, hero
from viz import load_data, SKILLS

BASE = os.path.dirname(os.path.abspath(__file__))
HERO_IMG = os.path.join(BASE, "assets", "hero.jpg")
OFFICE_IMG = os.path.join(BASE, "assets", "office.jpg")

st.set_page_config(page_title="给个工作吧", page_icon="💼", layout="wide")
inject_css()

# —— Hero：左文字右配图 ——
if os.path.exists(HERO_IMG):
    c_text, c_img = st.columns([11, 9], gap="large", vertical_alignment="center")
    with c_text:
        hero(
            "给个工作吧",
            "海投没回音？先看清市场在招什么、缺什么技能，再把简历改到位。",
        )
        st.page_link("pages/1_📊_市场分析.py", label="立即看行情 →")
    with c_img:
        st.image(HERO_IMG, use_container_width=True)
else:
    hero(
        "给个工作吧",
        "海投没回音？先看清市场在招什么、缺什么技能，再把简历改到位。",
    )

# —— 数据亮点 ——
df = load_data()
n_ind = int(df["industry"].nunique()) if "industry" in df.columns else 0
st.markdown(
    f"""
    <div class="stats">
        <div class="stat"><div class="stat-num">{len(df)}</div><div class="stat-label">岗位样本</div></div>
        <div class="stat"><div class="stat-num">{n_ind}</div><div class="stat-label">覆盖行业</div></div>
        <div class="stat"><div class="stat-num">{len(SKILLS)}</div><div class="stat-label">技能词</div></div>
        <div class="stat"><div class="stat-num">7</div><div class="stat-label">AI 工具</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# —— 数据说明 ——
st.markdown(
    """
    <div class="data-note">
        <b>数据说明</b>：本站图表数据为<b>示例数据</b>（500 条岗位样本，非真实招聘数据），仅用于功能演示。
        薪资为税前估算中值（K = 千元/月），技能词表为预设的 20 项数据分析相关技能。
    </div>
    """,
    unsafe_allow_html=True,
)

# —— 价值主张：照片 + 三个要点 ——
if os.path.exists(OFFICE_IMG):
    c_img, c_txt = st.columns([9, 11], gap="large", vertical_alignment="center")
    with c_img:
        st.image(OFFICE_IMG, use_container_width=True)
    with c_txt:
        st.markdown('<div class="section-label">这个站怎么帮你</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="value-point"><div class="value-point-icon">📊</div>
              <div><div class="value-point-title">先看清行情</div>
              <div class="value-point-desc">哪些行业在招人、给多少钱、要什么学历经验，图表一目了然。</div></div></div>
            <div class="value-point"><div class="value-point-icon">💪</div>
              <div><div class="value-point-title">再找准技能</div>
              <div class="value-point-desc">20 项核心技能出现率排名，别在没人要的技能上花时间。</div></div></div>
            <div class="value-point"><div class="value-point-icon">📝</div>
              <div><div class="value-point-title">最后改好简历</div>
              <div class="value-point-desc">7 个 AI 工具从找方向到排计划，把简历改成招聘方想看到的样子。</div></div></div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-label">功能入口</div>', unsafe_allow_html=True)

cards = [
    ("📊", "招聘市场分析", "薪资、行业、学历、经验全景，点击图表联动筛选。", "pages/1_📊_市场分析.py", "查看行情"),
    ("🧰", "求职工具箱", "7 个 AI 工具：找方向、提技能、补差距、重写简历、排计划。", "pages/2_🧰_求职工具箱.py", "打开工具箱"),
    ("💪", "技能排行", "最吃香技能总排名，以及各行业、各技能的出现率。", "pages/3_💪_技能排行.py", "查看技能"),
]

cols = st.columns(3, gap="medium")
for col, (icon, title, desc, path, label) in zip(cols, cards):
    with col:
        st.markdown(
            f'<div class="card"><div class="card-icon">{icon}</div>'
            f'<div class="card-title">{title}</div>'
            f'<div class="card-desc">{desc}</div></div>',
            unsafe_allow_html=True,
        )
        st.page_link(path, label=label, use_container_width=True)

st.markdown(
    """
    <div class="footer">
        <a href="https://github.com/050729-zxn/job-market-analysis" target="_blank">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True,
)
