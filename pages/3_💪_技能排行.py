# -*- coding: utf-8 -*-
"""技能排行页：技能出现次数排名 + 各行业技能出现率。"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st
from styles import inject_css, hero
from viz import load_data, hbar, SKILLS, SKILL_CATEGORY

st.set_page_config(page_title="给个工作吧 · 技能排行", page_icon="💪", layout="wide")
inject_css()

st.page_link("app.py", label="← 返回主页")

df = load_data()

hero(
    "技能排行",
    "全球数据岗最吃香的技能，以及各行业对技能的不同要求",
)
st.caption("出现次数 = 技能在岗位描述中被提及的岗位数；出现率 = 该技能出现次数 ÷ 本行业岗位数。")

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

filtered = df[
    df["education"].isin(selected_edu)
    & df["experience"].isin(selected_exp)
    & df["industry"].isin(selected_ind)
]

if filtered.empty:
    st.warning("当前筛选条件下没有数据，请调整上方筛选。")
    st.stop()

# —— 技能出现次数总排名 ——
st.subheader(f"技能出现次数总排名（当前 {len(filtered)} 条岗位）")
skill_counts = {s: int(filtered["skill_" + s].sum()) for s in SKILLS}
skill_counts = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True))
st.plotly_chart(hbar(skill_counts.keys(), skill_counts.values(), xlabel="出现次数（次）", fmt="{:,.0f}"),
                use_container_width=True)
st.caption("按技能在岗位描述中出现的次数排名，出现越多代表越被企业看重。")

st.divider()

# —— 技能类别分布 ——
st.subheader("技能类别分布")
cat_totals = {}
for s, c in SKILL_CATEGORY.items():
    cat_totals[c] = cat_totals.get(c, 0) + skill_counts.get(s, 0)
cat_totals = dict(sorted(cat_totals.items(), key=lambda x: x[1], reverse=True))
st.plotly_chart(hbar(cat_totals.keys(), cat_totals.values(), xlabel="出现次数合计（次）", fmt="{:,.0f}"),
                use_container_width=True)
st.caption("同一类别下所有技能的出现次数合计，反映企业最看重的能力方向。")

st.divider()

# —— 各行业技能排行榜 ——
st.subheader("各行业技能排行榜（出现率）")
st.caption("出现率 = 该技能在本行业岗位描述中出现次数 ÷ 本行业岗位数。同一技能在不同行业按各自行业独立计算。")

all_ind = sorted(filtered["industry"].dropna().unique().tolist())
pick_ind = st.selectbox("选择行业查看技能排行榜", all_ind, key="rank_ind")
sub = filtered[filtered["industry"] == pick_ind]
n = len(sub)
rank_rows = []
for skill in SKILLS:
    cnt = int(sub["skill_" + skill].sum())
    rate = round(cnt / n * 100, 1) if n else 0.0
    rank_rows.append({
        "技能": skill,
        "类别": SKILL_CATEGORY.get(skill, "其他"),
        "出现次数": cnt,
        "出现率(%)": rate,
    })
rank_df = pd.DataFrame(rank_rows).sort_values("出现率(%)", ascending=False).reset_index(drop=True)

top = rank_df.head(15)
st.plotly_chart(hbar(top["技能"], top["出现率(%)"], xlabel="出现率（%）", fmt="{:.1f}%"),
                use_container_width=True)
st.caption(f"「{pick_ind}」行业技能出现率 Top 15。")

# —— 技能在哪些行业吃香 ——
st.subheader("某个技能，在哪些行业吃香")
st.caption("选一个技能，看它在各行业的出现率排名——帮你判断自己会的技能该投向哪个行业。")

default_skill = list(skill_counts.keys())[0] if skill_counts else SKILLS[0]
pick_skill = st.selectbox("选择一个技能", SKILLS, index=SKILLS.index(default_skill), key="skill_ind")
skill_rows = []
for ind in all_ind:
    sub2 = filtered[filtered["industry"] == ind]
    n2 = len(sub2)
    cnt = int(sub2["skill_" + pick_skill].sum())
    rate = round(cnt / n2 * 100, 1) if n2 else 0.0
    skill_rows.append((ind, rate))
skill_rows.sort(key=lambda x: x[1], reverse=True)
st.plotly_chart(hbar([r[0] for r in skill_rows], [r[1] for r in skill_rows],
                     xlabel="出现率（%）", fmt="{:.1f}%"),
                use_container_width=True)
st.caption(f"「{pick_skill}」在各行业的出现率，越高代表该行业越需要这项技能。")

# —— 完整排名表 ——
with st.expander("查看完整排名表"):
    show_df = rank_df.copy()
    show_df.index = show_df.index + 1
    st.dataframe(show_df, use_container_width=True)
