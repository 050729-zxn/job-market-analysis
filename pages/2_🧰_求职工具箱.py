# -*- coding: utf-8 -*-
"""求职工具箱（多页应用第 2 页）：7 个 AI 工具，从找方向到拿 offer。"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import streamlit as st
from styles import inject_css, hero
from review.reviewer import (extract_text, find_roles, translate_skills, analyze_gap,
                             career_pivot, scan_industries, rewrite_resume, job_strategy)

EXAMPLE_RESUME = """张三 | 数据分析师 | 3 年经验

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

st.set_page_config(page_title="给个工作吧 · 求职工具箱", page_icon="🧰", layout="wide")
inject_css()

st.page_link("app.py", label="← 返回主页")

hero(
    "求职工具箱",
    "7 个 AI 工具：找方向、提技能、补差距、规划路线、扫行业、重写简历、排 30 天计划",
)

# —— 侧边栏：API 配置 ——
with st.sidebar:
    st.caption("① 填 Key → ② 传简历 → ③ 选工具 → ④ 运行")
    st.header("API 配置")
    api_key = st.text_input("DeepSeek API Key", type="password",
                            help="只存当前会话内存，不写入磁盘或代码")
    model = st.text_input("模型名", value="deepseek-chat",
                          help="如 deepseek-chat / deepseek-reasoner")
    st.caption("Key 不会保存，刷新页面后需重新填。")


def _ready(resume_text):
    """运行前统一检查。"""
    if not resume_text.strip():
        st.error("请先上传或粘贴简历")
        return False
    if not api_key:
        st.error("请先在左侧填写自己的 DeepSeek API Key")
        return False
    return True


st.divider()

# —— 上传简历（所有工具共用） ——
st.subheader("上传简历")
if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = ""

f = st.file_uploader("上传简历文件（txt / md / docx / pdf）", type=["txt", "md", "docx", "pdf"])
if f is not None:
    if st.session_state.get("_last_file") != f.name:
        try:
            st.session_state["resume_text"] = extract_text(f)
            st.session_state["_last_file"] = f.name
        except Exception as e:
            st.error(f"解析失败：{e}")

if st.button("没有简历？填入示例简历试试", key="fill_example"):
    st.session_state["resume_text"] = EXAMPLE_RESUME
    st.session_state["_last_file"] = None

resume_text = st.text_area("简历内容", height=260, key="resume_text",
                           placeholder="上传后自动填入，也可以直接把简历文本粘贴到这里……")

st.divider()

# —— 7 个工具（tab 切换） ——
tabs = st.tabs([
    "① 隐藏角色搜索器",
    "② 可转移技能翻译器",
    "③ 资格差距分析器",
    "④ 职业支点地图",
    "⑤ 最佳匹配行业扫描器",
    "⑥ 简历定位重写工具",
    "⑦ 机会搜索策略",
])

# ---- 工具 1：隐藏角色搜索器 ----
with tabs[0]:
    st.caption("分析简历，识别 15 个和经验匹配的跨行业职位，按契合度、薪资、需求、准入难度分类。")
    if st.button("🔍 找 15 个隐藏岗位", type="primary", key="run_roles", use_container_width=True):
        if _ready(resume_text):
            with st.spinner("正在识别隐藏岗位，约需 1 分钟……"):
                try:
                    st.session_state["roles"] = find_roles(api_key, resume_text, model)
                except Exception as e:
                    st.error(f"分析失败：{e}")
    r = st.session_state.get("roles")
    if r:
        roles = r.get("roles", [])
        rows = [{"职位": x.get("title"), "行业": x.get("industry"), "契合度": x.get("fit_score"),
                 "薪资范围": x.get("salary_range"), "需求": x.get("demand"),
                 "准入难度": x.get("entry_difficulty")} for x in roles]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        for x in roles:
            with st.expander(f"{x.get('title')} · {x.get('industry')} · 契合度 {x.get('fit_score')}"):
                st.write(x.get("fit_reason"))

# ---- 工具 2：可转移技能翻译器 ----
with tabs[1]:
    st.caption("提取简历里雇主看重的技能，关联对应行业岗位，解释经验匹配度。")
    if st.button("🔄 提取可迁移技能", type="primary", key="run_skills", use_container_width=True):
        if _ready(resume_text):
            with st.spinner("正在提取可迁移技能，约需 1 分钟……"):
                try:
                    st.session_state["skills"] = translate_skills(api_key, resume_text, model)
                except Exception as e:
                    st.error(f"分析失败：{e}")
    r = st.session_state.get("skills")
    if r:
        for s in r.get("skills", []):
            with st.expander(f"{s.get('skill')} · 匹配度 {s.get('match_level')}"):
                st.markdown(f"**雇主为何看重**：{s.get('why_valuable')}")
                st.markdown(f"**关联岗位/行业**：{'、'.join(s.get('related_roles', []))}")
                st.markdown(f"**简历证据**：{s.get('evidence')}")

# ---- 工具 3：资格差距分析器 ----
with tabs[2]:
    st.caption("对比简历和目标岗位 JD，标注已满足 / 部分满足 / 缺失项，给补差距的最快方案。")
    jd_text = st.text_area("目标岗位 JD", height=180, key="gap_jd",
                           placeholder="把招聘网站的职位描述粘贴到这里……")
    if st.button("📏 分析资格差距", type="primary", key="run_gap", use_container_width=True):
        if _ready(resume_text) and jd_text.strip():
            with st.spinner("正在逐条对比 JD 要求，约需 1 分钟……"):
                try:
                    st.session_state["gap"] = analyze_gap(api_key, resume_text, jd_text, model)
                except Exception as e:
                    st.error(f"分析失败：{e}")
        elif not jd_text.strip():
            st.error("请先粘贴目标岗位 JD")
    r = st.session_state.get("gap")
    if r:
        for req in r.get("requirements", []):
            status = req.get("status")
            icon = {"已满足": "✅", "部分满足": "🟡", "缺失": "🔴"}.get(status, "•")
            with st.expander(f"{icon} {req.get('requirement')}（{status}）"):
                if req.get("evidence"):
                    st.markdown(f"**证据/说明**：{req.get('evidence')}")
                if req.get("gap_action"):
                    st.markdown(f"**补差距方案**：{req.get('gap_action')}")
        st.info(r.get("summary"))

# ---- 工具 4：职业支点地图 ----
with tabs[3]:
    st.caption("生成 5 条职业转型路线，含初始岗位、技能缺口、薪资范围、30 天过渡计划。")
    if st.button("🗺️ 生成职业转型路线", type="primary", key="run_pivot", use_container_width=True):
        if _ready(resume_text):
            with st.spinner("正在规划转型路线，约需 1 分钟……"):
                try:
                    st.session_state["pivot"] = career_pivot(api_key, resume_text, model)
                except Exception as e:
                    st.error(f"分析失败：{e}")
    r = st.session_state.get("pivot")
    if r:
        for route in r.get("routes", []):
            with st.expander(f"{route.get('route_name')} → {route.get('entry_role')}"):
                st.markdown(f"**初始岗位**：{route.get('entry_role')}")
                st.markdown(f"**技能缺口**：{'、'.join(route.get('skill_gaps', []))}")
                st.markdown(f"**薪资范围**：{route.get('salary_range')}")
                st.markdown("**30 天过渡计划**：")
                for i, step in enumerate(route.get("plan_30days", []), 1):
                    st.markdown(f"{i}. {step}")

# ---- 工具 5：最佳匹配行业扫描器 ----
with tabs[4]:
    st.caption("识别 10 个适配你技能的行业，按招聘需求、薪酬、成长空间、准入难度排序。")
    if st.button("🏭 扫描匹配行业", type="primary", key="run_industries", use_container_width=True):
        if _ready(resume_text):
            with st.spinner("正在扫描匹配行业，约需 1 分钟……"):
                try:
                    st.session_state["industries"] = scan_industries(api_key, resume_text, model)
                except Exception as e:
                    st.error(f"分析失败：{e}")
    r = st.session_state.get("industries")
    if r:
        rows = [{"行业": x.get("industry"), "招聘需求": x.get("demand"), "薪酬": x.get("salary"),
                 "成长空间": x.get("growth"), "准入难度": x.get("entry_difficulty")}
                for x in r.get("industries", [])]
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        for x in r.get("industries", []):
            with st.expander(x.get("industry")):
                st.write(x.get("fit_reason"))

# ---- 工具 6：简历定位重写工具 ----
with tabs[5]:
    st.caption("针对目标方向重写简历，突出相关成就、可量化成果和行业术语，不造假。")
    target6 = st.text_input("目标方向", key="rewrite_target",
                            placeholder="如：数据产品经理 / 游戏数据分析师")
    if st.button("✍️ 重写我的简历", type="primary", key="run_rewrite", use_container_width=True):
        if _ready(resume_text) and target6.strip():
            with st.spinner("正在重写简历，约需 1 分钟……"):
                try:
                    st.session_state["rewritten"] = rewrite_resume(api_key, resume_text, target6, model)
                except Exception as e:
                    st.error(f"重写失败：{e}")
        elif not target6.strip():
            st.error("请先填写目标方向")
    r = st.session_state.get("rewritten")
    if r:
        st.markdown("**重写后的简历**")
        st.download_button("下载重写后的简历", r.get("rewritten_resume", ""),
                           file_name="rewritten_resume.txt", mime="text/plain")
        st.text_area("重写结果", value=r.get("rewritten_resume", ""), height=400, key="rewritten_out")
        st.markdown("**关键改动**")
        for ch in r.get("changes", []):
            st.markdown(f"**原文**：{ch.get('before')}")
            st.markdown(f"**改后**：{ch.get('after')}")
            st.markdown(f"*为什么*：{ch.get('reason')}")
            st.markdown("---")

# ---- 工具 7：机会搜索策略 ----
with tabs[6]:
    st.caption("制定 30 天求职计划：关键词、企业清单、拓展动作、每周复盘节点。")
    target7 = st.text_input("目标方向", key="strategy_target",
                            placeholder="如：商业分析师 / 风控策略")
    if st.button("📅 制定 30 天求职计划", type="primary", key="run_strategy", use_container_width=True):
        if _ready(resume_text) and target7.strip():
            with st.spinner("正在制定求职计划，约需 1 分钟……"):
                try:
                    st.session_state["strategy"] = job_strategy(api_key, resume_text, target7, model)
                except Exception as e:
                    st.error(f"生成失败：{e}")
        elif not target7.strip():
            st.error("请先填写目标方向")
    r = st.session_state.get("strategy")
    if r:
        st.markdown("**搜索关键词**")
        st.markdown("、".join(r.get("keywords", [])))
        st.markdown("**目标企业清单**")
        for c in r.get("companies", []):
            st.markdown(f"- **{c.get('name')}**：{c.get('note')}")
        st.markdown("**拓展动作**")
        for a in r.get("outreach", []):
            st.markdown(f"- {a}")
        st.markdown("**每周复盘节点**")
        for wk in r.get("weekly_plan", []):
            with st.expander(f"第 {wk.get('week')} 周：{wk.get('focus')}"):
                for a in wk.get("actions", []):
                    st.markdown(f"- {a}")
                st.markdown(f"**复盘**：{wk.get('review')}")

# —— 底部：和我直接问 AI 有什么区别 ——
st.divider()
st.markdown(
    """
    <div class="why-card">
        <div class="why-title">和我直接问 AI 有什么区别？</div>
        <div class="why-body">
            直接问 AI，你得自己一遍遍追问、自己梳理，容易漏掉关键环节。这里把求职拆成
            <b>7 个专职工具</b>——找方向、提技能、补差距、规划路线、扫行业、重写简历、排计划——
            每个工具专注一件事，产出结构化结果，照着做就行。
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
