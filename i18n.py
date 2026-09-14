# -*- coding: utf-8 -*-
"""中英双语：文案字典 + 语言切换。"""
import streamlit as st

from catalog_i18n import EDU_EN, EXP_EN, IND_EN, IND_ZH

T = {
    # —— 通用 ——
    "back_home": {"zh": "← 返回主页", "en": "← Back to Home"},
    "no_data": {"zh": "当前筛选条件下没有数据，请调整上方筛选。", "en": "No data under the current filters. Please adjust them above."},
    "jobs_count": {"zh": "{n} 条岗位", "en": "{n} jobs"},
    "view_raw": {"zh": "查看原始数据", "en": "View raw data"},

    # —— 国家 / 薪资口径 ——
    "c_cn": {"zh": "中国", "en": "China"},
    "c_us": {"zh": "美国", "en": "United States"},
    "c_both": {"zh": "对比", "en": "Compare"},
    "country_scope": {"zh": "数据范围", "en": "Data scope"},
    "note_cn_sample": {"zh": "中国样本约 300 条（一线城市），美国样本约 5553 条（全美）。", "en": "China sample ≈300 jobs (a tier-1 city); US sample ≈5,553 jobs (nationwide)."},

    # —— 首页 ——
    "home_subtitle": {
        "zh": "海投没回音？先看清市场在招什么、缺什么技能，再把简历改到位。",
        "en": "No replies to your applications? First see what the market is hiring and which skills it lacks, then fix your resume.",
    },
    "home_cta": {"zh": "立即看行情 →", "en": "See the market →"},
    "stat_jobs": {"zh": "真实岗位", "en": "Real jobs"},
    "stat_industries": {"zh": "覆盖行业", "en": "Industries"},
    "stat_skills": {"zh": "技能词", "en": "Skills"},
    "stat_ai": {"zh": "AI 工具", "en": "AI tools"},
    "home_how": {"zh": "这个站怎么帮你", "en": "How this site helps you"},
    "vp1_title": {"zh": "先看清行情", "en": "See the market first"},
    "vp1_desc": {"zh": "哪些行业在招人、给多少钱、要什么学历经验，图表一目了然。", "en": "Which industries are hiring, what they pay, and what education/experience they require — clear at a glance."},
    "vp2_title": {"zh": "再找准技能", "en": "Find the right skills"},
    "vp2_desc": {"zh": "20 项核心技能出现率排名，别在没人要的技能上花时间。", "en": "Ranking of 20 core skills by demand — don't waste time on skills nobody wants."},
    "vp3_title": {"zh": "最后改好简历", "en": "Then fix your resume"},
    "vp3_desc": {"zh": "7 个 AI 工具从找方向到排计划，把简历改成招聘方想看到的样子。", "en": "7 AI tools take you from finding a direction to planning, reshaping your resume into what recruiters want."},
    "home_features": {"zh": "功能入口", "en": "Features"},
    "card1_title": {"zh": "招聘市场分析", "en": "Market Analysis"},
    "card1_desc": {"zh": "薪资、行业、学历、经验全景，点击图表联动筛选。", "en": "Salary, industry, education, experience at a glance, with click-to-filter."},
    "card1_btn": {"zh": "查看行情", "en": "View market"},
    "card2_title": {"zh": "求职工具箱", "en": "Job Toolkit"},
    "card2_desc": {"zh": "7 个 AI 工具：找方向、提技能、补差距、重写简历、排计划。", "en": "7 AI tools: find a direction, build skills, close gaps, rewrite your resume, plan."},
    "card2_btn": {"zh": "打开工具箱", "en": "Open toolkit"},
    "card3_title": {"zh": "技能排行", "en": "Skill Ranking"},
    "card3_desc": {"zh": "最吃香技能总排名，以及各行业、各技能的出现率。", "en": "Overall ranking of in-demand skills, plus prevalence by industry and skill."},
    "card3_btn": {"zh": "查看技能", "en": "View skills"},

    # —— 市场分析页 ——
    "market_title": {"zh": "招聘市场分析", "en": "Job Market Analysis"},
    "market_subtitle": {"zh": "全球数据岗的招聘全景：薪资、行业、学历、经验", "en": "The full picture of data jobs: salary, industry, education, experience"},
    "market_hint": {"zh": "图表可悬停查看数值、框选缩放；点击「行业对比」中的柱子可联动筛选其他图表。", "en": "Hover for values and box-zoom. In single-country view, click a bar in \"Industry comparison\" to filter the other charts."},
    "f_edu": {"zh": "学历", "en": "Education"},
    "f_exp": {"zh": "经验", "en": "Experience"},
    "f_ind": {"zh": "行业", "en": "Industry"},
    "overview": {"zh": "概览（当前 {n} 条岗位）", "en": "Overview ({n} jobs now)"},
    "linked_info": {"zh": "已联动筛选：**{ind}** 行业。下方图表仅显示该行业，点击「清除联动」恢复全部。", "en": "Linked filter: **{ind}** industry. Charts below show only this industry — click \"Clear link\" to reset."},
    "clear_link": {"zh": "清除联动", "en": "Clear link"},
    "metric_jobs": {"zh": "有效岗位数", "en": "Valid jobs"},
    "metric_top_skill": {"zh": "最吃香技能", "en": "Top skill"},
    "sec_salary_dist": {"zh": "薪资分布", "en": "Salary distribution"},
    "axis_jobs": {"zh": "岗位数", "en": "Jobs"},
    "cap_salary_dist": {"zh": "横轴为{unit}，纵轴为该薪资区间的岗位数量。悬停可看每个区间的具体数量。", "en": "X axis = {unit}, Y axis = number of jobs per salary bucket. Hover for exact counts."},
    "sec_industry": {"zh": "行业对比", "en": "Industry comparison"},
    "ind_count_title": {"zh": "各行业岗位数量 · 点击可联动", "en": "Jobs by industry · click to link"},
    "ind_salary_title": {"zh": "各行业平均{unit}", "en": "Average {unit} by industry"},
    "cap_click": {"zh": "点击某根柱子，其他图表会联动筛选到该行业。", "en": "Click a bar to filter the other charts to that industry."},
    "cap_ind_salary": {"zh": "反映各行业的薪资水平差异。", "en": "Shows salary differences across industries."},
    "sec_edu_exp": {"zh": "学历与经验", "en": "Education & Experience"},
    "edu_dist_title": {"zh": "学历要求分布", "en": "Education distribution"},
    "cap_edu": {"zh": "各学历要求的岗位占比。", "en": "Share of jobs by education requirement."},
    "exp_dist_title": {"zh": "经验要求分布", "en": "Experience distribution"},
    "cap_exp": {"zh": "反映对不同工作年限的需求。", "en": "Shows demand for different experience levels."},
    "sec_deepdive": {"zh": "单个行业深挖", "en": "Industry deep dive"},
    "pick_ind": {"zh": "选择一个行业查看详情", "en": "Pick an industry to explore"},
    "metric_jobs_short": {"zh": "岗位数（条）", "en": "Jobs"},
    "metric_main_edu": {"zh": "主要学历要求", "en": "Main education"},
    "cap_deepdive": {"zh": "「{ind}」行业共 {n} 条岗位。{unit_cap}；技能要求请到「技能排行」页查看。", "en": "\"{ind}\" has {n} jobs. {unit_cap}; see the Skill Ranking page for skill requirements."},

    # —— 技能排行页 ——
    "skill_title": {"zh": "技能排行", "en": "Skill Ranking"},
    "skill_subtitle": {"zh": "全球数据岗最吃香的技能，以及各行业对技能的不同要求", "en": "The most in-demand skills for data jobs, and how requirements differ by industry"},
    "skill_hint": {"zh": "出现次数 = 技能在岗位描述中被提及的岗位数；出现率 = 该技能出现次数 ÷ 本行业岗位数。", "en": "Count = jobs whose description mentions the skill; prevalence = count ÷ jobs in that industry."},
    "sec_total_rank": {"zh": "技能出现次数总排名（当前 {n} 条岗位）", "en": "Overall skill count ranking ({n} jobs now)"},
    "axis_count": {"zh": "出现次数（次）", "en": "Count"},
    "cap_total_rank": {"zh": "按技能在岗位描述中出现的次数排名，出现越多代表越被企业看重。", "en": "Ranked by how often the skill appears in job descriptions — the more, the more valued."},
    "sec_category": {"zh": "技能类别分布", "en": "Skill category distribution"},
    "axis_cat_count": {"zh": "出现次数合计（次）", "en": "Total count"},
    "cap_category": {"zh": "同一类别下所有技能的出现次数合计，反映企业最看重的能力方向。", "en": "Total count across all skills in a category — shows which capability area employers value most."},
    "sec_industry_rank": {"zh": "各行业技能排行榜（出现率）", "en": "Skill ranking by industry (prevalence)"},
    "cap_industry_rank": {"zh": "出现率 = 该技能在本行业岗位描述中出现次数 ÷ 本行业岗位数。同一技能在不同行业按各自行业独立计算。", "en": "Prevalence = count in this industry ÷ jobs in this industry, computed per industry."},
    "pick_ind_rank": {"zh": "选择行业查看技能排行榜", "en": "Pick an industry to see its skill ranking"},
    "col_skill": {"zh": "技能", "en": "Skill"},
    "col_cat": {"zh": "类别", "en": "Category"},
    "col_count": {"zh": "出现次数", "en": "Count"},
    "col_rate": {"zh": "出现率(%)", "en": "Prevalence (%)"},
    "cap_top15": {"zh": "「{ind}」行业技能出现率 Top 15。", "en": "Top 15 skills by prevalence in \"{ind}\"."},
    "sec_skill_industry": {"zh": "某个技能，在哪些行业吃香", "en": "Where a skill is in demand"},
    "cap_skill_industry": {"zh": "选一个技能，看它在各行业的出现率排名——帮你判断自己会的技能该投向哪个行业。", "en": "Pick a skill to see its prevalence across industries — helps you decide where to aim your skills."},
    "pick_skill": {"zh": "选择一个技能", "en": "Pick a skill"},
    "cap_skill_by_ind": {"zh": "「{skill}」在各行业的出现率，越高代表该行业越需要这项技能。", "en": "Prevalence of \"{skill}\" by industry — higher means the industry needs it more."},
    "view_full_table": {"zh": "查看完整排名表", "en": "View full ranking table"},

    # —— 工具箱页 ——
    "tool_title": {"zh": "求职工具箱", "en": "Job Toolkit"},
    "tool_subtitle": {"zh": "7 个 AI 工具，把简历从「没人看」改成「被邀面」。", "en": "7 AI tools to turn your resume from \"ignored\" into \"interviewed\"."},
    "tool_steps": {"zh": "① 填 Key → ② 传简历 → ③ 选工具 → ④ 运行", "en": "① Fill key → ② Upload resume → ③ Pick a tool → ④ Run"},
    "api_header": {"zh": "API 配置", "en": "API setup"},
    "api_key_label": {"zh": "DeepSeek API Key", "en": "DeepSeek API Key"},
    "api_model_label": {"zh": "模型名", "en": "Model name"},
    "api_hint": {"zh": "Key 不会保存，刷新页面后需重新填。", "en": "The key is not saved; re-enter after refreshing."},
    "upload_header": {"zh": "上传简历", "en": "Upload resume"},
    "need_resume": {"zh": "请先上传或粘贴简历", "en": "Please upload or paste your resume first."},
    "need_key": {"zh": "请先在左侧填写自己的 DeepSeek API Key", "en": "Please enter your DeepSeek API Key on the left first."},
    "parse_fail": {"zh": "解析失败：{e}", "en": "Parse failed: {e}"},
    "fill_example": {"zh": "没有简历？填入示例简历试试", "en": "No resume? Try the sample"},
    "resume_label": {"zh": "简历内容", "en": "Resume content"},
    "tool_tab_intro": {"zh": "选择左侧工具，在下方运行。", "en": "Pick a tool on the left, then run it below."},
    "run_fail": {"zh": "运行失败：{e}", "en": "Failed: {e}"},
    "api_key_help": {"zh": "只存当前会话内存，不写入磁盘或代码", "en": "Stored only in this session's memory, never written to disk or code"},
    "api_model_help": {"zh": "如 deepseek-chat / deepseek-reasoner", "en": "e.g. deepseek-chat / deepseek-reasoner"},
    "uploader_label": {"zh": "上传简历文件（txt / md / docx / pdf）", "en": "Upload resume (txt / md / docx / pdf)"},
    "resume_placeholder": {"zh": "上传后自动填入，也可以直接把简历文本粘贴到这里……", "en": "Auto-filled after upload, or paste your resume text here..."},

    "tab1": {"zh": "① 隐藏角色搜索器", "en": "① Hidden Role Finder"},
    "tab2": {"zh": "② 可转移技能翻译器", "en": "② Transferable Skill Translator"},
    "tab3": {"zh": "③ 资格差距分析器", "en": "③ Gap Analyzer"},
    "tab4": {"zh": "④ 职业支点地图", "en": "④ Career Pivot Map"},
    "tab5": {"zh": "⑤ 最佳匹配行业扫描器", "en": "⑤ Industry Match Scanner"},
    "tab6": {"zh": "⑥ 简历定位重写工具", "en": "⑥ Resume Rewriter"},
    "tab7": {"zh": "⑦ 机会搜索策略", "en": "⑦ Job Search Strategy"},

    "t1_cap": {"zh": "分析简历，识别 15 个和经验匹配的跨行业职位，按契合度、薪资、需求、准入难度分类。", "en": "Analyze your resume and find 15 cross-industry roles that match your experience, ranked by fit, salary, demand, and entry difficulty."},
    "t1_btn": {"zh": "🔍 找 15 个隐藏岗位", "en": "🔍 Find 15 hidden roles"},
    "t1_spin": {"zh": "正在识别隐藏岗位，约需 1 分钟……", "en": "Finding hidden roles, ~1 minute..."},
    "col_title": {"zh": "职位", "en": "Title"},
    "col_industry": {"zh": "行业", "en": "Industry"},
    "col_fit": {"zh": "契合度", "en": "Fit"},
    "col_salary": {"zh": "薪资范围", "en": "Salary range"},
    "col_demand": {"zh": "需求", "en": "Demand"},
    "col_difficulty": {"zh": "准入难度", "en": "Entry difficulty"},

    "t2_cap": {"zh": "提取简历里雇主看重的技能，关联对应行业岗位，解释经验匹配度。", "en": "Extract the skills employers value, link them to roles/industries, and explain the match."},
    "t2_btn": {"zh": "🔄 提取可迁移技能", "en": "🔄 Extract transferable skills"},
    "t2_spin": {"zh": "正在提取可迁移技能，约需 1 分钟……", "en": "Extracting transferable skills, ~1 minute..."},
    "why_valuable": {"zh": "雇主为何看重", "en": "Why employers value it"},
    "related_roles": {"zh": "关联岗位/行业", "en": "Related roles/industries"},
    "evidence": {"zh": "简历证据", "en": "Resume evidence"},
    "match": {"zh": "匹配度", "en": "Match"},

    "t3_cap": {"zh": "对比简历和目标岗位 JD，标注已满足 / 部分满足 / 缺失项，给补差距的最快方案。", "en": "Compare your resume against a target JD, mark met / partially met / missing items, and give the fastest way to close gaps."},
    "jd_label": {"zh": "目标岗位 JD", "en": "Target JD"},
    "jd_placeholder": {"zh": "把招聘网站的职位描述粘贴到这里……", "en": "Paste the job description here..."},
    "t3_btn": {"zh": "📏 分析资格差距", "en": "📏 Analyze the gap"},
    "t3_spin": {"zh": "正在逐条对比 JD 要求，约需 1 分钟……", "en": "Comparing against the JD, ~1 minute..."},
    "need_jd": {"zh": "请先粘贴目标岗位 JD", "en": "Please paste the target JD first."},
    "evidence_label": {"zh": "证据/说明", "en": "Evidence / note"},
    "gap_action": {"zh": "补差距方案", "en": "How to close the gap"},

    "t4_cap": {"zh": "生成 5 条职业转型路线，含初始岗位、技能缺口、薪资范围、30 天过渡计划。", "en": "Generate 5 career pivot routes with entry role, skill gaps, salary range, and a 30-day plan."},
    "t4_btn": {"zh": "🗺️ 生成职业转型路线", "en": "🗺️ Generate pivot routes"},
    "t4_spin": {"zh": "正在规划转型路线，约需 1 分钟……", "en": "Planning pivot routes, ~1 minute..."},
    "entry_role": {"zh": "初始岗位", "en": "Entry role"},
    "skill_gaps": {"zh": "技能缺口", "en": "Skill gaps"},
    "salary_range": {"zh": "薪资范围", "en": "Salary range"},
    "plan30": {"zh": "30 天过渡计划", "en": "30-day transition plan"},

    "t5_cap": {"zh": "识别 10 个适配你技能的行业，按招聘需求、薪酬、成长空间、准入难度排序。", "en": "Identify 10 industries that fit your skills, ranked by demand, pay, growth, and entry difficulty."},
    "t5_btn": {"zh": "🏭 扫描匹配行业", "en": "🏭 Scan matching industries"},
    "t5_spin": {"zh": "正在扫描匹配行业，约需 1 分钟……", "en": "Scanning matching industries, ~1 minute..."},
    "col_growth": {"zh": "成长空间", "en": "Growth"},

    "t6_cap": {"zh": "针对目标方向重写简历，突出相关成就、可量化成果和行业术语，不造假。", "en": "Rewrite your resume for a target direction, highlighting achievements, metrics, and industry terms — no fabrication."},
    "target_label": {"zh": "目标方向", "en": "Target direction"},
    "target_placeholder": {"zh": "如：数据产品经理 / 游戏数据分析师", "en": "e.g. Data PM / Game Data Analyst"},
    "t6_btn": {"zh": "✍️ 重写我的简历", "en": "✍️ Rewrite my resume"},
    "t6_spin": {"zh": "正在重写简历，约需 1 分钟……", "en": "Rewriting your resume, ~1 minute..."},
    "need_target": {"zh": "请先填写目标方向", "en": "Please fill in the target direction first."},
    "rewritten_title": {"zh": "重写后的简历", "en": "Rewritten resume"},
    "download": {"zh": "下载重写后的简历", "en": "Download rewritten resume"},
    "rewritten_area": {"zh": "重写结果", "en": "Result"},
    "changes_title": {"zh": "关键改动", "en": "Key changes"},
    "before": {"zh": "原文", "en": "Before"},
    "after": {"zh": "改后", "en": "After"},
    "reason": {"zh": "为什么", "en": "Why"},

    "t7_cap": {"zh": "制定 30 天求职计划：关键词、企业清单、拓展动作、每周复盘节点。", "en": "Build a 30-day job search plan: keywords, target companies, outreach, weekly checkpoints."},
    "t7_btn": {"zh": "📅 制定 30 天求职计划", "en": "📅 Build a 30-day plan"},
    "t7_spin": {"zh": "正在制定求职计划，约需 1 分钟……", "en": "Building your plan, ~1 minute..."},
    "keywords_title": {"zh": "搜索关键词", "en": "Search keywords"},
    "companies_title": {"zh": "目标企业清单", "en": "Target companies"},
    "outreach_title": {"zh": "拓展动作", "en": "Outreach"},
    "weekly_title": {"zh": "每周复盘节点", "en": "Weekly checkpoints"},
    "week_focus": {"zh": "第 {week} 周：{focus}", "en": "Week {week}: {focus}"},
    "review": {"zh": "复盘", "en": "Review"},

    "why_title": {"zh": "和我直接问 AI 有什么区别？", "en": "How is this different from asking AI directly?"},
    "why_body": {"zh": "直接问 AI，你得自己一遍遍追问、自己梳理，容易漏掉关键环节。这里把求职拆成 7 个专职工具——找方向、提技能、补差距、规划路线、扫行业、重写简历、排计划——每个工具专注一件事，产出结构化结果，照着做就行。", "en": "Asking AI directly means prompting over and over and sorting it out yourself. Here the job search is split into 7 dedicated tools — direction, skills, gaps, routes, industries, rewrite, plan — each doing one thing and producing structured results you can act on."},
}

# 薪资口径（按国家）—— 与 viz.salary_terms 配合使用
SALARY = {
    "CN": {
        "avg": {"zh": "平均月薪", "en": "Avg monthly salary"},
        "med": {"zh": "月薪中位数", "en": "Median monthly"},
        "axis": {"zh": "月薪（K）", "en": "Monthly salary (K¥)"},
        "cap": {"zh": "K = 千元/月（税前估算中值）", "en": "K = ¥K/month (pre-tax estimate)"},
        "ind_avg": {"zh": "各行业平均月薪", "en": "Avg monthly salary by industry"},
    },
    "US": {
        "avg": {"zh": "平均年薪", "en": "Avg annual salary"},
        "med": {"zh": "年薪中位数", "en": "Median annual"},
        "axis": {"zh": "年薪（K美元）", "en": "Annual salary (K$)"},
        "cap": {"zh": "K = 千美元/年（税前估算中值）", "en": "K = $K/year (pre-tax estimate)"},
        "ind_avg": {"zh": "各行业平均年薪", "en": "Avg annual salary by industry"},
    },
}


def get_lang():
    return st.session_state.get("lang", "zh")


def t(key, **kw):
    """取当前语言的文案。key 不存在时原样返回 key，便于发现漏翻。"""
    lang = get_lang()
    entry = T.get(key)
    if entry is None:
        return key
    s = entry.get(lang) or entry.get("en") or key
    return s.format(**kw) if kw else s


def cat_text(category, value):
    """分类值的当前语言显示名：category ∈ {"education", "experience", "industry"}。

    - education / experience：数据统一是中文，切英文时翻成英文。
    - industry：中文名→英文（切英文时），英文名→中文（切中文时）。
    """
    if value is None:
        return value
    lang = get_lang()
    if category in ("education", "experience"):
        if lang == "en":
            table = EDU_EN if category == "education" else EXP_EN
            return table.get(value, value)
        return value
    # industry
    if lang == "en":
        return IND_EN.get(value, value)
    return IND_ZH.get(value, value)


def cat_multiselect(label, raw_options, category, key):
    """带分类翻译的多选筛选器。

    由于 st.multiselect 的 format_func 不作用于「已选标签」，这里直接把选项值
    换成翻译后的文本，再反查回原始值，供页面用原始值做数据过滤。
    key 末尾会拼上当前语言，切换语言时自动重置为全选。
    """
    show = [cat_text(category, v) for v in raw_options]
    back = dict(zip(show, raw_options))
    sel = st.multiselect(label, show, default=show, key=f"{key}_{get_lang()}")
    return [back.get(v, v) for v in sel]


def salary_text(country, field):
    """取某国薪资口径文案：salary_text('CN','avg') -> '平均月薪' / 'Avg monthly salary'。"""
    lang = get_lang()
    entry = SALARY.get(country, SALARY["US"])[field]
    return entry.get(lang) or entry.get("en")


def jobs_str(n):
    """岗位数量：'5853 条' / '5,853'。"""
    return f"{n:,} 条" if get_lang() == "zh" else f"{n:,}"


def lang_toggle():
    """侧边栏语言切换（存 session_state['lang']，跨页生效）。"""
    with st.sidebar:
        st.markdown("**Language / 语言**")
        st.radio(
            "lang", ["zh", "en"], key="lang",
            format_func=lambda x: "中文" if x == "zh" else "English",
            horizontal=True, label_visibility="collapsed",
        )
