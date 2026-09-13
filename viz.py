# -*- coding: utf-8 -*-
"""共享可视化工具：配色、技能词表、Plotly 图表函数、数据加载。"""
import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANED = os.path.join(BASE_DIR, "data", "cleaned", "cleaned.csv")

BLUE = "#1F4E79"        # 主色：第一名 / 重点
BLUE_LIGHT = "#2E75B6"  # 次级色：其余条目
BLUE_PALE = "#7BA7D0"
BLUE_PALER = "#B8CBE0"
GREY = "#4B5563"        # 次要说明文字
DARK = "#1F2937"        # 主文字 / 图表文字
FONT = "Microsoft YaHei, PingFang SC, Noto Sans SC, sans-serif"

SKILLS = ["Python", "SQL", "Excel", "Pandas", "NumPy", "Tableau", "PowerBI", "机器学习",
          "数据挖掘", "爬虫", "Spark", "Hadoop", "统计分析", "可视化", "A/B测试", "MySQL",
          "Hive", "ETL", "数据仓库", "FineBI"]

SKILL_CATEGORY = {
    "Python": "编程语言",
    "Pandas": "数据处理", "NumPy": "数据处理", "Excel": "数据处理",
    "统计分析": "数据处理", "数据挖掘": "数据处理", "A/B测试": "数据处理", "爬虫": "数据处理",
    "SQL": "数据库", "MySQL": "数据库",
    "Tableau": "可视化", "PowerBI": "可视化", "FineBI": "可视化", "可视化": "可视化",
    "Spark": "大数据", "Hadoop": "大数据", "Hive": "大数据", "ETL": "大数据", "数据仓库": "大数据",
    "机器学习": "机器学习",
}


@st.cache_data
def load_data():
    if not os.path.exists(CLEANED):
        st.error("找不到清洗后的数据，请先运行 python analysis/clean.py")
        st.stop()
    return pd.read_csv(CLEANED)


def style_fig(fig, height=None):
    """统一的 Plotly 样式：白底、浅灰网格、深色文字、统一配色。"""
    fig.update_layout(
        font=dict(family=FONT, size=12, color=DARK),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=10, r=40, t=20, b=30),
        colorway=[BLUE, BLUE_LIGHT, BLUE_PALE, BLUE_PALER],
    )
    if height:
        fig.update_layout(height=height)
    fig.update_xaxes(showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    fig.update_yaxes(showgrid=False)
    return fig


def hbar(labels, values, xlabel="", fmt="{:,.0f}", highlight=True):
    """横向条形图（交互版）：分类标签竖排、文字水平，第一名在顶部并高亮。

    labels 需按数值降序传入；悬停可看具体数值，可缩放、平移。
    """
    labels = list(labels)
    values = [float(v) for v in values]
    n = len(labels)
    colors = [BLUE_LIGHT] * n
    if highlight and n:
        colors[0] = BLUE
    text = [fmt.format(v) for v in values]
    fig = go.Figure(go.Bar(
        x=values, y=labels, orientation="h",
        marker_color=colors,
        text=text, textposition="outside",
        textfont=dict(size=11, color=DARK),
        hovertemplate="%{y}：%{x}<extra></extra>",
    ))
    fig.update_yaxes(autorange="reversed")  # 第一名在顶部
    fig.update_layout(xaxis_title=xlabel, yaxis_title=None)
    fig.update_yaxes(tickfont=dict(size=12, color=DARK))
    fig = style_fig(fig, height=max(300, 38 * n + 80))
    fig.update_layout(margin=dict(r=70))  # 右侧留白，避免数值标签被裁切
    return fig
