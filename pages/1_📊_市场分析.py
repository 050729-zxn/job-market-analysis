# -*- coding: utf-8 -*-
"""招聘市场分析看板（多页应用第 1 页）：市场全景，Plotly 交互 + 点击联动。"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.express as px
from styles import inject_css, hero
from viz import load_data, style_fig, hbar, BLUE, BLUE_LIGHT, BLUE_PALE, BLUE_PALER, DARK, SKILLS

st.set_page_config(page_title="给个工作吧 · 市场分析", page_icon="📊", layout="wide")
inject_css()

st.page_link("app.py", label="← 返回主页")

df = load_data()

hero(
    "招聘市场分析",
    "全球数据岗的招聘全景：薪资、行业、学历、经验",
)
st.caption("图表可悬停查看数值、框选缩放；点击「行业对比」中的柱子可联动筛选其他图表。")

# —— 顶部筛选（横排） ——
f1, f2, f3 = st.columns(3)
with f1:
    edu_options = df["education"].dropna().unique().tolist()
    selected_edu = st.multiselect("学历", edu_options, default=edu_options)
with f2:
    exp_options = df["experience"].dropna().unique().tolist()
    selected_exp = st.multiselect("经验", exp_options, default=exp_options)
with f3:
    ind_options = df["industry"].dropna().unique().tolist()
    selected_ind = st.multiselect("行业", ind_options, default=ind_options)

base = df[
    df["education"].isin(selected_edu)
    & df["experience"].isin(selected_exp)
    & df["industry"].isin(selected_ind)
]

if base.empty:
    st.warning("当前筛选条件下没有数据，请调整上方筛选。")
    st.stop()

# —— 点击联动状态 ——
if "linked_ind" not in st.session_state:
    st.session_state["linked_ind"] = None

linked_ind = st.session_state["linked_ind"]
if linked_ind and linked_ind in base["industry"].values:
    filtered = base[base["industry"] == linked_ind]
else:
    filtered = base

# 联动提示条
if linked_ind and linked_ind in base["industry"].values:
    c1, c2 = st.columns([8, 2])
    with c1:
        st.info(f"已联动筛选：**{linked_ind}** 行业。下方图表仅显示该行业，点击「清除联动」恢复全部。")
    with c2:
        if st.button("清除联动", use_container_width=True):
            st.session_state["linked_ind"] = None
            st.rerun()

# —— 概览 KPI ——
st.subheader(f"概览（当前 {len(filtered)} 条岗位）")
c1, c2, c3, c4 = st.columns(4)
c1.metric("有效岗位数", f"{len(filtered)} 条")
c2.metric("平均年薪", f"{filtered['salary_mid'].mean():.1f} K")
c3.metric("年薪中位数", f"{filtered['salary_mid'].median():.1f} K")
top_skill = max(SKILLS, key=lambda s: int(filtered["skill_" + s].sum()))
c4.metric("最吃香技能", top_skill)
st.caption("K = 千美元/年。年薪为税前估算中值，数据为公开的真实全球岗位数据。")

st.divider()

# —— 薪资分布 ——
st.subheader("薪资分布")
fig = px.histogram(filtered, x="salary_mid", nbins=20, color_discrete_sequence=[BLUE],
                   text_auto=True)
fig.update_layout(xaxis_title="年薪（K美元）", yaxis_title="岗位数")
fig.update_traces(marker_line=dict(color="white", width=1),
                  textposition="outside", textfont=dict(size=11, color=DARK))
st.plotly_chart(style_fig(fig, height=320), use_container_width=True)
st.caption("横轴为年薪（K美元），纵轴为该薪资区间的岗位数量。悬停可看每个区间的具体数量。")

# —— 行业对比（可点击联动） ——
st.subheader("行业对比")
c1, c2 = st.columns(2)
with c1:
    st.markdown("**各行业岗位数量 · 点击可联动**")
    cnt = base["industry"].value_counts()
    sel = st.plotly_chart(
        hbar(cnt.index, cnt.values, xlabel="岗位数（条）"),
        use_container_width=True, on_select="rerun", selection_mode="points", key="ind_click",
    )
    st.caption("点击某根柱子，其他图表会联动筛选到该行业。")
with c2:
    st.markdown("**各行业平均年薪**")
    ind_salary = base.groupby("industry")["salary_mid"].mean().sort_values(ascending=False)
    st.plotly_chart(hbar(ind_salary.index, ind_salary.values, xlabel="年薪（K美元）", fmt="{:,.1f}"),
                    use_container_width=True)
    st.caption("反映各行业的薪资水平差异。")

# 处理点击联动
if sel and sel.selection and sel.selection.get("points"):
    clicked = sel.selection["points"][0].get("y")
    if clicked and clicked != st.session_state["linked_ind"]:
        st.session_state["linked_ind"] = clicked
        st.rerun()

st.divider()

# —— 学历 + 经验 ——
st.subheader("学历与经验")
c1, c2 = st.columns(2)
with c1:
    st.markdown("**学历要求分布**")
    edu_counts = filtered["education"].value_counts().reset_index()
    edu_counts.columns = ["education", "count"]
    fig = px.pie(edu_counts, names="education", values="count",
                 color_discrete_sequence=[BLUE, BLUE_LIGHT, BLUE_PALE, BLUE_PALER],
                 hole=0.35)
    fig.update_traces(textinfo="label+percent", textfont=dict(size=12, color=DARK))
    st.plotly_chart(style_fig(fig, height=340), use_container_width=True)
    st.caption("各学历要求的岗位占比。")
with c2:
    st.markdown("**经验要求分布**")
    exp_cnt = filtered["experience"].value_counts()
    st.plotly_chart(hbar(exp_cnt.index, exp_cnt.values, xlabel="岗位数（条）"), use_container_width=True)
    st.caption("反映对不同工作年限的需求。")

st.divider()

# —— 单个行业深挖 ——
st.subheader("单个行业深挖")
chosen = st.selectbox("选择一个行业查看详情", sorted(base["industry"].dropna().unique().tolist()))
sub = base[base["industry"] == chosen]
m1, m2, m3, m4 = st.columns(4)
m1.metric("岗位数（条）", f"{len(sub)}")
m2.metric("平均年薪（K美元）", f"{sub['salary_mid'].mean():.1f}")
m3.metric("年薪中位数（K美元）", f"{sub['salary_mid'].median():.1f}")
m4.metric("主要学历要求", sub["education"].value_counts().index[0] if len(sub) else "—")
st.caption(f"「{chosen}」行业共 {len(sub)} 条岗位。年薪为税前估算中值，单位 K = 千美元/年；"
           "技能要求请到「技能排行」页查看。")

# —— 原始数据 ——
with st.expander("查看原始数据"):
    st.dataframe(filtered)
