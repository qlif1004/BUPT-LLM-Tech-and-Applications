学术论文自动追踪与简报生成系统 —— 项目设计文档

## 一、项目概述

本项目面向研究生学者，构建一个基于 LLM Agent 的学术论文自动追踪与简报生成系统。

系统提供 CLI 命令行界面和 Web 前端两种交互方式。Web 前端通过对话式 Chat UI 支持自然语言指令路由，自动识别用户意图并分发到对应模块。

---

## 二、系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户交互层                                │
│         自然语言输入 → 意图解析 → 任务配置确认                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      Agent 编排层 (LangGraph)                    │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│   │ 意图解析节点  │  │ 任务调度节点  │  │   报告生成节点        │  │
│   └──────────────┘  └──────────────┘  └──────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                       数据获取层                                  │
│   ┌──────────┐  ┌──────────────────┐  ┌──────────┐             │
│   │  arXiv   │  │ Semantic Scholar  │  │ CrossRef │  ...        │
│   └──────────┘  └──────────────────┘  └──────────┘             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                       排序与筛选层                                │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│   │  最新 Ranker  │  │ 热门 Ranker  │  │   相关性 Ranker       │  │
│   │  (按发布日期) │  │ (引用/热度)  │  │  (语义向量相似度)     │  │
│   └──────────────┘  └──────────────┘  └──────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                       存储层                                      │
│         用户配置 | 论文缓存 | 历史报告 | 向量索引                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、核心功能模块设计

### 3.1 意图解析模块 (IntentParser)

将用户自然语言输入解析为结构化的任务配置对象。

**输入示例：**
> "帮我追踪大语言模型推理优化方向的论文，关注 NeurIPS、ICML 和 arXiv cs.LG，每周一早上推送，重点关注最近三个月的成果"

**输出结构：**
```json
{
  "research_direction": "大语言模型推理优化",
  "keywords": ["LLM inference", "reasoning optimization", "efficient inference"],
  "sources": ["arxiv:cs.LG", "dblp:KDD", "semantic_scholar"],
  "time_range_days": 90,
  "schedule": "每周一 08:00",
  "categories": ["latest", "popular", "relevant"],
  "top_n_per_category": 5
}
```

### 3.2 自然语言指令路由 (NLRouter)

将用户的任意自然语言输入分类为系统功能意图并提取参数。支持 10 种意图：search / schedule / list_tasks / trigger_task / view_logs / view_reports / start_scheduler / help / exit / unrelated。

### 3.3 论文获取模块 (Fetchers)

支持多数据源，统一抽象为 `BaseFetcher` 接口。

| 数据源 | API | 获取内容 |
|--------|-----|---------|
| arXiv | arXiv API (免费) | 预印本，cs/physics/math 等 |
| Semantic Scholar | S2 API (免费) | 引用数、影响力、摘要 |
| CrossRef | CrossRef REST API | DOI、期刊、会议论文 |
| PubMed | NCBI E-utilities | 生物医学领域 |

每个 Fetcher 返回统一的 `Paper` 数据模型：
```python
class Paper:
    title: str
    authors: list[str]
    abstract: str
    published_date: datetime
    url: str
    doi: Optional[str]
    citation_count: int
    source: str
    keywords: list[str]
    venue: Optional[str]   # 期刊/会议名
```

---

### 3.3 排序与筛选模块 (Rankers)

#### 最新 (Latest Ranker)
- 按 `published_date` 降序排列
- 过滤指定时间窗口内的论文
- 去重（同一论文可能出现在多个数据源）

#### 最热门 (Popular Ranker)
- 综合评分 = `citation_count × 0.6 + recent_citation_velocity × 0.3 + altmetric_score × 0.1`
- `recent_citation_velocity`：近 30 天新增引用数（反映近期热度）
- 可选接入 Altmetric API 获取社交媒体热度

#### 最相关 (Relevance Ranker)
- 将用户研究方向描述和论文摘要分别编码为向量（使用 `text-embedding-3-small` 或本地 `sentence-transformers`）
- 计算余弦相似度，取 Top-N
- 支持关键词精确匹配加权

---

### 3.4 报告生成模块 (Report Generator)

**单篇论文简报生成：**
- 输入：论文标题 + 摘要 + 元数据
- 输出：3-5 句话的中文简报，包含核心贡献、方法亮点

**整体进展综述生成：**
- 输入：本次所有筛选论文的简报集合 + 用户研究方向
- 输出：500-800 字的近期研究进展概要，涵盖主要趋势、代表性工作、潜在研究空白

**Prompt 设计原则：**
- 角色设定为"资深学术助手"
- 要求输出结构化 Markdown
- 明确要求保留原文链接，不捏造内容

---

### 3.5 任务调度模块 (Scheduler)

使用 APScheduler，支持 cron 表达式、中文调度规则识别、任务持久化和手动触发。

### 3.7 存储模块 (Storage)

使用 SQLite + SQLAlchemy，含 task_configs / papers / reports / task_runs 四张表。

---

## 四、工作流程

### CLI 流程
```
用户输入 → IntentParser 解析 → 展示 TaskConfig
  → [确认执行 / 修改配置 / 取消]
  → Fetcher 获取论文 → 去重 → Ranker 排序
  → ReportGenerator 生成简报 → 保存 Markdown
```

### Web 流程
```
用户输入 → NLRouter 意图分类
  → search/schedule: 解析配置 → 返回 config_review → 用户确认/修改/取消 → 执行
  → 其他意图: 直接执行并返回结果
```

---

## 五、代码结构

```
academic_tracker/
├── agent/
│   ├── deepseek_client.py
│   ├── graph.py
│   ├── intent_parser.py
│   ├── nl_router.py
│   └── report_generator.py
├── config/settings.py
├── fetchers/
│   ├── __init__.py
│   ├── base.py                  # BaseFetcher 抽象类
│   ├── arxiv_fetcher.py         # arXiv API 封装
│   ├── semantic_scholar.py      # Semantic Scholar API 封装
│   └── crossref_fetcher.py      # CrossRef API 封装
│
├── rankers/
│   ├── latest.py
│   ├── popular.py
│   └── relevant.py
├── scheduler/task_scheduler.py
├── storage/
│   ├── database.py
│   └── models.py
├── tests/test_core.py
├── utils/
│   ├── deduplication.py
│   └── formatting.py
server.py
static/index.html
```

---

## 六、技术栈

| 层次 | 技术选型 | 说明 |
|------|---------|------|
| Agent 框架 | 自研编排 (graph.py) | 任务编排 / 数据获取 / 排序 / 报告生成 |
| LLM | DeepSeek API | 意图解析、摘要生成、NL 路由 |
| Web 框架 | FastAPI + uvicorn | REST API + 静态文件服务 |
| 前端 | Vanilla HTML/CSS/JS + marked.js | SPA 三页面 |
| 关系数据库 | SQLite + SQLAlchemy | 轻量持久化 |
| 任务调度 | APScheduler | 定时任务 |
| HTTP 客户端 | httpx (异步) | 并发 API 请求 |
| 数据验证 | Pydantic v2 | 数据模型与校验 |
| 论文数据源 | arXiv API, Semantic Scholar API, CrossRef API | 免费，无需注册 |
| 测试 | pytest + pytest-asyncio | 单元测试 |

---

## 七、关键数据流示例

以用户配置"追踪 RAG 方向，每周推送"为例：

```
1. 用户输入 → intent_parser 解析
   → TaskConfig(keywords=["RAG","retrieval augmented generation"], schedule="weekly", ...)

2. 定时触发 → fetch_papers 并发请求
   → arXiv 返回 50 篇 + Semantic Scholar 返回 30 篇 → 去重后 60 篇

3. rank_papers 三路并行
   → Latest:   按日期取 Top 5
   → Popular:  按引用速度取 Top 5
   → Relevant: 向量相似度取 Top 5（可能与前两类有重叠，报告中标注）

4. generate_summaries 并发（最多 15 篇）
   → 每篇生成 3-5 句中文简报

5. generate_overview
   → 基于 15 篇简报生成 600 字进展综述

6. format_report → 输出完整 Markdown 报告
```

---

## 八、报告输出格式

```markdown
# 学术简报：RAG 方向近期进展
生成时间：2026-06-01 | 覆盖范围：arXiv cs.CL, ACL, EMNLP | 时间窗口：近 30 天

---

## 一、最新论文 (Top 5)

### 1. [论文标题](原文链接)
**作者：** ... | **发表：** 2026-05-28 | **来源：** arXiv cs.CL
**核心贡献：** ...（3-5 句简报）

...

---

## 二、最热门论文 (Top 5)

### 1. [论文标题](原文链接)
**引用数：** 142 | **近期引用增速：** +38/月
**核心贡献：** ...

...

---

## 三、最相关论文 (Top 5)

### 1. [论文标题](原文链接)
**相关度：** 0.94 | **关键词匹配：** RAG, dense retrieval
**核心贡献：** ...

...

---

## 四、近期研究进展综述

（600-800 字，涵盖主要趋势、代表性工作、值得关注的新方向）

...
```

---

## 八、实现阶段

| 阶段 | 内容 | 预计工时 |
|------|------|---------|
| Phase 1 | 数据模型 + arXiv/Semantic Scholar Fetcher + 基础排序 | 1 天 |
| Phase 2 | LangGraph Agent 工作流 + 意图解析 + 报告生成 | 1.5 天 |
| Phase 3 | 向量相关性排序 + ChromaDB 集成 | 0.5 天 |
| Phase 4 | APScheduler 定时任务 + SQLite 持久化 | 0.5 天 |
| Phase 5 | CLI 交互界面 + 完整测试 + README | 0.5 天 |

**总计约 4 天可完成可演示的完整系统。**

---

## 九、扩展方向

- 更多学术数据源：CrossRef、PubMed、OpenAlex
- 向量数据库：ChromaDB 集成提升相关性排序质量
- 多用户支持：用户独立的配置和报告历史
- 消息推送：邮件、企业微信、飞书等报告推送渠道
