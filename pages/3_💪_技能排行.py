# -*- coding: utf-8 -*-
"""技能排行页：技能出现次数排名 + 各行业技能出现率，支持中/美/对比视角。"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st
from styles import inject_css, hero
from viz import load_data, hbar, country_select, skill_display, category_display, SKILLS, SKILL_CATEGORY
from i18n import t, lang_toggle

st.set_page_config(page_title="给个工作吧 · 技能排行", page_icon="💪", layout="wide")
inject_css()
lang_toggle()

st.page_link("app.py", label=t("back_home"))

df = load_data()

hero(t("skill_title"), t("skill_subtitle"))
st.caption(t("skill_hint"))

mode = country_select()


def render_skills(sub, country, key_prefix):
    """渲染某国完整技能看板。"""
    # —— 技能出现次数总排名 ——
    st.subheader(t("sec_total_rank", n=len(sub)))
    skill_counts = {s: int(sub["skill_" + s].sum()) for s in SKILLS}
    skill_counts = dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True))
    st.plotly_chart(
        hbar([skill_display(s) for s in skill_counts], skill_counts.values(),
             xlabel=t("axis_count"), fmt="{:,.0f}"),
        use_container_width=True,
    )
    st.caption(t("cap_total_rank"))

    st.divider()

    # —— 技能类别分布 ——
    st.subheader(t("sec_category"))
    cat_totals = {}
    for s, c in SKILL_CATEGORY.items():
        cat_totals[c] = cat_totals.get(c, 0) + skill_counts.get(s, 0)
    cat_totals = dict(sorted(cat_totals.items(), key=lambda x: x[1], reverse=True))
    st.plotly_chart(
        hbar([category_display(c) for c in cat_totals], cat_totals.values(),
             xlabel=t("axis_cat_count"), fmt="{:,.0f}"),
        use_container_width=True,
    )
    st.caption(t("cap_category"))

    st.divider()

    # —— 各行业技能排行榜（出现率） ——
    st.subheader(t("sec_industry_rank"))
    st.caption(t("cap_industry_rank"))

    all_ind = sorted(sub["industry"].dropna().unique().tolist())
    pick_ind = st.selectbox(t("pick_ind_rank"), all_ind, key=f"{key_prefix}_rank_ind")
    sub_ind = sub[sub["industry"] == pick_ind]
    n = len(sub_ind)
    rank_rows = []
    for skill in SKILLS:
        cnt = int(sub_ind["skill_" + skill].sum())
        rate = round(cnt / n * 100, 1) if n else 0.0
        rank_rows.append({
            t("col_skill"): skill_display(skill),
            t("col_cat"): category_display(SKILL_CATEGORY.get(skill, "data")),
            t("col_count"): cnt,
            t("col_rate"): rate,
        })
    rank_df = pd.DataFrame(rank_rows).sort_values(t("col_rate"), ascending=False).reset_index(drop=True)

    top = rank_df.head(15)
    st.plotly_chart(
        hbar(top[t("col_skill")], top[t("col_rate")], xlabel=t("col_rate"), fmt="{:.1f}%"),
        use_container_width=True,
    )
    st.caption(t("cap_top15", ind=pick_ind))

    # —— 技能在哪些行业吃香 ——
    st.subheader(t("sec_skill_industry"))
    st.caption(t("cap_skill_industry"))

    default_skill = list(skill_counts.keys())[0] if skill_counts else SKILLS[0]
    pick_skill = st.selectbox(
        t("pick_skill"), SKILLS, index=SKILLS.index(default_skill),
        key=f"{key_prefix}_skill_ind", format_func=skill_display,
    )
    skill_rows = []
    for ind in all_ind:
        sub2 = sub[sub["industry"] == ind]
        n2 = len(sub2)
        cnt = int(sub2["skill_" + pick_skill].sum())
        rate = round(cnt / n2 * 100, 1) if n2 else 0.0
        skill_rows.append((ind, rate))
    skill_rows.sort(key=lambda x: x[1], reverse=True)
    st.plotly_chart(
        hbar([r[0] for r in skill_rows], [r[1] for r in skill_rows],
             xlabel=t("col_rate"), fmt="{:.1f}%"),
        use_container_width=True,
    )
    st.caption(t("cap_skill_by_ind", skill=skill_display(pick_skill)))

    # —— 完整排名表 ——
    with st.expander(t("view_full_table")):
        show_df = rank_df.copy()
        show_df.index = show_df.index + 1
        st.dataframe(show_df, use_container_width=True)


# —— 单国模式：筛选器 ——
if mode in ("CN", "US"):
    sub = df[df["country"] == mode]
    f1, f2, f3 = st.columns(3)
    with f1:
        edu_opt = sub["education"].dropna().unique().tolist()
        sel_edu = st.multiselect(t("f_edu"), edu_opt, default=edu_opt, key=f"edu_{mode}")
    with f2:
        exp_opt = sub["experience"].dropna().unique().tolist()
        sel_exp = st.multiselect(t("f_exp"), exp_opt, default=exp_opt, key=f"exp_{mode}")
    with f3:
        ind_opt = sub["industry"].dropna().unique().tolist()
        sel_ind = st.multiselect(t("f_ind"), ind_opt, default=ind_opt, key=f"ind_{mode}")

    filtered = sub[
        sub["education"].isin(sel_edu)
        & sub["experience"].isin(sel_exp)
        & sub["industry"].isin(sel_ind)
    ]
    if filtered.empty:
        st.warning(t("no_data"))
        st.stop()

    render_skills(filtered, mode, mode)

# —— 对比模式：并排渲染 ——
else:
    cn = df[df["country"] == "CN"]
    us = df[df["country"] == "US"]
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(t("c_cn"))
        render_skills(cn, "CN", "cn")
    with c2:
        st.subheader(t("c_us"))
        render_skills(us, "US", "us")
