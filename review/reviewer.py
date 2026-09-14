# -*- coding: utf-8 -*-
"""求职工具箱后端：基于 DeepSeek API 的 7 个 AI 工具。

每个工具是一个独立函数，输入简历（部分工具还需 JD / 目标方向），
调用 LLM 返回结构化 JSON，供页面渲染。

用法：
    from review.reviewer import find_roles
    result = find_roles(api_key, resume, model)
"""
import io
import json

import requests

API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"  # 可在页面上改，如 deepseek-v4-pro / deepseek-reasoner

# 当前输出语言（由页面在渲染时设置，用于让 AI 结果跟随界面语言）
_CURRENT_LANG = "zh"

LANG_INSTR = {
    "zh": "请用中文回答，包括所有枚举值和薪资范围（薪资用「K/月」）。",
    "en": (
        "Respond entirely in English — including all enum values "
        "(高/中/低 → high/medium/low, 强/中/弱 → strong/medium/weak, "
        "已满足/部分满足/缺失 → met/partially met/missing, 低/中/高 → low/medium/high) "
        "and salary ranges in $K/year."
    ),
}


def set_lang(lang):
    """设置后续所有工具调用的输出语言（'zh' / 'en'）。"""
    global _CURRENT_LANG
    _CURRENT_LANG = lang if lang in ("zh", "en") else "zh"


def extract_text(uploaded_file):
    """从上传的文件里提取纯文本。支持 txt / md / docx / pdf。"""
    name = (uploaded_file.name or "").lower()
    data = uploaded_file.getvalue()

    if name.endswith((".txt", ".md", ".markdown")):
        return data.decode("utf-8", errors="ignore")

    if name.endswith(".docx"):
        from docx import Document
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    if name.endswith(".pdf"):
        import pdfplumber
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            return "\n".join((page.extract_text() or "") for page in pdf.pages)

    raise ValueError("暂不支持的文件格式，请上传 txt / md / docx / pdf。")


def _call_llm(api_key, system, user, model=MODEL):
    """调用 DeepSeek chat/completions，强制 JSON 输出，返回解析后的 dict。"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.3,
        "response_format": {"type": "json_object"},
    }
    resp = requests.post(API_URL, json=payload, headers=headers, timeout=300)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    # 容错：去掉可能包裹的 ```json ``` 标记
    content = content.strip()
    if content.startswith("```"):
        content = content.strip("`")
        if content.startswith("json"):
            content = content[4:]
    return json.loads(content)


def _run_tool(api_key, system, user, schema, model=MODEL):
    """通用工具调用：把 JSON schema 追加到 prompt，强制结构化输出。"""
    user_full = (
        user
        + "\n\n请严格按以下 JSON 结构返回（不要输出任何多余文字）：\n"
        + json.dumps(schema, ensure_ascii=False, indent=2)
        + "\n\n" + LANG_INSTR[_CURRENT_LANG]
    )
    result = _call_llm(api_key, system, user_full, model)
    # 校验顶层字段是否齐全，缺了就给用户友好提示，而不是渲染出静默空白
    if not isinstance(result, dict) or not schema.keys() <= result.keys():
        raise ValueError("返回结果不完整，请重试一次")
    return result


# ============================================================
# 工具 1：隐藏角色搜索器 —— 找岗位方向
# ============================================================
def find_roles(api_key, resume, model=MODEL):
    """识别 15 个与经验匹配的跨行业职位，按契合度/薪资/需求/准入难度分类。"""
    schema = {
        "roles": [
            {
                "title": "职位名",
                "industry": "所属行业",
                "fit_score": 85,
                "fit_reason": "为什么匹配（1-2句）",
                "salary_range": "如 12-20K/月",
                "demand": "高/中/低",
                "entry_difficulty": "低/中/高",
            }
        ]
    }
    system = "你是资深职业规划师与猎头，擅长发现候选人经验可迁移到的隐藏岗位。"
    user = (
        "【候选人简历】\n{resume}\n\n"
        "请分析这份简历，识别 15 个与该候选人经验匹配的「跨行业职位」——"
        "即不是候选人当前明显对口、但经验其实能迁移过去的岗位。\n"
        "要求：\n"
        "1. 职位要具体（如「数据产品经理」「商业分析师」「风控策略分析师」），不要泛泛的「数据分析师」；\n"
        "2. 覆盖多个不同行业（互联网、金融、零售、制造、咨询、游戏等），体现「跨行业」；\n"
        "3. 每个职位给出：契合度评分(0-100)、契合原因、薪资范围、招聘需求热度、准入难度；\n"
        "4. 按契合度从高到低排序，共 15 个。"
    ).format(resume=resume)
    return _run_tool(api_key, system, user, schema, model)


# ============================================================
# 工具 2：可转移技能翻译器 —— 提取可迁移技能
# ============================================================
def translate_skills(api_key, resume, model=MODEL):
    """提取雇主看重的技能，关联行业岗位，解释经验匹配度。"""
    schema = {
        "skills": [
            {
                "skill": "技能名",
                "why_valuable": "雇主为何看重（1-2句）",
                "related_roles": ["可关联的岗位或行业"],
                "match_level": "强/中/弱",
                "evidence": "简历中的具体证据",
            }
        ]
    }
    system = "你是可迁移技能评估专家，擅长把候选人的具体经验翻译成雇主能看懂的通用技能语言。"
    user = (
        "【候选人简历】\n{resume}\n\n"
        "请提取这份简历中「雇主真正看重」的技能，并翻译成可迁移的通用技能。\n"
        "要求：\n"
        "1. 提取 8-12 项核心技能（既包括硬技能如 Python/SQL，也包括软技能如跨部门协作、项目推动）；\n"
        "2. 每项说明：雇主为何看重、可关联到哪些行业/岗位、经验匹配度；\n"
        "3. 匹配度用「强 / 中 / 弱」标注，并引用简历中的具体证据。"
    ).format(resume=resume)
    return _run_tool(api_key, system, user, schema, model)


# ============================================================
# 工具 3：资格差距分析器 —— 分析 JD 差距
# ============================================================
def analyze_gap(api_key, resume, jd, model=MODEL):
    """对比简历与 JD，标注已满足/部分满足/缺失项，给出补差距方案。"""
    schema = {
        "requirements": [
            {
                "requirement": "JD 中的一条要求",
                "status": "已满足/部分满足/缺失",
                "evidence": "简历证据（已满足/部分满足时），或缺失说明",
                "gap_action": "补差距的最快方案（部分满足/缺失时）",
            }
        ],
        "summary": "总体差距结论（1-2句）",
    }
    system = "你是资深招聘顾问，擅长做候选人资格与 JD 要求的差距分析。"
    user = (
        "【候选人简历】\n{resume}\n\n"
        "【目标岗位 JD】\n{jd}\n\n"
        "请逐条对比 JD 中的任职要求与候选人简历，标注每条要求的满足状态：\n"
        "- 已满足：简历里有明确证据；\n"
        "- 部分满足：有相关经验但不完全对口，或证据不够硬；\n"
        "- 缺失：简历里找不到对应证据。\n\n"
        "对「部分满足」和「缺失」的项，给出「补差距的最快方案」（可操作、能在一个月内推进）。\n"
        "最后给一句总体差距结论。"
    ).format(resume=resume, jd=jd)
    return _run_tool(api_key, system, user, schema, model)


# ============================================================
# 工具 4：职业支点地图 —— 规划职业路线
# ============================================================
def career_pivot(api_key, resume, model=MODEL):
    """生成 5 条职业转型路线，含初始岗位、技能缺口、薪资范围、30天计划。"""
    schema = {
        "routes": [
            {
                "route_name": "路线名（方向）",
                "entry_role": "初始岗位",
                "skill_gaps": ["需要补的技能缺口"],
                "salary_range": "薪资范围",
                "plan_30days": ["30天过渡计划的步骤，4-6步"],
            }
        ]
    }
    system = "你是职业转型规划师，擅长为候选人设计可行的职业转型路线。"
    user = (
        "【候选人简历】\n{resume}\n\n"
        "请基于这份简历，生成 5 条不同的「职业转型路线」。每条路线要：\n"
        "1. 给出一个「初始岗位」（转型第一步，候选人现在就能投、门槛匹配的岗位）；\n"
        "2. 列出需要补的「技能缺口」；\n"
        "3. 给出该岗位的「薪资范围」；\n"
        "4. 给出一份「30 天过渡计划」（分步骤、可执行）。\n\n"
        "5 条路线尽量覆盖不同方向（如：数据方向、产品方向、运营方向、行业研究、技术方向等），体现多样性。"
    ).format(resume=resume)
    return _run_tool(api_key, system, user, schema, model)


# ============================================================
# 工具 5：最佳匹配行业扫描器 —— 找匹配行业
# ============================================================
def scan_industries(api_key, resume, model=MODEL):
    """识别 10 个适配技能的行业，按招聘需求/薪酬/成长空间/准入难度排序。"""
    schema = {
        "industries": [
            {
                "industry": "行业名",
                "demand": "招聘需求：高/中/低",
                "salary": "薪酬水平：高/中/低",
                "growth": "成长空间：高/中/低",
                "entry_difficulty": "准入难度：低/中/高",
                "fit_reason": "适配理由（1-2句）",
            }
        ]
    }
    system = "你是行业研究分析师，擅长评估候选人技能与不同行业的匹配度。"
    user = (
        "【候选人简历】\n{resume}\n\n"
        "请识别 10 个最适配这份简历技能的行业，按以下维度评估：\n"
        "1. 招聘需求：该行业对这类人才的需求热度；\n"
        "2. 薪酬：该行业相关岗位的薪酬水平；\n"
        "3. 成长空间：该行业未来的发展空间；\n"
        "4. 准入难度：候选人进入该行业的难易。\n\n"
        "按「综合适配度」从高到低排序，每个行业给一句适配理由。"
    ).format(resume=resume)
    return _run_tool(api_key, system, user, schema, model)


# ============================================================
# 工具 6：简历定位重写工具 —— 优化简历
# ============================================================
def rewrite_resume(api_key, resume, target, model=MODEL):
    """针对目标方向重写简历，突出成就/量化成果/行业术语，不造假。"""
    schema = {
        "rewritten_resume": "重写后的完整简历文本",
        "changes": [
            {
                "before": "原文片段",
                "after": "改写后片段",
                "reason": "为什么这样改",
            }
        ],
    }
    system = "你是资深简历顾问，擅长针对特定目标方向重写简历，突出成就与量化成果，但绝不允许造假。"
    user = (
        "【候选人简历】\n{resume}\n\n"
        "【目标方向】\n{target}\n\n"
        "请针对这个目标方向重写简历。要求：\n"
        "1. 突出与目标方向最相关的成就和可量化成果；\n"
        "2. 使用目标行业的专业术语；\n"
        "3. 严格基于简历中的真实经历改写，绝不虚构、不夸大数字；\n"
        "4. 保留简历原有的基本信息结构。\n\n"
        "同时列出你做的关键改动（原文 → 改写后 → 为什么这样改），挑最重要的 5-8 处。"
    ).format(resume=resume, target=target)
    return _run_tool(api_key, system, user, schema, model)


# ============================================================
# 工具 7：机会搜索策略 —— 30 天求职计划
# ============================================================
def job_strategy(api_key, resume, target, model=MODEL):
    """制定 30 天求职计划：关键词、企业清单、拓展动作、每周复盘节点。"""
    schema = {
        "keywords": ["搜索关键词"],
        "companies": [{"name": "企业名或类型", "note": "为什么是目标"}],
        "outreach": ["拓展动作"],
        "weekly_plan": [
            {"week": 1, "focus": "本周重点", "actions": ["具体动作"], "review": "复盘要点"}
        ],
    }
    system = "你是求职策略顾问，擅长制定可执行的求职行动计划。"
    user = (
        "【候选人简历】\n{resume}\n\n"
        "【目标方向】\n{target}\n\n"
        "请为这个目标方向制定一份 30 天求职计划，包含：\n"
        "1. 搜索关键词：在招聘网站用什么关键词搜；\n"
        "2. 目标企业清单：10-15 家，含公司类型/为何是目标；\n"
        "3. 拓展动作：networking、内推、猎头、作品集等；\n"
        "4. 每周复盘节点：第 1-4 周，每周的 focus + 具体动作 + 复盘要点。"
    ).format(resume=resume, target=target)
    return _run_tool(api_key, system, user, schema, model)
