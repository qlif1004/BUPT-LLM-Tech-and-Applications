# 学术论文自动追踪与简报生成系统 — 项目设计文档

## 一、项目概述

本项目面向研究生学者，构建一个基于 LLM Agent 的学术论文自动追踪与简报生成系统。用户通过自然语言配置研究方向、关键词、查询范围和周期，Agent 自动从多个学术数据源获取论文，按**最新**、**最热门**、**最相关**三类规则筛选排序，生成包含摘要、核心贡献和原文链接的结构化简报，并附上当前研究方向的近期进展综述。

系统同时提供 CLI 命令行界面和 Web 前端两种交互方式。Web 前端通过对话式 Chat UI 支持自然语言指令路由，自动识别用户意图并分发到对应模块。

---

## 二、系统架构

```text
┌─────────────────────────────────────────────────────────────────┐
│                        用户交互层                                │
│       CLI / Rich Console     |     Web UI / FastAPI SPA          │
│         自然语言输入 → 意图解析 → 任务配置确认                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      指令路由与解析层                             │
│   ┌──────────────────┐      ┌────────────────────────────────┐  │
│   │ NLRouter          │      │ IntentParser                    │  │
│   │ 系统功能意图识别   │      │ 自然语言 → TaskConfig            │  │
│   └──────────────────┘      └────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                       Agent 编排层                                │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│   │ 数据获取流程  │  │ 排序筛选流程  │  │   报告生成流程        │  │
│   └──────────────┘  └──────────────┘  └──────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                       数据获取层                                  │
│   ┌──────────┐  ┌──────────┐  ┌─────────────────────────────┐   │
│   │  arXiv   │  │  DBLP    │  │ Semantic Scholar             │   │
│   └──────────┘  └──────────┘  └─────────────────────────────┘   │
│              CrossRef / PubMed / OpenAlex 等作为后续扩展          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                       排序与筛选层                                │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│   │  最新 Ranker  │  │ 热门 Ranker  │  │   相关性 Ranker       │  │
│   │  按发布日期   │  │ 引用/热度     │  │  关键词/语义相关性     │  │
│   └──────────────┘  └──────────────┘  └──────────────────────┘  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                       存储与调度层                                │
│     SQLite: 任务配置 | 论文缓存 | 历史报告 | 运行日志             │
│     APScheduler: 周期任务注册、恢复、手动触发                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、核心功能模块设计

### 3.1 意图解析模块 (IntentParser)

将用户自然语言输入解析为结构化的任务配置对象。

**输入示例：**

> “帮我追踪大语言模型推理优化方向的论文，关注 NeurIPS、ICML 和 arXiv cs.LG，每周一早上推送，重点关注最近三个月的成果”

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

**实现方式：** 调用 DeepSeek API，将自然语言映射到 `TaskConfig` Pydantic 模型，并在 CLI / Web 侧展示解析结果供用户确认、修改或取消。

---

### 3.2 自然语言指令路由 (NLRouter)

`NLRouter` 面向 Web 对话、CLI `nl` 命令和交互式控制台，用于判断用户当前想执行哪类系统操作。

支持的意图包括：

| 意图 | 说明 |
| --- | --- |
| `search` | 立即检索论文并生成简报。 |
| `schedule` | 创建周期追踪任务。 |
| `list_tasks` | 查看任务列表。 |
| `trigger_task` | 手动触发指定任务。 |
| `view_logs` | 查看任务运行日志。 |
| `view_reports` | 查看历史报告。 |
| `start_scheduler` | 启动调度服务。 |
| `help` | 展示帮助信息。 |
| `exit` | 退出交互式会话。 |
| `unrelated` | 与系统能力无关的问题。 |

`search` 与 `schedule` 意图会继续进入 `IntentParser`；其他管理类意图可直接由对应工具函数执行。

---

### 3.3 论文获取模块 (Fetchers)

支持多数据源，统一抽象为 `BaseFetcher` 接口。

| 数据源 | API | 获取内容 | 当前状态 |
| --- | --- | --- | --- |
| arXiv | arXiv API | 预印本，cs/physics/math 等 | 已实现 |
| DBLP | DBLP Search API | 会议/期刊元数据、DOI、venue | 已实现 |
| Semantic Scholar | S2 API | 引用数、影响力、摘要 | 已实现 |
| CrossRef | CrossRef REST API | DOI、期刊、会议论文 | 扩展方向 |
| PubMed | NCBI E-utilities | 生物医学领域 | 扩展方向 |

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
    venue: Optional[str]
    external_id: Optional[str]
```

DBLP 主要提供会议/期刊元数据；当摘要、引用数等信息不足时，可通过 DOI 或标题尝试使用 Semantic Scholar 批量接口补充元数据。

---

### 3.4 排序与筛选模块 (Rankers)

#### 最新 (Latest Ranker)

- 按 `published_date` 降序排列。
- 过滤指定时间窗口内的论文。
- 与去重逻辑配合，避免同一论文在多个数据源中重复展示。

#### 最热门 (Popular Ranker)

- 基于 `citation_count` 等可获得的热度信号排序。
- 当数据源提供近期引用速度、影响力分数或其他热度指标时，可加入加权评分。
- 可扩展为：`citation_count × 0.6 + recent_citation_velocity × 0.3 + altmetric_score × 0.1`。

#### 最相关 (Relevance Ranker)

- 基于研究方向、关键词、标题、摘要和 venue 信息计算相关性。
- 当前可采用关键词匹配与文本相似度启发式评分。
- 后续可接入 `text-embedding-3-small`、本地 `sentence-transformers` 或 ChromaDB 向量索引，计算语义相似度。

---

### 3.5 报告生成模块 (ReportGenerator)

**单篇论文简报生成：**

- 输入：论文标题、摘要、作者、来源、时间、链接等元数据。
- 输出：3-5 句话的中文简报，包含核心贡献、方法亮点和适用场景。

**整体进展综述生成：**

- 输入：本次所有筛选论文的简报集合 + 用户研究方向。
- 输出：方向级近期研究进展概要，涵盖主要趋势、代表性工作、潜在研究空白。

**Prompt 设计原则：**

- 角色设定为“资深学术助手”。
- 要求输出结构化 Markdown。
- 明确要求保留原文链接。
- 不捏造摘要中没有的信息。
- 对摘要为空或元数据不足的论文，降低结论强度并明确依据有限。

---

### 3.6 任务调度模块 (Scheduler)

使用 `APScheduler` 实现定时任务：

- 支持 cron 表达式和常见中文调度规则识别。
- 任务持久化到 SQLite，重启后恢复。
- 支持手动触发指定任务。
- 记录每次任务执行状态、报告路径、错误信息和运行时间。

---

### 3.7 存储模块 (Storage)

使用 SQLite + SQLAlchemy，轻量、便于课程项目部署。核心表包括：

| 表 | 说明 |
| --- | --- |
| `task_configs` | 用户创建的追踪任务配置。 |
| `papers` | 论文缓存，避免重复抓取和重复入库。 |
| `reports` | 历史报告元数据与内容索引。 |
| `task_runs` | 每次任务执行日志，包括状态、错误与耗时。 |

向量索引暂不作为当前核心依赖；如后续引入 ChromaDB，可增加 `paper_vectors` 或独立向量存储目录。

---

## 四、工作流程

### 4.1 CLI 流程

```text
用户输入
  → IntentParser 解析
  → 展示 TaskConfig
  → [确认执行 / 修改配置 / 取消]
  → Fetcher 获取论文
  → 去重
  → Ranker 排序
  → ReportGenerator 生成简报
  → 保存 Markdown 与数据库记录
```

### 4.2 Web 流程

```text
用户输入
  → NLRouter 意图分类
  → search / schedule:
       IntentParser 解析配置
       → 返回 config_review
       → 用户确认 / 修改 / 取消
       → 执行检索或保存任务
  → 其他意图:
       直接执行对应管理操作并返回结果
```

### 4.3 Agent 执行流程

```text
[parse_task]
    │
    ▼
[fetch_papers] ──→ 并发或顺序调用多个 Fetcher
    │
    ▼
[deduplicate] ──→ DOI / external_id / title stable key 去重
    │
    ▼
[rank_papers] ──→ Latest / Popular / Relevant 各取 Top-N
    │
    ▼
[generate_summaries] ──→ 为入选论文生成中文简报
    │
    ▼
[generate_overview] ──→ 生成整体研究进展综述
    │
    ▼
[format_report] ──→ 整合为完整 Markdown 报告
    │
    ▼
[save_report] ──→ 写入 reports/ 与 SQLite
```

---

## 五、代码结构

```text
academic_tracker/
├── agent/
│   ├── __init__.py
│   ├── deepseek_client.py        # DeepSeek API 客户端
│   ├── graph.py                  # AcademicTrackerAgent 主编排逻辑
│   ├── intent_parser.py          # 自然语言 → TaskConfig
│   ├── nl_router.py              # 自然语言指令路由
│   ├── report_comparison.py      # 报告对比能力
│   └── report_generator.py       # 单篇简报 + 整体综述生成
├── config/
│   ├── __init__.py
│   └── settings.py               # 全局配置（API keys, 数据库路径等）
├── fetchers/
│   ├── __init__.py
│   ├── base.py                   # BaseFetcher 抽象类
│   ├── arxiv_fetcher.py          # arXiv API 封装
│   ├── dblp_fetcher.py           # DBLP Search API 封装
│   └── semantic_scholar.py       # Semantic Scholar API 封装
├── rankers/
│   ├── __init__.py
│   ├── latest.py                 # 最新论文排序
│   ├── popular.py                # 最热门论文排序
│   └── relevant.py               # 最相关论文排序
├── scheduler/
│   ├── __init__.py
│   └── task_scheduler.py         # APScheduler 任务管理
├── storage/
│   ├── __init__.py
│   ├── database.py               # 数据库连接与 CRUD 操作
│   └── models.py                 # SQLAlchemy ORM / Pydantic 数据模型
├── tests/
│   ├── test_core.py
│   └── test_web_app.py
└── utils/
    ├── __init__.py
    ├── deduplication.py          # 论文去重逻辑
    └── formatting.py             # Markdown 报告格式化

server.py                         # FastAPI REST API + 静态文件服务
static/index.html                 # Web SPA 页面
main.py                           # CLI 入口
requirements.txt                  # 依赖清单
.env.example                      # 环境变量模板
README.md                         # 项目说明
DESIGN.md                         # 项目设计文档
```

---

## 六、技术栈

| 层次 | 技术选型 | 说明 |
| --- | --- | --- |
| Agent 编排 | 自研编排 (`graph.py`) | 任务编排 / 数据获取 / 排序 / 报告生成 |
| LLM | DeepSeek API | 意图解析、摘要生成、NL 路由 |
| Web 框架 | FastAPI + uvicorn | REST API + 静态文件服务 |
| 前端 | Vanilla HTML/CSS/JS + marked.js | SPA 三页面 |
| 关系数据库 | SQLite + SQLAlchemy | 轻量持久化 |
| 任务调度 | APScheduler | 定时任务 |
| HTTP 客户端 | httpx | 异步 API 请求 |
| 数据验证 | Pydantic v2 | 数据模型与校验 |
| 论文数据源 | arXiv API, DBLP Search API, Semantic Scholar API | 免费或可选 API Key |
| 测试 | pytest + pytest-asyncio | 单元测试与 Web 测试 |

---

## 七、关键数据流示例

以用户配置“追踪 RAG 方向，每周推送”为例：

```text
1. 用户输入 → intent_parser 解析
   → TaskConfig(keywords=["RAG", "retrieval augmented generation"], schedule="weekly", ...)

2. 定时触发 → fetch_papers 请求数据源
   → arXiv 返回 50 篇 + DBLP 返回 30 篇 + Semantic Scholar 返回 30 篇
   → 去重后得到候选集合

3. rank_papers 三路排序
   → Latest:   按日期取 Top 5
   → Popular:  按引用数 / 热度取 Top 5
   → Relevant: 按关键词与语义相关性取 Top 5

4. generate_summaries
   → 每篇生成 3-5 句中文简报

5. generate_overview
   → 基于入选论文简报生成方向级进展综述

6. format_report
   → 输出完整 Markdown 报告

7. save_report
   → 保存到 reports/，并写入 reports 与 task_runs 表
```

---

## 八、报告输出格式

```markdown
# 学术简报：RAG 方向近期进展
生成时间：2026-06-01 | 覆盖范围：arXiv cs.CL, DBLP, Semantic Scholar | 时间窗口：近 30 天

---

## 一、最新论文 (Top 5)

### 1. [论文标题](原文链接)
**作者：** ... | **发表：** 2026-05-28 | **来源：** arXiv cs.CL
**核心贡献：** ...（3-5 句简报）

...

---

## 二、最热门论文 (Top 5)

### 1. [论文标题](原文链接)
**引用数：** 142
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

（围绕主要趋势、代表性工作、方法演进和潜在研究空白生成综述）
```

---

## 九、Web 与 API 设计

Web 端由 `server.py` 提供 FastAPI 服务，`static/index.html` 提供单页应用。

### 9.1 对话接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `POST` | `/api/chat` | 接收自然语言，返回消息或配置确认卡片。 |

`/api/chat` 对 search / schedule 类意图采用“先确认后执行”的交互模式：

```text
用户输入
  → 返回 config_review
  → 前端展示确认 / 修改 / 取消按钮
  → 用户确认后发送 __confirm__
  → 后端执行检索或创建任务
```

### 9.2 报告管理接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `GET` | `/api/reports` | 获取历史报告列表。 |
| `GET` | `/api/reports/{id}` | 获取单篇报告详情。 |
| `DELETE` | `/api/reports/{id}` | 删除报告。 |

### 9.3 任务管理接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| `GET` | `/api/tasks` | 获取定时任务列表。 |
| `DELETE` | `/api/tasks/{id}` | 删除定时任务。 |

---

## 十、实现阶段规划

| 阶段 | 内容 | 预计工时 |
| --- | --- | --- |
| Phase 1 | 数据模型 + arXiv / Semantic Scholar / DBLP Fetcher + 基础排序 | 1 天 |
| Phase 2 | Agent 工作流 + 意图解析 + 自然语言指令路由 + 报告生成 | 1.5 天 |
| Phase 3 | SQLite 持久化 + APScheduler 定时任务 | 0.5 天 |
| Phase 4 | CLI 交互界面 + 配置确认流程 + Web API | 0.5 天 |
| Phase 5 | Web SPA + 完整测试 + README / DESIGN 文档 | 0.5 天 |

**总计约 4 天可完成可演示的完整系统。**

---

## 十一、扩展方向

- **更多学术数据源**：CrossRef、PubMed、OpenAlex。
- **向量数据库**：ChromaDB 或 FAISS 集成，提升相关性排序质量。
- **多用户支持**：用户独立的任务配置和报告历史。
- **消息推送**：邮件、企业微信、飞书、Telegram 等报告推送渠道。
- **增量更新**：只处理上次运行后的新论文，避免重复生成报告。
- **引用网络分析**：可视化论文引用关系图。
- **报告质量评估**：增加 Prompt 评测、事实一致性检查和摘要质量打分。
- **CI/CD**：使用 GitHub Actions 自动运行测试和格式检查。
