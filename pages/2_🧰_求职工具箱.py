# -*- coding: utf-8 -*-
"""求职工具箱（多页应用第 2 页）：7 个 AI 工具，从找方向到拿 offer。"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st
from styles import inject_css, hero
from review.reviewer import (extract_text, find_roles, translate_skills, analyze_gap,
                             career_pivot, scan_industries, rewrite_resume, job_strategy, set_lang)
from i18n import t, lang_toggle, get_lang

EXAMPLE_RESUME_ZH = """张三 | 数据分析师 | 3 年经验

工作经历
● 某电商公司 · 数据分析师（2021.06 至今）
  - 负责用户增长分析，搭建核心指标体系，用 SQL 处理千万级用户行为数据
  - 主导 A/B 测试平台落地，将实验分析效率提升 40%
  - 用 Tableau 搭建经营分析看板，覆盖 5 个业务线，周报自动化

● 某咨询公司 · 数据分析实习生（2020.07 - 2020.12）
  - 协助完成 10+ 份行业研究报告，负责数据清洗与图表制作

项目经历
● 用户流失预测：用逻辑回归 + XGBoost 建模预测用户流失，AUC 0.85，支撑运营召回策略
● 电商销售分析：用 Pandas 清洗 50 万条订单数据，产出 RFM 分层与复购分析报告

技能
● 硬技能：Python、SQL、Excel、Pandas、NumPy、Tableau、机器学习
● 软技能：跨部门协作、项目推动、数据汇报

教育
本科 · 统计学
"""

EXAMPLE_RESUME_EN = """John Doe | Data Analyst | 3 years experience

Work Experience
● E-commerce company · Data Analyst (2021.06 - present)
  - Led user growth analytics, built the core metric system, processed 10M+ user behavior records with SQL
  - Led A/B testing platform rollout, improving experiment analysis efficiency by 40%
  - Built Tableau business dashboards covering 5 business lines, automated weekly reports

● Consulting firm · Data Analyst Intern (2020.07 - 2020.12)
  - Contributed to 10+ industry research reports, handled data cleaning and charting

Projects
● User churn prediction: logistic regression + XGBoost, AUC 0.85, supporting retention campaigns
● E-commerce sales analysis: cleaned 500K orders with Pandas, produced RFM segmentation and repurchase report

Skills
● Technical: Python, SQL, Excel, Pandas, NumPy, Tableau, machine learning
● Soft skills: cross-team collaboration, project delivery, data storytelling

Education
B.S. in Statistics
"""

st.set_page_config(page_title="给个工作吧 · 求职工具箱", page_icon="🧰", layout="wide")
inject_css()
lang_toggle()
set_lang(get_lang())  # 让 AI 结果跟随界面语言

st.page_link("app.py", label=t("back_home"))

hero(t("tool_title"), t("tool_subtitle"))

# —— 侧边栏：API 配置 ——
with st.sidebar:
    st.caption(t("tool_steps"))
    st.header(t("api_header"))
    api_key = st.text_input(t("api_key_label"), type="password", help=t("api_key_help"))
    model = st.text_input(t("api_model_label"), value="deepseek-chat", help=t("api_model_help"))
    st.caption(t("api_hint"))


def _ready(resume_text):
    """运行前统一检查。"""
    if not resume_text.strip():
        st.error(t("need_resume"))
        return False
    if not api_key:
        st.error(t("need_key"))
        return False
    return True


def _status_icon(status):
    """把 AI 返回的满足状态（中/英）映射成图标。"""
    s = str(status).strip().lower()
    if "partial" in s or "部分" in s:
        return "🟡"
    if "met" in s or "满足" in s or "satisf" in s:
        return "✅"
    return "🔴"


st.divider()

# —— 上传简历（所有工具共用） ——
st.subheader(t("upload_header"))
if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = ""

f = st.file_uploader(t("uploader_label"), type=["txt", "md", "docx", "pdf"])
if f is not None:
    if st.session_state.get("_last_file") != f.name:
        try:
            st.session_state["resume_text"] = extract_text(f)
            st.session_state["_last_file"] = f.name
        except Exception as e:
            st.error(t("run_fail", e=e))

if st.button(t("fill_example"), key="fill_example"):
    st.session_state["resume_text"] = EXAMPLE_RESUME_ZH if get_lang() == "zh" else EXAMPLE_RESUME_EN
    st.session_state["_last_file"] = None

resume_text = st.text_area(t("resume_label"), height=260, key="resume_text",
                           placeholder=t("resume_placeholder"))

st.divider()

# —— 7 个工具（tab 切换） ——
tabs = st.tabs([t("tab1"), t("tab2"), t("tab3"), t("tab4"), t("tab5"), t("tab6"), t("tab7")])

# ---- 工具 1：隐藏角色搜索器 ----
with tabs[0]:
    st.caption(t("t1_cap"))
    if st.button(t("t1_btn"), type="primary", key="run_roles", use_container_width=True):
        if _ready(resume_text):
            with st.spinner(t("t1_spin")):
                try:
                    st.session_state["roles"] = find_roles(api_key, resume_text, model)
                except Exception as e:
                    st.error(t("run_fail", e=e))
    r = st.session_state.get("roles")
    if r:
        roles = r.get("roles", [])
        rows = [{t("col_title"): x.get("title"), t("col_industry"): x.get("industry"),
                 t("col_fit"): x.get("fit_score"), t("col_salary"): x.get("salary_range"),
                 t("col_demand"): x.get("demand"), t("col_difficulty"): x.get("entry_difficulty")}
                for x in roles]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        for x in roles:
            with st.expander(f"{x.get('title')} · {x.get('industry')} · {t('col_fit')} {x.get('fit_score')}"):
                st.write(x.get("fit_reason"))

# ---- 工具 2：可转移技能翻译器 ----
with tabs[1]:
    st.caption(t("t2_cap"))
    if st.button(t("t2_btn"), type="primary", key="run_skills", use_container_width=True):
        if _ready(resume_text):
            with st.spinner(t("t2_spin")):
                try:
                    st.session_state["skills"] = translate_skills(api_key, resume_text, model)
                except Exception as e:
                    st.error(t("run_fail", e=e))
    r = st.session_state.get("skills")
    if r:
        for s in r.get("skills", []):
            with st.expander(f"{s.get('skill')} · {t('match')} {s.get('match_level')}"):
                st.markdown(f"**{t('why_valuable')}**：{s.get('why_valuable')}")
                st.markdown(f"**{t('related_roles')}**：{'、'.join(s.get('related_roles', []))}")
                st.markdown(f"**{t('evidence')}**：{s.get('evidence')}")

# ---- 工具 3：资格差距分析器 ----
with tabs[2]:
    st.caption(t("t3_cap"))
    jd_text = st.text_area(t("jd_label"), height=180, key="gap_jd", placeholder=t("jd_placeholder"))
    if st.button(t("t3_btn"), type="primary", key="run_gap", use_container_width=True):
        if _ready(resume_text) and jd_text.strip():
            with st.spinner(t("t3_spin")):
                try:
                    st.session_state["gap"] = analyze_gap(api_key, resume_text, jd_text, model)
                except Exception as e:
                    st.error(t("run_fail", e=e))
        elif not jd_text.strip():
            st.error(t("need_jd"))
    r = st.session_state.get("gap")
    if r:
        for req in r.get("requirements", []):
            status = req.get("status")
            icon = _status_icon(status)
            with st.expander(f"{icon} {req.get('requirement')}（{status}）"):
                if req.get("evidence"):
                    st.markdown(f"**{t('evidence_label')}**：{req.get('evidence')}")
                if req.get("gap_action"):
                    st.markdown(f"**{t('gap_action')}**：{req.get('gap_action')}")
        st.info(r.get("summary"))

# ---- 工具 4：职业支点地图 ----
with tabs[3]:
    st.caption(t("t4_cap"))
    if st.button(t("t4_btn"), type="primary", key="run_pivot", use_container_width=True):
        if _ready(resume_text):
            with st.spinner(t("t4_spin")):
                try:
                    st.session_state["pivot"] = career_pivot(api_key, resume_text, model)
                except Exception as e:
                    st.error(t("run_fail", e=e))
    r = st.session_state.get("pivot")
    if r:
        for route in r.get("routes", []):
            with st.expander(f"{route.get('route_name')} → {route.get('entry_role')}"):
                st.markdown(f"**{t('entry_role')}**：{route.get('entry_role')}")
                st.markdown(f"**{t('skill_gaps')}**：{'、'.join(route.get('skill_gaps', []))}")
                st.markdown(f"**{t('salary_range')}**：{route.get('salary_range')}")
                st.markdown(f"**{t('plan30')}**：")
                for i, step in enumerate(route.get("plan_30days", []), 1):
                    st.markdown(f"{i}. {step}")

# ---- 工具 5：最佳匹配行业扫描器 ----
with tabs[4]:
    st.caption(t("t5_cap"))
    if st.button(t("t5_btn"), type="primary", key="run_industries", use_container_width=True):
        if _ready(resume_text):
            with st.spinner(t("t5_spin")):
                try:
                    st.session_state["industries"] = scan_industries(api_key, resume_text, model)
                except Exception as e:
                    st.error(t("run_fail", e=e))
    r = st.session_state.get("industries")
    if r:
        rows = [{t("col_industry"): x.get("industry"), t("col_demand"): x.get("demand"),
                 t("col_salary"): x.get("salary"), t("col_growth"): x.get("growth"),
                 t("col_difficulty"): x.get("entry_difficulty")}
                for x in r.get("industries", [])]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        for x in r.get("industries", []):
            with st.expander(x.get("industry")):
                st.write(x.get("fit_reason"))

# ---- 工具 6：简历定位重写工具 ----
with tabs[5]:
    st.caption(t("t6_cap"))
    target6 = st.text_input(t("target_label"), key="rewrite_target", placeholder=t("target_placeholder"))
    if st.button(t("t6_btn"), type="primary", key="run_rewrite", use_container_width=True):
        if _ready(resume_text) and target6.strip():
            with st.spinner(t("t6_spin")):
                try:
                    st.session_state["rewritten"] = rewrite_resume(api_key, resume_text, target6, model)
                except Exception as e:
                    st.error(t("run_fail", e=e))
        elif not target6.strip():
            st.error(t("need_target"))
    r = st.session_state.get("rewritten")
    if r:
        st.markdown(f"**{t('rewritten_title')}**")
        st.download_button(t("download"), r.get("rewritten_resume", ""),
                           file_name="rewritten_resume.txt", mime="text/plain")
        st.text_area(t("rewritten_area"), value=r.get("rewritten_resume", ""), height=400, key="rewritten_out")
        st.markdown(f"**{t('changes_title')}**")
        for ch in r.get("changes", []):
            st.markdown(f"**{t('before')}**：{ch.get('before')}")
            st.markdown(f"**{t('after')}**：{ch.get('after')}")
            st.markdown(f"*{t('reason')}*：{ch.get('reason')}")
            st.markdown("---")

# ---- 工具 7：机会搜索策略 ----
with tabs[6]:
    st.caption(t("t7_cap"))
    target7 = st.text_input(t("target_label"), key="strategy_target", placeholder=t("target_placeholder"))
    if st.button(t("t7_btn"), type="primary", key="run_strategy", use_container_width=True):
        if _ready(resume_text) and target7.strip():
            with st.spinner(t("t7_spin")):
                try:
                    st.session_state["strategy"] = job_strategy(api_key, resume_text, target7, model)
                except Exception as e:
                    st.error(t("run_fail", e=e))
        elif not target7.strip():
            st.error(t("need_target"))
    r = st.session_state.get("strategy")
    if r:
        st.markdown(f"**{t('keywords_title')}**")
        st.markdown("、".join(r.get("keywords", [])))
        st.markdown(f"**{t('companies_title')}**")
        for c in r.get("companies", []):
            st.markdown(f"- **{c.get('name')}**：{c.get('note')}")
        st.markdown(f"**{t('outreach_title')}**")
        for a in r.get("outreach", []):
            st.markdown(f"- {a}")
        st.markdown(f"**{t('weekly_title')}**")
        for wk in r.get("weekly_plan", []):
            with st.expander(t("week_focus", week=wk.get("week"), focus=wk.get("focus"))):
                for a in wk.get("actions", []):
                    st.markdown(f"- {a}")
                st.markdown(f"**{t('review')}**：{wk.get('review')}")

# —— 底部：和我直接问 AI 有什么区别 ——
st.divider()
st.markdown(
    f"""
    <div class="why-card">
        <div class="why-title">{t('why_title')}</div>
        <div class="why-body">{t('why_body')}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
