# 给个工作吧

一个数据分析岗求职工具：用招聘数据看清市场，用 7 个 AI 工具从找方向到拿 offer。

> 注意：本站图表数据为**示例数据**（500 条岗位样本，非真实招聘数据），仅用于功能演示。

## 功能

### 1. 📊 招聘市场分析
薪资、行业、学历、经验全景看板。图表可悬停、框选缩放；点击「行业对比」中的柱子可联动筛选其他图表。

### 2. 💪 技能排行
最吃香技能出现次数总排名、技能类别分布、各行业技能出现率，以及「某个技能在哪些行业吃香」。

### 3. 🧰 求职工具箱（7 个 AI 工具）
填自己的 DeepSeek API Key（只存当前会话内存，不落盘）：

① 隐藏角色搜索器 · ② 可转移技能翻译器 · ③ 资格差距分析器 · ④ 职业支点地图 · ⑤ 最佳匹配行业扫描器 · ⑥ 简历定位重写工具 · ⑦ 机会搜索策略

## 本地运行

```bash
pip install -r requirements.txt

# 准备数据（示例数据即可跑通，或用 crawler/boss.py 爬真实数据）
python crawler/make_sample_data.py
python analysis/clean.py
python analysis/analyze.py

# 启动网站
streamlit run app.py
```

冒烟测试（需先启动 Streamlit）：

```bash
python scripts/smoke_test.py
```

## 部署到 Streamlit Community Cloud

1. 把本仓库推送到 GitHub。
2. 打开 [share.streamlit.io](https://share.streamlit.io) → New app → 选择该仓库，Main file path 填 `app.py`。
3. Deploy。访客在求职工具箱页填自己的 DeepSeek API Key 即可使用。

## 目录结构

```
app.py                        # 主页（功能入口 + 数据亮点 + 价值主张）
pages/
  1_📊_市场分析.py            # 招聘市场分析看板
  2_🧰_求职工具箱.py          # 求职工具箱（7 个 AI 工具）
  3_💪_技能排行.py            # 技能排行
review/reviewer.py            # 求职工具箱后端（DeepSeek API 调用）
crawler/                      # 数据采集（boss.py / make_sample_data.py）
analysis/                     # 数据清洗（clean.py）+ 分析出图（analyze.py）
assets/                       # 主页配图（hero.jpg / office.jpg）
scripts/smoke_test.py         # Playwright 冒烟测试
styles.py                     # 全局样式（深蓝主题）
viz.py                        # 共享可视化工具（配色 / 图表 / 数据加载）
data/                         # raw 原始数据 / cleaned 清洗后数据
output/                       # 分析图表 + 技能排行榜 CSV
```

## 说明

- 爬虫仅供个人学习，请尊重目标网站 robots 协议、控制请求频率，勿用于商业用途。
- 求职工具箱后端 API Key 仅存当前会话内存，不写入磁盘或代码。
