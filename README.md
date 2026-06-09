# BUPT 大语言模型技术及应用：学术论文自动追踪与简报生成 Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Course%20Project-brightgreen)](#项目状态)
[![Web](https://img.shields.io/badge/Web-FastAPI-009688)]()

一个面向研究生、科研人员与课程项目场景的学术论文追踪 Agent。用户可以用自然语言描述研究方向、关键词、数据源、时间范围与周期规则，系统会自动从 arXiv 与 Semantic Scholar 获取候选论文，完成去重、排序、摘要生成与 Markdown 简报输出。

本项目来源于"BUPT 大语言模型技术及应用"课程实践，重点展示 LLM Agent 在科研信息获取、结构化任务解析、自动化报告生成和周期任务调度中的应用。

---

## 目录

- [核心能力](#核心能力)
- [系统架构](#系统架构)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [使用指南](#使用指南)
- [命令行参考](#命令行参考)
- [Web 前端](#web-前端)
- [输出结果](#输出结果)
- [项目结构](#项目结构)
- [测试](#测试)
- [项目状态](#项目状态)
- [路线图](#路线图)

---

## 核心能力

- **自然语言任务解析**：将自然语言需求解析为结构化 TaskConfig
- **自然语言指令路由**：识别用户意图（10 种意图），自动分发到对应模块
- **多数据源论文获取**：支持 arXiv 与 Semantic Scholar
- **请求限流与缓存**：重试等待、本地缓存（6小时 TTL）
- **论文去重**：基于 DOI、外部 ID 与标题稳定键
- **多维度排序**：最新、热门、相关三类排序视角
- **中文学术简报生成**：论文摘要、方法亮点、贡献解读
- **整体研究进展综述**：方向级综述
- **持久化任务调度**：手动运行、周期任务、调度服务、历史报告和运行日志
- **配置确认流程**：CLI 和 Web 均支持展示解析配置后由用户选择确认/修改/取消
- **Rich 终端交互界面**
- **Web 前端**：ChatGPT 风格对话 + 报告管理 + 定时任务管理（三页面 SPA）

---

## 系统架构

```text
用户交互层
├── CLI (main.py + Rich)
└── Web UI (server.py + FastAPI + static/index.html)
           │
           ▼
NL Router (nl_router.py) — 意图分类 + 参数提取
           │
           ▼
Agent 编排层 (graph.py)
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
  └── Markdown 报告 → reports/
```

---

## 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python 3.10+ |
| LLM 服务 | DeepSeek API |
| Web 框架 | FastAPI + uvicorn |
| CLI / TUI | argparse, Rich |
| 配置管理 | pydantic-settings, python-dotenv |
| 数据模型 | Pydantic v2 |
| HTTP 客户端 | httpx |
| 学术数据源 | arXiv API, Semantic Scholar API |
| 调度 | APScheduler |
| 数据存储 | SQLite, SQLAlchemy |
| 报告格式 | Markdown |
| 前端 | Vanilla HTML/CSS/JS + marked.js |
| 测试 | pytest |

---

## 快速开始

### 1. 进入项目目录

```bash
cd BUPT-LLM-Tech-and-Applications
```

### 2. 激活虚拟环境

```bash
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 初始化配置文件

```bash
python main.py init-env
```

### 5. 生成第一份简报

```bash
python main.py run "追踪大语言模型推理优化方向的论文，最近三个月，每类5篇" -y
```

### 6. 启动 Web 前端

```bash
venv\Scripts\python.exe -m uvicorn server:app --host 127.0.0.1 --port 8080
```

---

## 使用指南

### 立即运行一次论文追踪

```bash
python main.py run "追踪最近一个月多模态检索方向的论文，每类推荐5篇" -y
```

不加 -y 时，程序会显示解析后的任务配置，并询问是否继续执行（可选择确认/修改/取消）。

### 创建周期任务

```bash
python main.py task "每周一 08:00 追踪 RAG 和大语言模型检索增强方向，最近一个月，每类5篇" -y
```

### 启动调度服务

```bash
python main.py scheduler
```

### 查看任务、日志和历史报告

```bash
python main.py list-tasks
python main.py logs
python main.py reports
```

### 手动触发已有任务

```bash
python main.py run-task 1
```

### 自然语言指令

```bash
python main.py nl "显示我的任务列表"
python main.py nl "创建一个每周一追踪大语言模型推理优化的任务"
```

### 打开交互式 Agent Console

```bash
python main.py ui
```

---

## 命令行参考

```text
python main.py init-env [--api-key API_KEY]
python main.py run [query] [-y]
python main.py task [query] [-y]
python main.py run-task <task_id>
python main.py list-tasks
python main.py logs
python main.py reports
python main.py scheduler
python main.py ui
python main.py nl [query]
```

| 命令 | 作用 |
|------|------|
| init-env | 创建 .env 配置文件 |
| run | 根据自然语言任务立即生成一份简报 |
| task | 新增一个持久化周期追踪任务 |
| run-task | 立即触发一个已保存任务 |
| list-tasks | 查看已保存任务 |
| logs | 查看最近任务运行日志 |
| reports | 查看历史报告摘要 |
| scheduler | 启动常驻调度服务 |
| ui | 打开 Rich 终端交互界面 |
| nl | 自然语言指令路由 |

---

## Web 前端

启动 Web 服务器：

```bash
venv\Scripts\python.exe -m uvicorn server:app --host 127.0.0.1 --port 8080
```

浏览器访问 http://127.0.0.1:8080，左侧导航包含三个标签页：

### 对话页
- ChatGPT 风格对话界面
- search/schedule 意图先展示解析后的配置，用户可选择确认执行、修改配置或取消
- 修改模式在对话气泡中直接编辑配置字段

### 报告页
- 展示历史报告卡片列表
- 点击查看完整 Markdown 渲染内容
- 支持删除报告

### 定时任务页
- 表格展示已保存的任务
- 支持删除任务

### Web API 端点

| 方法 | 路径 | 功能 |
|------|------|------|
| POST | /api/chat | 自然语言指令路由 |
| GET | /api/reports | 历史报告列表 |
| GET | /api/reports/{id} | 单篇报告详情 |
| DELETE | /api/reports/{id} | 删除报告 |
| GET | /api/tasks | 定时任务列表 |
| DELETE | /api/tasks/{id} | 删除定时任务 |

---

## 输出结果

系统输出为 Markdown 格式报告，默认保存在 reports/ 目录。报告包含：

- 最新论文列表
- 热门论文列表
- 最相关论文列表
- 每篇论文的中文简报
- 作者、来源、发布时间、引用数、链接等元数据
- 研究方向近期进展综述

---

## 项目结构

```text
.
├── academic_tracker/
│   ├── agent/
│   │   ├── deepseek_client.py
│   │   ├── graph.py
│   │   ├── intent_parser.py
│   │   ├── nl_router.py
│   │   └── report_generator.py
│   ├── config/settings.py
│   ├── fetchers/
│   │   ├── arxiv_fetcher.py
│   │   ├── base.py
│   │   └── semantic_scholar.py
│   ├── rankers/
│   │   ├── latest.py
│   │   ├── popular.py
│   │   └── relevant.py
│   ├── scheduler/task_scheduler.py
│   ├── storage/
│   │   ├── database.py
│   │   └── models.py
│   ├── tests/test_core.py
│   └── utils/
│       ├── deduplication.py
│       └── formatting.py
├── server.py
├── static/index.html
├── data/         (不提交)
├── reports/      (报告输出)
├── .env.example
├── DESIGN.md
├── main.py
├── README.md
└── requirements.txt
```

---

## 测试

```bash
pytest academic_tracker/tests
```

---

## 项目状态

当前版本适合作为课程项目、科研辅助原型和 Agent 工程实践示例使用。已实现的主要能力包括：

- 自然语言任务解析与指令路由
- arXiv 与 Semantic Scholar 数据获取
- 论文去重与三维度排序
- 中文 Markdown 简报生成
- SQLite 持久化
- 周期任务调度（APScheduler）
- Rich CLI 交互界面
- Web 前端（对话 + 报告管理 + 任务管理）
- 配置确认/修改/取消流程（CLI + Web）

---

## 路线图

- [ ] 更多学术数据源（CrossRef、PubMed、OpenAlex）
- [ ] 向量数据库（ChromaDB）提升相关性排序
- [ ] 邮件、企业微信等报告推送
- [ ] 增强 Prompt 评估与报告质量评测
- [ ] GitHub Actions 自动测试
- [ ] 多用户支持
- [ ] 增量更新
