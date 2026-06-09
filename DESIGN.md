学术论文自动追踪与简报生成系统 —— 项目设计文档

## 一、项目概述

本项目面向研究生学者，构建一个基于 LLM Agent 的学术论文自动追踪与简报生成系统。

系统提供 CLI 命令行界面和 Web 前端两种交互方式。Web 前端通过对话式 Chat UI 支持自然语言指令路由，自动识别用户意图并分发到对应模块。

---

## 二、系统架构

```
用户交互层
├── CLI (main.py + Rich)
└── Web UI (server.py + FastAPI + static/index.html)
           │
           ▼
NL Router (nl_router.py) — 意图分类 + 参数提取
           │
           ▼
Agent 编排层 (agent/)
  ├── IntentParser      NL → TaskConfig
  ├── NLRouter          NL → 系统功能路由
  └── ReportGenerator   摘要 + 综述
           │
    ┌──────┼──────────┐
    ▼      ▼          ▼
Fetchers   Rankers    Scheduler
arXiv     Latest     APScheduler
S2        Popular    SQLite
          Relevant
           │
           ▼
Storage + Reports
  ├── SQLite (task_configs, papers, reports, task_runs)
  └── Markdown 报告输出 (reports/)
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
  "sources": ["arxiv:cs.LG", "NeurIPS", "ICML"],
  "time_range_days": 90,
  "schedule": "每周一 08:00",
  "categories": ["latest", "popular", "relevant"],
  "top_n_per_category": 5
}
```

### 3.2 自然语言指令路由 (NLRouter)

将用户的任意自然语言输入分类为系统功能意图并提取参数。支持 10 种意图：search / schedule / list_tasks / trigger_task / view_logs / view_reports / start_scheduler / help / exit / unrelated。

### 3.3 论文获取模块 (Fetchers)

支持多数据源，统一抽象为 BaseFetcher 接口。已实现 arXiv API 和 Semantic Scholar API，含请求限流、重试等待与本地缓存策略。

### 3.4 排序与筛选模块 (Rankers)

- **最新 (Latest)**：按发布日期降序
- **最热门 (Popular)**：综合评分 = citation_count × 0.8 + recency_bonus × 20.0
- **最相关 (Relevance)**：基于 TF 词频 + 余弦相似度

### 3.5 报告生成模块 (ReportGenerator)

- 单篇论文简报：3-5 句中文摘要
- 整体进展综述：方向级研究进展概览

### 3.6 任务调度模块 (Scheduler)

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
│   ├── arxiv_fetcher.py
│   ├── base.py
│   └── semantic_scholar.py
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
| CLI | Rich | 终端交互界面 |

---

## 七、Web 前端设计

前端为单页应用 (SPA)，包含三个标签页：

- **对话页**：ChatGPT 风格对话界面。search/schedule 意图先展示配置待确认
- **报告页**：历史报告卡片列表，支持查看和删除
- **定时任务页**：任务表格，支持删除

Web API 端点：

| 方法 | 路径 | 功能 |
|------|------|------|
| POST | /api/chat | 自然语言指令路由与执行 |
| GET | /api/reports | 历史报告列表 |
| GET | /api/reports/{id} | 单篇报告详情 |
| DELETE | /api/reports/{id} | 删除报告 |
| GET | /api/tasks | 定时任务列表 |
| DELETE | /api/tasks/{id} | 删除定时任务 |

---

## 八、实现阶段

| 阶段 | 内容 | 状态 |
|------|------|------|
| Phase 1 | 数据模型 + arXiv/S2 Fetcher + 基础排序 | ✅ 完成 |
| Phase 2 | Agent 工作流 + 意图解析 + 报告生成 | ✅ 完成 |
| Phase 3 | TF 相关性排序 + 论文去重 | ✅ 完成 |
| Phase 4 | APScheduler 定时任务 + SQLite 持久化 | ✅ 完成 |
| Phase 5 | CLI Rich 交互 + NL Router | ✅ 完成 |
| Phase 6 | Web 前端 + FastAPI 后端 | ✅ 完成 |

---

## 九、扩展方向

- 更多学术数据源：CrossRef、PubMed、OpenAlex
- 向量数据库：ChromaDB 集成提升相关性排序质量
- 多用户支持：用户独立的配置和报告历史
- 消息推送：邮件、企业微信、飞书等报告推送渠道
