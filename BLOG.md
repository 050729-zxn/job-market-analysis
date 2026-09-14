# 给个工作吧：Streamlit 求职网站的中英双语与分国家改造踩坑记

> 一个数据分析岗求职网站：用真实招聘数据看市场，用 7 个 AI 工具找工作。
> 这次我们把数据拆成「中国 / 美国」、给全站加上中英双语切换，一路踩了不少坑。
> 按「现象 → 原因 → 解决」的顺序记下来，希望能帮到同样在折腾 Streamlit 双语的人。

## 项目背景

「给个工作吧」是一个 Streamlit 多页应用（主页 + 市场分析 + 求职工具箱 + 技能排行）。这次的核心需求：

1. 数据区分**中国 / 美国**，市场分析和技能排行支持「只看中国 / 只看美国 / 两国对比」三种视角；
2. 全站**中英双语**可切换，AI 工具箱的输出也跟着界面语言走；
3. 修复首页「真实岗位」显示 500 的问题。

---

## 坑 1：首页「真实岗位」显示 500？

**现象**：首页数据亮点里「真实岗位」显示 500。

**原因**：不是数据算错了，是线上还在跑最早那版的**示例数据**（500 条 sample），真正的数据早已换成 5853 条真实岗位。

**解决**：把中国 300 条（BOSS 直聘公开数据，月薪·人民币）+ 美国 5553 条（公开数据，年薪·美元）合并进 `data/cleaned/cleaned.csv`，加一个 `country` 列区分，重新提交即可。

---

## 坑 2：薪资单位打架——月薪 vs 年薪、人民币 vs 美元

**现象**：两份数据薪资口径完全不同：中国是「月薪·人民币」，美国是「年薪·美元」。直接放进一张图毫无意义，粗暴换算又可能失真。

**决策**：**不换算，并排展示、各自标单位**。

**做法**：给每个国家单独定义薪资口径文案，图表的坐标轴、指标、说明都按国家取：

```python
def salary_text(country, field):
    # 中国 -> "月薪（K）"，美国 -> "Annual salary (K$)"
```

对比模式用 `st.columns(2)` 并排渲染两国，各自用自己的单位标签。

---

## 坑 3：数据里的分类值不会自己翻译（本次最隐蔽）

**现象**：切英文后，标题、按钮、统计标签都变英文了，但图表里的**行业名、学历、经验**还是中文——因为它们是 CSV 里的原始数据，不是 UI 文案。

**原因**：只翻了「界面文案」，漏了「数据值」。行业 / 学历 / 经验这些分类值是存在数据里的中文，切语言时原样显示。

**解决**：建一个 `catalog_i18n.py`，把分类值全部映射：

- 学历 5 个、经验 5 个（数据里统一是中文）；
- 中国行业 47 个 → 英文；美国行业 109 个 → 中文。

再提供一个统一翻译函数，所有图表标签、下拉框、提示文案都改走它：

```python
def cat_text(category, value):
    # "互联网" -> "Internet"（切英文时）；"IT Services" -> "IT 服务"（切中文时）
```

---

## 坑 4：st.multiselect 的 format_func 不作用于已选标签

**现象**：修完上面的问题，筛选器**已选标签**还是中文。

**排查**：用 Playwright 抓到残留中文的 DOM 节点，发现全都挂在 `stMultiSelectTagsContainer` 下——也就是多选框的「已选标签」。

**原因**：Streamlit 的 `st.multiselect` 里，`format_func` **只作用于下拉选项，不作用于已选标签**（pill）。这是个很隐蔽的行为差异，不实测根本不会发现。

**解决**：既然标签不吃 format_func，那就直接把**选项值本身换成翻译后的文本**，选完再反查回原始值做过滤：

```python
def cat_multiselect(label, raw_options, category, key):
    show = [cat_text(category, v) for v in raw_options]  # 显示用的翻译文本
    back = dict(zip(show, raw_options))                   # 翻译 -> 原始值
    sel = st.multiselect(label, show, default=show, key=f"{key}_{get_lang()}")
    return [back.get(v, v) for v in sel]                  # 反查回原始值
```

`key` 末尾拼上当前语言，切换语言时自动重置为全选，避免旧语言的值残留。

---

## 坑 5：本地服务缓存旧模块 → ImportError

**现象**：改完 `viz.py` 后，子页面全崩：

```
ImportError: cannot import name 'country_select' from 'viz'
```

**原因**：`streamlit run` 是在改文件**之前**启动的，进程内存里还缓存着旧版模块；磁盘上明明有 `country_select`，运行中的进程却不知道。

**解决**：**重启服务**（kill 掉进程重新 `streamlit run`）。这是本地开发最容易误判的一个点——看到报错先别急着怀疑代码，重启一下。

---

## 坑 6：AI 工具箱的输出要跟随语言

**现象**：切英文后，7 个 AI 工具（简历分析、岗位推荐、差距分析…）返回的还是中文。

**解决**：调用 LLM 前 `set_lang(get_lang())`，并在提示词里追加语言指令：

```python
LANG_INSTR = {
    "zh": "请用中文回答，包括所有枚举值和薪资范围（薪资用「K/月」）。",
    "en": "Respond entirely in English ... and salary ranges in $K/year.",
}
```

---

## 坑 7：测试里的两个假警报（浪费过时间）

- **AppTest 隔离环境**：在隔离环境里跑带 `st.page_link("app.py")` 的页面会报 `Could not find page: app.py`——这是 AppTest 没有多页路由的**测试工具限制**，不是真 bug。
- **Playwright 全页跳转重置 session_state**：`page.goto()` 等于开新会话，切好的语言会被清空；真实应用里的 `st.page_link` 导航是保留会话的。

---

## 小结

做双语站点的几条心得：

1. **别只翻 UI 文案**，数据里的分类值（行业 / 学历 / 经验）也要翻译，这是最容易漏的。
2. **Streamlit 组件的行为差异要实测**——`multiselect` 的 format_func 就是活生生的例子，不能想当然。
3. **本地服务改了模块要重启**，报 ImportError 先重启再怀疑代码。
4. 双语不是「一个字典」就完事，是数据层、展示层、AI 层都要有语言意识。

项目地址：https://github.com/050729-zxn/job-market-analysis
