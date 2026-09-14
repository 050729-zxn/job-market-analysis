# -*- coding: utf-8 -*-
"""招聘市场分析看板（多页应用第 1 页）：市场全景，支持中/美/对比视角。"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import plotly.express as px
from styles import inject_css, hero
from viz import load_data, style_fig, hbar, country_select, skill_display, BLUE, BLUE_LIGHT, BLUE_PALE, BLUE_PALER, DARK, SKILLS
from i18n import t, salary_text, jobs_str, lang_toggle, cat_text, cat_multiselect

st.set_page_config(page_title="给个工作吧 · 市场分析", page_icon="📊", layout="wide")
inject_css()
lang_toggle()

st.page_link("app.py", label=t("back_home"))

df = load_data()

hero(t("market_title"), t("market_subtitle"))
st.caption(t("market_hint"))

mode = country_select()

# 逻辑排序
EDU_ORDER = ["学历不限", "大专", "本科", "硕士", "博士"]
EXP_ORDER = ["经验不限", "应届生", "1-3年", "3-5年", "5年以上"]


def _ordered(opts, order):
    return sorted(opts, key=lambda x: order.index(x) if x in order else len(order))


def render_market(view, base, country, allow_link, key_prefix):
    """渲染某国完整市场看板。view=联动/筛选后的数据，base=仅筛选后的数据（行业对比用）。"""
    # —— 概览 KPI ——
    st.subheader(t("overview", n=len(view)))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("metric_jobs"), jobs_str(len(view)))
    c2.metric(salary_text(country, "avg"), f"{view['salary_mid'].mean():.1f} K")
    c3.metric(salary_text(country, "med"), f"{view['salary_mid'].median():.1f} K")
    top_skill = max(SKILLS, key=lambda s: int(view["skill_" + s].sum()))
    c4.metric(t("metric_top_skill"), skill_display(top_skill))
    st.caption(salary_text(country, "cap"))

    st.divider()

    # —— 薪资分布 ——
    st.subheader(t("sec_salary_dist"))
    fig = px.histogram(view, x="salary_mid", nbins=20, color_discrete_sequence=[BLUE],
                       text_auto=True)
    fig.update_layout(xaxis_title=salary_text(country, "axis"), yaxis_title=t("axis_jobs"))
    fig.update_traces(marker_line=dict(color="white", width=1),
                      textposition="outside", textfont=dict(size=11, color=DARK))
    st.plotly_chart(style_fig(fig, height=320), use_container_width=True)
    st.caption(t("cap_salary_dist", unit=salary_text(country, "axis")))

    # —— 行业对比（可点击联动，仅单国模式） ——
    st.subheader(t("sec_industry"))
    c1, c2 = st.columns(2)
    sel = None
    label2raw = {}
    with c1:
        st.markdown(f"**{t('ind_count_title')}**")
        cnt = base["industry"].value_counts()
        ind_labels = [cat_text("industry", x) for x in cnt.index]
        label2raw = dict(zip(ind_labels, cnt.index))
        if allow_link:
            sel = st.plotly_chart(
                hbar(ind_labels, cnt.values, xlabel=t("axis_jobs")),
                use_container_width=True, on_select="rerun", selection_mode="points",
                key=f"{key_prefix}_ind_click",
            )
            st.caption(t("cap_click"))
        else:
            st.plotly_chart(hbar(ind_labels, cnt.values, xlabel=t("axis_jobs")),
                            use_container_width=True)
    with c2:
        st.markdown(f"**{salary_text(country, 'ind_avg')}**")
        ind_salary = base.groupby("industry")["salary_mid"].mean().sort_values(ascending=False)
        st.plotly_chart(hbar([cat_text("industry", x) for x in ind_salary.index],
                             ind_salary.values,
                             xlabel=salary_text(country, "axis"), fmt="{:,.1f}"),
                        use_container_width=True)
        st.caption(t("cap_ind_salary"))

    # 处理点击联动
    if allow_link and sel and sel.selection and sel.selection.get("points"):
        clicked_label = sel.selection["points"][0].get("y")
        clicked = label2raw.get(clicked_label, clicked_label)
        if clicked and clicked != st.session_state.get("linked_ind"):
            st.session_state["linked_ind"] = clicked
            st.rerun()

    st.divider()

    # —— 学历 + 经验 ——
    st.subheader(t("sec_edu_exp"))
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{t('edu_dist_title')}**")
        edu_counts = view["education"].value_counts().reset_index()
        edu_counts.columns = ["education", "count"]
        edu_counts["edu_label"] = edu_counts["education"].apply(lambda v: cat_text("education", v))
        fig = px.pie(edu_counts, names="edu_label", values="count",
                     color_discrete_sequence=[BLUE, BLUE_LIGHT, BLUE_PALE, BLUE_PALER],
                     hole=0.35)
        fig.update_traces(textinfo="label+percent", textfont=dict(size=12, color=DARK))
        st.plotly_chart(style_fig(fig, height=340), use_container_width=True)
        st.caption(t("cap_edu"))
    with c2:
        st.markdown(f"**{t('exp_dist_title')}**")
        exp_cnt = view["experience"].value_counts()
        st.plotly_chart(hbar([cat_text("experience", x) for x in exp_cnt.index],
                             exp_cnt.values, xlabel=t("axis_jobs")),
                        use_container_width=True)
        st.caption(t("cap_exp"))

    st.divider()

    # —— 单个行业深挖 ——
    st.subheader(t("sec_deepdive"))
    ind_list = _ordered(base["industry"].dropna().unique().tolist(), [])
    chosen = st.selectbox(t("pick_ind"), ind_list, key=f"{key_prefix}_deepind",
                          format_func=lambda v: cat_text("industry", v))
    sub = base[base["industry"] == chosen]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t("metric_jobs_short"), jobs_str(len(sub)))
    m2.metric(salary_text(country, "avg"), f"{sub['salary_mid'].mean():.1f}")
    m3.metric(salary_text(country, "med"), f"{sub['salary_mid'].median():.1f}")
    main_edu = sub["education"].value_counts().index[0] if len(sub) else "—"
    m4.metric(t("metric_main_edu"), cat_text("education", main_edu) if main_edu != "—" else "—")
    st.caption(t("cap_deepdive", ind=cat_text("industry", chosen), n=len(sub),
                 unit_cap=salary_text(country, "cap")))

    # —— 原始数据 ——
    with st.expander(t("view_raw")):
        st.dataframe(view)


# —— 单国模式：筛选器 + 联动 ——
if mode in ("CN", "US"):
    sub = df[df["country"] == mode]
    f1, f2, f3 = st.columns(3)
    with f1:
        edu_opt = _ordered(sub["education"].dropna().unique().tolist(), EDU_ORDER)
        sel_edu = cat_multiselect(t("f_edu"), edu_opt, "education", f"edu_{mode}")
    with f2:
        exp_opt = _ordered(sub["experience"].dropna().unique().tolist(), EXP_ORDER)
        sel_exp = cat_multiselect(t("f_exp"), exp_opt, "experience", f"exp_{mode}")
    with f3:
        ind_opt = sorted(sub["industry"].dropna().unique().tolist())
        sel_ind = cat_multiselect(t("f_ind"), ind_opt, "industry", f"ind_{mode}")

    base = sub[
        sub["education"].isin(sel_edu)
        & sub["experience"].isin(sel_exp)
        & sub["industry"].isin(sel_ind)
    ]
    if base.empty:
        st.warning(t("no_data"))
        st.stop()

    if "linked_ind" not in st.session_state:
        st.session_state["linked_ind"] = None
    linked = st.session_state["linked_ind"]
    if linked and linked in base["industry"].values:
        filtered = base[base["industry"] == linked]
    else:
        filtered = base

    if linked and linked in base["industry"].values:
        c1, c2 = st.columns([8, 2])
        with c1:
            st.info(t("linked_info", ind=cat_text("industry", linked)))
        with c2:
            if st.button(t("clear_link"), use_container_width=True, key=f"clear_{mode}"):
                st.session_state["linked_ind"] = None
                st.rerun()

    render_market(filtered, base, mode, allow_link=True, key_prefix=mode)

# —— 对比模式：并排渲染，不做联动 ——
else:
    cn = df[df["country"] == "CN"]
    us = df[df["country"] == "US"]
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(t("c_cn"))
        render_market(cn, cn, "CN", allow_link=False, key_prefix="cn")
    with c2:
        st.subheader(t("c_us"))
        render_market(us, us, "US", allow_link=False, key_prefix="us")
