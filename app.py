# -*- coding: utf-8 -*-
"""主页：给个工作吧。"""
import os
import streamlit as st
from styles import inject_css, hero
from viz import load_data, SKILLS
from i18n import t, lang_toggle, get_lang

BASE = os.path.dirname(os.path.abspath(__file__))
HERO_IMG = os.path.join(BASE, "assets", "hero.jpg")
OFFICE_IMG = os.path.join(BASE, "assets", "office.jpg")

st.set_page_config(page_title="给个工作吧", page_icon="💼", layout="wide")
inject_css()
lang_toggle()

# —— Hero：左文字右配图 ——
if os.path.exists(HERO_IMG):
    c_text, c_img = st.columns([11, 9], gap="large", vertical_alignment="center")
    with c_text:
        hero("给个工作吧", t("home_subtitle"))
        st.page_link("pages/1_📊_市场分析.py", label=t("home_cta"))
    with c_img:
        st.image(HERO_IMG, use_container_width=True)
else:
    hero("给个工作吧", t("home_subtitle"))

# —— 数据亮点 ——
df = load_data()
n_total = len(df)
n_cn = int((df["country"] == "CN").sum())
n_us = int((df["country"] == "US").sum())
n_ind = int(df["industry"].nunique()) if "industry" in df.columns else 0

st.markdown(
    f"""
    <div class="stats">
        <div class="stat"><div class="stat-num">{n_total:,}</div><div class="stat-label">{t('stat_jobs')}</div></div>
        <div class="stat"><div class="stat-num">{n_ind}</div><div class="stat-label">{t('stat_industries')}</div></div>
        <div class="stat"><div class="stat-num">{len(SKILLS)}</div><div class="stat-label">{t('stat_skills')}</div></div>
        <div class="stat"><div class="stat-num">7</div><div class="stat-label">{t('stat_ai')}</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# —— 数据说明 ——
if get_lang() == "zh":
    data_note_html = (
        '<div class="data-note"><b>数据说明</b>：本站为<b>真实岗位数据</b>，共 <b>'
        f'{n_total:,}</b> 条 —— 中国样本约 <b>{n_cn:,}</b> 条（一线城市，月薪·人民币）＋ 美国样本约 <b>{n_us:,}</b> 条（全美，年薪·美元）。'
        '两国薪资口径不同：对比页并排展示、各自标单位，不做汇率换算。</div>'
    )
else:
    data_note_html = (
        '<div class="data-note"><b>Data</b>: real job postings — <b>'
        f'{n_total:,}</b> in total: ~<b>{n_cn:,}</b> China (a tier-1 city, monthly CNY) + ~<b>{n_us:,}</b> US (nationwide, annual USD). '
        'The two use different salary bases; the Compare view shows them side by side without currency conversion.</div>'
    )
st.markdown(data_note_html, unsafe_allow_html=True)

# —— 价值主张：照片 + 三个要点 ——
if os.path.exists(OFFICE_IMG):
    c_img, c_txt = st.columns([9, 11], gap="large", vertical_alignment="center")
    with c_img:
        st.image(OFFICE_IMG, use_container_width=True)
    with c_txt:
        st.markdown(f'<div class="section-label">{t("home_how")}</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="value-point"><div class="value-point-icon">📊</div>
              <div><div class="value-point-title">{t('vp1_title')}</div>
              <div class="value-point-desc">{t('vp1_desc')}</div></div></div>
            <div class="value-point"><div class="value-point-icon">💪</div>
              <div><div class="value-point-title">{t('vp2_title')}</div>
              <div class="value-point-desc">{t('vp2_desc')}</div></div></div>
            <div class="value-point"><div class="value-point-icon">📝</div>
              <div><div class="value-point-title">{t('vp3_title')}</div>
              <div class="value-point-desc">{t('vp3_desc')}</div></div></div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(f'<div class="section-label">{t("home_features")}</div>', unsafe_allow_html=True)

cards = [
    ("📊", t("card1_title"), t("card1_desc"), "pages/1_📊_市场分析.py", t("card1_btn")),
    ("🧰", t("card2_title"), t("card2_desc"), "pages/2_🧰_求职工具箱.py", t("card2_btn")),
    ("💪", t("card3_title"), t("card3_desc"), "pages/3_💪_技能排行.py", t("card3_btn")),
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
