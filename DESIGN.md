# 学术论文自动追踪与简报生成系统 — 项目设计文档

## 一、项目概述

本项目面向研究生学者，构建一个基于 LLM Agent 的学术论文自动追踪与简报生成系统。用户通过自然语言配置研究方向、关键词、查询范围和周期，Agent 自动定期从多个学术数据源获取论文，按**最新**、**最热门**、**最相关**三类规则筛选排序，生成包含摘要、核心贡献和原文链接的结构化简报，并附上当前研究方向的近期进展综述。

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

### 3.1 意图解析模块 (Intent Parser)

将用户自然语言输入解析为结构化的任务配置对象。

**输入示例：**
> "帮我追踪大语言模型推理优化方向的论文，关注 NeurIPS、ICML 和 arXiv cs.LG，每周一早上推送，重点关注最近三个月的成果"

**输出结构：**
```json
{
  "research_direction": "大语言模型推理优化",
  "keywords": ["LLM inference", "reasoning optimization", "efficient inference"],
  "sources": ["arxiv:cs.LG", "NeurIPS", "ICML"],
  "time_range_days": 90,
  "schedule": "每周一 08:00",
  "categories": ["latest", "popular", "relevant"],
  "top_n_per_category": 5
}
```

**实现方式：** 使用 LLM Function Calling / Structured Output，将自然语言映射到 `TaskConfig` Pydantic 模型。

---

### 3.2 论文获取模块 (Fetchers)

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

使用 `APScheduler` 实现定时任务：
- 支持 cron 表达式（每周一、每天、每月等）
- 任务持久化到数据库，重启后恢复
- 支持手动触发（立即执行一次）
- 任务执行日志记录

---

### 3.6 存储模块 (Storage)

使用 SQLite（轻量，无需部署）+ ChromaDB（向量存储）：

```
数据库表：
- users          用户信息
- task_configs   任务配置
- papers         论文缓存（避免重复抓取）
- reports        历史报告
- paper_vectors  论文向量索引（ChromaDB 管理）
```

---

## 四、Agent 工作流 (LangGraph)

```
用户输入
    │
    ▼
[parse_intent] ──→ 提取结构化 TaskConfig
    │
    ▼
[confirm_config] ──→ 向用户展示解析结果，确认或修改
    │
    ▼
[save_task] ──→ 持久化任务配置，注册定时任务
    │
    ▼ (定时触发 / 手动触发)
[fetch_papers] ──→ 并发调用多个 Fetcher
    │
    ▼
[rank_papers] ──→ 分别执行三类 Ranker，各取 Top-N
    │
    ▼
[generate_summaries] ──→ 并发为每篇论文生成简报
    │
    ▼
[generate_overview] ──→ 生成整体进展综述
    │
    ▼
[format_report] ──→ 整合为完整 Markdown 报告
    │
    ▼
[deliver_report] ──→ 返回用户（终端输出 / 文件保存）
```

---

## 五、代码结构

```
academic_tracker/
│
├── main.py                      # 程序入口，CLI 交互
├── requirements.txt             # 依赖清单（含版本锁定）
├── .env.example                 # 环境变量模板
│
├── config/
│   ├── __init__.py
│   └── settings.py              # 全局配置（API keys, 数据库路径等）
│
├── agent/
│   ├── __init__.py
│   ├── graph.py                 # LangGraph 工作流定义（主 Agent）
│   ├── intent_parser.py         # 自然语言 → TaskConfig 解析
│   ├── report_generator.py      # 单篇简报 + 整体综述生成
│   └── prompts.py               # 所有 Prompt 模板
│
├── fetchers/
│   ├── __init__.py
│   ├── base.py                  # BaseFetcher 抽象类
│   ├── arxiv_fetcher.py         # arXiv API 封装
│   ├── semantic_scholar.py      # Semantic Scholar API 封装
│   └── crossref_fetcher.py      # CrossRef API 封装
│
├── rankers/
│   ├── __init__.py
│   ├── latest.py                # 最新论文排序
│   ├── popular.py               # 最热门论文排序
│   └── relevant.py              # 最相关论文排序（向量相似度）
│
├── scheduler/
│   ├── __init__.py
│   └── task_scheduler.py        # APScheduler 任务管理
│
├── storage/
│   ├── __init__.py
│   ├── models.py                # SQLAlchemy ORM 模型 / Pydantic 数据模型
│   ├── database.py              # 数据库连接与 CRUD 操作
│   └── vector_store.py          # ChromaDB 向量存储封装
│
├── utils/
│   ├── __init__.py
│   ├── deduplication.py         # 论文去重逻辑
│   └── formatting.py            # Markdown 报告格式化
│
└── tests/
    ├── test_fetchers.py
    ├── test_rankers.py
    ├── test_intent_parser.py
    └── test_report_generator.py
```

---

## 六、技术栈

| 层次 | 技术选型 | 说明 |
|------|---------|------|
| Agent 框架 | LangGraph + LangChain | 工作流编排，工具调用 |
| LLM | OpenAI GPT-4o / Claude API | 意图解析、摘要生成 |
| 向量嵌入 | OpenAI text-embedding-3-small | 相关性计算 |
| 向量数据库 | ChromaDB | 本地向量存储，无需部署 |
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

## 九、实现阶段规划

| 阶段 | 内容 | 预计工时 |
|------|------|---------|
| Phase 1 | 数据模型 + arXiv/Semantic Scholar Fetcher + 基础排序 | 1 天 |
| Phase 2 | LangGraph Agent 工作流 + 意图解析 + 报告生成 | 1.5 天 |
| Phase 3 | 向量相关性排序 + ChromaDB 集成 | 0.5 天 |
| Phase 4 | APScheduler 定时任务 + SQLite 持久化 | 0.5 天 |
| Phase 5 | CLI 交互界面 + 完整测试 + README | 0.5 天 |

**总计约 4 天可完成可演示的完整系统。**

---

## 十、扩展方向（课程展示加分项）

- **多用户支持**：每个用户独立的任务配置和报告历史
- **邮件/消息推送**：通过 SMTP 或 Telegram Bot 推送报告
- **Web UI**：用 Gradio 或 Streamlit 构建可视化界面
- **增量更新**：只处理上次运行后的新论文，避免重复
- **引用网络分析**：可视化论文引用关系图
- **多语言支持**：自动检测用户语言，输出对应语言报告
