# -*- coding: utf-8 -*-
"""全局样式：专业数据仪表盘风。

无衬线、左对齐、卡片分区、图表带标注。配色：白底 + 深灰文字 + 深蓝主色。
"""
import streamlit as st

GLOBAL_CSS = """
<style>
html, body, [class*="css"] {
    font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif;
    color: #1F2937;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {visibility: hidden;}

.stApp { background: #FFFFFF; }

h1, h2, h3, h4 { color: #1F2937 !important; font-weight: 700; letter-spacing: 0; }

/* —— 区块标题：左侧深蓝竖条（仅主区）—— */
h2 {
    border-left: 4px solid #1F4E79;
    padding-left: 12px;
    font-size: 20px;
    margin-top: 8px;
}
h3 {
    border-left: 4px solid #1F4E79;
    padding-left: 12px;
    font-size: 17px;
    margin-top: 6px;
}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    border-left: none;
    padding-left: 0;
}

/* —— Hero（左对齐）—— */
.hero { padding: 32px 0 14px; }
.hero-title { font-size: 46px; font-weight: 700; color: #1F2937; letter-spacing: -1px; }
.hero-sub { margin-top: 12px; font-size: 17px; line-height: 1.6; color: #374151; }

/* —— 指标卡 —— */
div[data-testid="stMetric"] {
    background: #F9FAFB;
    border: 1px solid #E5E7EB;
    border-radius: 6px;
    padding: 16px 18px;
    box-shadow: none;
    transition: box-shadow .2s ease, transform .25s cubic-bezier(.2,.7,.3,1), border-color .2s ease;
}
div[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 12px rgba(31, 78, 121, .1);
    transform: translateY(-2px);
    border-color: #D1D5DB;
}
[data-testid="stMetricLabel"] { color: #1F2937 !important; font-size: 15px !important; font-weight: 700 !important; }
[data-testid="stMetricValue"] { color: #1F4E79 !important; font-size: 24px !important; font-weight: 700 !important; }

/* —— 侧边栏：深墨色 + 浅字 —— */
section[data-testid="stSidebar"] {
    background: #1F2937;
    border-right: none;
}
section[data-testid="stSidebar"] * { color: #E5E7EB !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #FFFFFF !important; }
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea { color: #1F2937 !important; }

/* —— 按钮 —— */
.stButton > button, .stDownloadButton > button {
    background: #1F4E79;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 10px 28px;
    font-weight: 600;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #2E75B6;
    color: #FFFFFF;
}

/* —— 项目条目（首页）—— */
.entry { padding: 20px 0; }
.entry-title { font-size: 20px; font-weight: 700; color: #1F2937; }
.entry-desc {
    max-width: 640px;
    margin: 8px 0 16px;
    font-size: 14px;
    line-height: 1.7;
    color: #374151;
}

/* —— 动作链接（st.page_link）—— */
div.stElementContainer:has(div.stPageLink) { width: 100% !important; }
div.stPageLink { display: flex; justify-content: flex-start; width: 100% !important; }
a[data-testid="stPageLink-NavLink"] {
    display: inline-block;
    background: #1F4E79;
    color: #FFFFFF !important;
    border: none;
    border-radius: 999px;
    padding: 11px 28px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none !important;
    transition: background .3s ease, transform .3s cubic-bezier(.2,.7,.3,1), box-shadow .3s ease;
}
a[data-testid="stPageLink-NavLink"]:hover {
    background: #2E75B6;
    color: #FFFFFF !important;
    transform: translateY(-2px) scale(1.04);
    box-shadow: 0 10px 24px rgba(31, 78, 121, .28);
}

/* —— 页脚 —— */
.footer {
    text-align: center;
    color: #4B5563;
    font-size: 13px;
    padding: 32px 0 16px;
}

/* —— 说明文字（st.caption）—— */
div[data-testid="stCaptionContainer"] { color: #374151 !important; }
div[data-testid="stCaptionContainer"] * { color: #374151 !important; }
section[data-testid="stSidebar"] div[data-testid="stCaptionContainer"],
section[data-testid="stSidebar"] div[data-testid="stCaptionContainer"] * { color: #E5E7EB !important; }
.footer a { color: #1F4E79; text-decoration: none; }
.footer a:hover { text-decoration: underline; }
/* —— 筛选框选中项（chip）：浅灰 —— */
[data-testid="stMultiSelect"] span.e1kig3hy3 {
    background-color: #F3F4F6 !important;
    color: #1F2937 !important;
}
[data-testid="stMultiSelect"] span.e1kig3hy3 span,
[data-testid="stMultiSelect"] span.e1kig3hy4 {
    color: #1F2937 !important;
}

/* —— 首页功能卡片 —— */
.card {
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 22px 22px 18px;
    background: #FFFFFF;
    min-height: 132px;
    transition: border-color .2s ease, box-shadow .2s ease, transform .25s cubic-bezier(.2,.7,.3,1);
}
.card:hover {
    border-color: #1F4E79;
    box-shadow: 0 12px 28px rgba(31, 78, 121, .16);
    transform: translateY(-6px);
}
.card-icon { font-size: 28px; line-height: 1; margin-bottom: 12px; }
.card-title { font-size: 18px; font-weight: 700; color: #1F2937; }
.card-desc { margin-top: 10px; font-size: 14px; line-height: 1.65; color: #374151; }

/* —— 首页数据亮点条 —— */
.stats {
    display: flex;
    gap: 48px;
    padding: 4px 0 22px;
    margin-bottom: 22px;
    border-bottom: 1px solid #E5E7EB;
}
.stat-num { font-size: 26px; font-weight: 700; color: #1F4E79; }
.stat-label { margin-top: 2px; font-size: 13px; color: #374151; }
.section-label { font-size: 15px; font-weight: 700; color: #1F2937; margin: 4px 0 16px; }

/* —— 数据说明条 —— */
.data-note {
    background: #FFF7ED;
    border-left: 3px solid #F59E0B;
    border-radius: 6px;
    padding: 10px 14px;
    margin: 2px 0 18px;
    font-size: 13px;
    line-height: 1.6;
    color: #78350F;
}

/* —— 标签页（st.tabs）—— */
[data-testid="stTab"] p {
    color: #1F2937 !important;
    font-weight: 600;
}
[data-testid="stTab"][aria-selected="true"] p {
    color: #1F4E79 !important;
}

/* —— 求职工具箱：为什么用它 —— */
.why-card {
    background: #F0F5FA;
    border-left: 4px solid #1F4E79;
    border-radius: 6px;
    padding: 14px 18px;
    margin: 12px 0 4px;
}
.why-title { font-size: 15px; font-weight: 700; color: #1F4E79; margin-bottom: 6px; }
.why-body { font-size: 14px; line-height: 1.7; color: #1F2937; }

/* —— 首页价值要点 —— */
.value-point { display: flex; align-items: flex-start; gap: 12px; padding: 10px 0; }
.value-point-icon { font-size: 24px; line-height: 1.3; }
.value-point-title { font-size: 15px; font-weight: 700; color: #1F2937; }
.value-point-desc { margin-top: 2px; font-size: 13.5px; line-height: 1.6; color: #374151; }

/* —— 动画：仅首屏 Hero 一次克制的进场，其余区块直接呈现、靠 hover 反馈 —— */
@keyframes heroIn {
    from { opacity: 0; transform: translateY(32px) scale(.97); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
.hero { animation: heroIn .8s cubic-bezier(.16,.84,.44,1) backwards; }

img { border-radius: 14px !important; }

/* 按钮过渡 + hover 上浮 */
.stButton > button, .stDownloadButton > button {
    transition: background .3s ease, transform .3s cubic-bezier(.2,.7,.3,1), box-shadow .3s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(31, 78, 121, .25);
}
</style>
"""


def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def hero(title, subtitle):
    st.markdown(
        f'<div class="hero"><div class="hero-title">{title}</div>'
        f'<div class="hero-sub">{subtitle}</div></div>',
        unsafe_allow_html=True,
    )


def rule():
    st.markdown('<hr class="rule">', unsafe_allow_html=True)
