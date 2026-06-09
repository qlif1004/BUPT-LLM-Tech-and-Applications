# BUPT 大语言模型技术及应用：学术论文自动追踪与简报生成 Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Course%20Project-brightgreen)](#项目状态)
[![Web](https://img.shields.io/badge/Web-FastAPI-009688)](#web-前端)
[![License](https://img.shields.io/badge/License-TBD-lightgrey)](#license)

一个面向研究生、科研人员与课程项目场景的学术论文追踪 Agent。用户可以用自然语言描述研究方向、关键词、数据源、时间范围与周期规则，系统会自动从 arXiv、DBLP 与 Semantic Scholar 获取候选论文，完成去重、排序、摘要生成与 Markdown 简报输出。

本项目来源于“BUPT 大语言模型技术及应用”课程实践，重点展示 LLM Agent 在科研信息获取、结构化任务解析、自然语言指令路由、自动化报告生成和周期任务调度中的应用。

---

## 目录

- [核心能力](#核心能力)
- [系统架构](#系统架构)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [使用指南](#使用指南)
- [命令行参考](#命令行参考)
- [Web 前端](#web-前端)
- [输出结果](#输出结果)
- [项目结构](#项目结构)
- [数据与安全](#数据与安全)
- [测试](#测试)
- [常见问题](#常见问题)
- [项目状态](#项目状态)
- [路线图](#路线图)
- [贡献指南](#贡献指南)
- [License](#license)

---

## 核心能力

- **自然语言任务解析**：将“追踪最近三个月 RAG 方向高影响论文”等自然语言需求解析为结构化 `TaskConfig`。
- **自然语言指令路由**：识别 search / schedule / list_tasks / trigger_task / view_logs / view_reports / start_scheduler / help / exit / unrelated 等意图，并自动分发到对应模块。
- **多数据源论文获取**：支持 arXiv、DBLP 与 Semantic Scholar，并预留统一 Fetcher 接口便于扩展。
- **请求限流与缓存**：对外部 API 采用重试等待与本地缓存策略，降低 429/503 风险。
- **论文去重**：基于 DOI、外部 ID 与标题稳定键合并重复论文，并保留更有信息量的记录。
- **多维排序**：支持“最新”“热门”“相关”三类排序视角。
- **中文学术简报生成**：为论文生成中文摘要、方法亮点、贡献解读与原文链接。
- **整体研究进展综述**：基于本轮筛选论文生成方向级综述。
- **持久化任务调度**：支持手动运行、周期任务、调度服务、历史报告和运行日志。
- **配置确认流程**：CLI 和 Web 均支持展示解析配置后由用户选择确认、修改或取消。
- **Rich 终端交互界面**：提供命令式与自然语言混合交互体验。
- **Web 前端**：ChatGPT 风格对话 + 报告管理 + 定时任务管理（三页面 SPA）。

---

## 系统架构

```text
用户交互层
├── CLI / Rich Console (main.py)
└── Web UI (server.py + FastAPI + static/index.html)
           │
           ▼
NL Router (nl_router.py) — 意图分类 + 参数提取
           │
           ▼
Agent 编排层 (graph.py)
  ├── IntentParser      自然语言 → TaskConfig
  ├── NLRouter          自然语言 → 系统功能路由
  └── ReportGenerator   单篇摘要 + 方向综述
           │
    ┌──────┼──────────┐
    ▼      ▼          ▼
Fetchers   Rankers    Scheduler
arXiv      Latest     APScheduler
DBLP       Popular    SQLite
S2         Relevant
           │
           ▼
Storage + Reports
  ├── SQLite (task_configs, papers, reports, task_runs)
  └── Markdown 报告 → reports/
```

核心数据流：

1. 用户输入自然语言追踪需求或管理指令。
2. `NLRouter` 识别功能意图；检索/调度类需求由 `IntentParser` 解析为 `TaskConfig`。
3. Fetcher 从目标数据源获取候选论文。
4. 系统对论文进行去重与多维排序。
5. `ReportGenerator` 调用 LLM 生成中文简报与综述。
6. 结果保存到 `reports/`，元数据写入 SQLite。
7. 对周期任务，APScheduler 根据规则自动触发后续运行。

---

## 技术栈

| 类别 | 技术 |
| --- | --- |
| 语言 | Python 3.10+ |
| LLM 服务 | DeepSeek API |
| Web 框架 | FastAPI + uvicorn |
| CLI / TUI | argparse, Rich |
| 配置管理 | pydantic-settings, python-dotenv |
| 数据模型 | Pydantic v2 |
| HTTP 客户端 | httpx |
| 学术数据源 | arXiv API, DBLP Search API, Semantic Scholar API |
| 调度 | APScheduler |
| 数据存储 | SQLite, SQLAlchemy |
| 报告格式 | Markdown |
| 前端 | Vanilla HTML/CSS/JS + marked.js |
| 测试 | pytest, pytest-asyncio |

---

## 快速开始

### 1. 克隆或进入项目目录

```bash
git clone https://github.com/qlif1004/BUPT-LLM-Tech-and-Applications.git
cd BUPT-LLM-Tech-and-Applications
```

如果你已经在当前本地仓库中开发，直接进入项目目录即可。

### 2. 创建并激活虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell 可使用：

```bash
.venv\Scripts\Activate.ps1
```

如果你使用 Conda：

```bash
conda create -n academic-tracker python=3.10 -y
conda activate academic-tracker
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 初始化配置文件

```bash
python main.py init-env
```

然后编辑 `.env`，至少填写 DeepSeek API Key。

### 5. 生成第一份简报

```bash
python main.py run "帮我追踪大语言模型推理优化方向的论文，关注 arXiv cs.LG、dblp:WWW 和 Semantic Scholar，最近三个月，每类给我 5 篇" -y
```

生成的 Markdown 报告会保存到 `reports/` 目录。

### 6. 启动 Web 前端

```bash
python -m uvicorn server:app --host 127.0.0.1 --port 8080
```

浏览器访问 [http://127.0.0.1:8080](http://127.0.0.1:8080)。

---

## 配置说明

项目通过 `.env` 或系统环境变量读取配置。推荐复制或生成 `.env` 后在本地填写，不要提交真实密钥。

| 变量名 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `DEEPSEEK_API_KEY` | 是 | 空 | DeepSeek API Key，用于意图解析与报告生成。 |
| `DEEPSEEK_BASE_URL` | 否 | `https://api.deepseek.com` | DeepSeek API 地址。 |
| `DEEPSEEK_MODEL` | 否 | 以代码配置为准 | 使用的 DeepSeek 模型名称，可按账户可用模型调整。 |
| `SEMANTIC_SCHOLAR_API_KEY` | 否 | 空 | Semantic Scholar API Key。填写后可降低限流概率。 |
| `DATABASE_URL` | 否 | `sqlite:///data/academic_tracker.db` | SQLite 数据库路径。 |
| `REPORT_DIR` | 否 | `reports` | Markdown 报告输出目录。 |
| `DEFAULT_MAX_RESULTS` | 否 | `30` | 每个数据源默认候选论文数。 |
| `REQUEST_TIMEOUT` | 否 | `60.0` | 外部请求超时时间，单位为秒。 |

也可以临时使用环境变量：

```bash
export DEEPSEEK_API_KEY="你的_deepseek_api_key"
python main.py run "追踪最近 30 天 RAG 与长上下文推理方向的高影响论文" -y
```

---

## 使用指南

### 立即运行一次论文追踪

```bash
python main.py run "帮我追踪最近一个月多模态检索方向的论文，每类推荐 5 篇" -y
```

不加 `-y` 时，程序会显示解析后的任务配置，并询问是否继续执行，可选择确认、修改或取消。

### 创建周期任务

```bash
python main.py task "帮我每周一 08:00 追踪 RAG 和大语言模型检索增强方向，最近一个月，每类 5 篇" -y
```

如果自然语言中没有明确周期规则，程序会提示你输入调度表达式。

### 启动调度服务

```bash
python main.py scheduler
```

调度服务会从 SQLite 恢复已保存的周期任务。服务运行期间请保持进程常驻，按 `Ctrl+C` 可退出。

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

其中 `1` 是任务 ID，可通过 `list-tasks` 查看。

### 自然语言指令

```bash
python main.py nl "显示我的任务列表"
python main.py nl "创建一个每周一追踪大语言模型推理优化的任务"
python main.py nl "查看最近运行日志"
```

### 打开交互式 Agent Console

```bash
python main.py ui
```

在交互界面中可以直接输入研究需求，也可以使用命令：

```text
task 每周一 08:00 追踪多模态大模型论文
tasks
run-task 1
logs
reports
scheduler
help
exit
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
| --- | --- |
| `init-env` | 创建 `.env` 配置文件。 |
| `run` | 根据自然语言任务立即生成一份简报。 |
| `task` | 新增一个持久化周期追踪任务。 |
| `run-task` | 立即触发一个已保存任务。 |
| `list-tasks` | 查看已保存任务。 |
| `logs` | 查看最近任务运行日志。 |
| `reports` | 查看历史报告摘要。 |
| `scheduler` | 启动常驻调度服务。 |
| `ui` | 打开 Rich 终端交互界面。 |
| `nl` | 使用自然语言指令路由自动识别意图并执行。 |

### 支持的调度规则示例

```text
weekly mon 08:00
每天 09:00
每月 1号 08:30
cron: 0 8 * * mon
```

---

## Web 前端

启动 Web 服务器：

```bash
python -m uvicorn server:app --host 127.0.0.1 --port 8080
```

浏览器访问 [http://127.0.0.1:8080](http://127.0.0.1:8080)，左侧导航包含三个标签页。

### 对话页

- ChatGPT 风格对话界面。
- search / schedule 意图先展示解析后的配置，用户可选择确认执行、修改配置或取消。
- 修改模式支持在对话气泡中直接编辑配置字段。

### 报告页

- 展示历史报告卡片列表。
- 点击查看完整 Markdown 渲染内容。
- 支持删除报告。

### 定时任务页

- 表格展示已保存的任务。
- 支持删除任务。

### Web API 端点

| 方法 | 路径 | 功能 |
| --- | --- | --- |
| `POST` | `/api/chat` | 自然语言指令路由。 |
| `GET` | `/api/reports` | 历史报告列表。 |
| `GET` | `/api/reports/{id}` | 单篇报告详情。 |
| `DELETE` | `/api/reports/{id}` | 删除报告。 |
| `GET` | `/api/tasks` | 定时任务列表。 |
| `DELETE` | `/api/tasks/{id}` | 删除定时任务。 |

---

## 输出结果

系统输出为 Markdown 格式报告，默认保存在 `reports/` 目录。报告通常包含：

- 任务配置摘要。
- 最新论文列表。
- 热门论文列表。
- 最相关论文列表。
- 每篇论文的中文简报。
- 作者、来源、发布时间、引用数、链接等元数据。
- 研究方向近期进展综述。

历史报告和任务运行记录会写入 SQLite 数据库，默认路径为：

```text
data/academic_tracker.db
```

---

## 项目结构

```text
.
├── academic_tracker/
│   ├── agent/
│   │   ├── deepseek_client.py        # DeepSeek API 客户端
│   │   ├── graph.py                  # AcademicTrackerAgent 主编排逻辑
│   │   ├── intent_parser.py          # 自然语言任务解析
│   │   ├── nl_router.py              # 自然语言指令路由
│   │   ├── report_comparison.py      # 报告对比能力
│   │   └── report_generator.py       # 论文摘要与报告生成
│   ├── config/
│   │   └── settings.py               # 环境变量与全局配置
│   ├── fetchers/
│   │   ├── arxiv_fetcher.py          # arXiv 数据源
│   │   ├── dblp_fetcher.py           # DBLP 数据源
│   │   ├── base.py                   # Fetcher 抽象接口
│   │   └── semantic_scholar.py       # Semantic Scholar 数据源
│   ├── rankers/
│   │   ├── latest.py                 # 最新排序
│   │   ├── popular.py                # 热门排序
│   │   └── relevant.py               # 相关性排序
│   ├── scheduler/
│   │   └── task_scheduler.py         # APScheduler 任务调度
│   ├── storage/
│   │   ├── database.py               # SQLite / SQLAlchemy 数据访问
│   │   └── models.py                 # Pydantic 数据模型 / ORM 模型
│   ├── tests/
│   │   ├── test_core.py              # 核心逻辑测试
│   │   └── test_web_app.py           # Web API 测试
│   └── utils/
│       ├── deduplication.py          # 论文去重
│       └── formatting.py             # 报告文件保存
├── static/
│   └── index.html                    # Web 前端入口
├── server.py                         # FastAPI Web 服务
├── main.py                           # CLI 入口
├── data/                             # 本地数据库与缓存，默认不提交
├── reports/                          # Markdown 报告输出
├── .env.example                      # 环境变量模板
├── .gitignore
├── DESIGN.md                         # 项目设计说明
├── README.md
└── requirements.txt
```

---

## 数据与安全

请特别注意以下安全约束：

- 不要提交 `.env` 或任何真实 API Key。
- 不要提交本地数据库、缓存、大规模论文数据或模型权重。
- 本仓库的 `.gitignore` 已默认排除 `.env`、`data/`、`*.db`、`*.sqlite`、`*.sqlite3`、Python 缓存与虚拟环境。
- 如果 Token、API Key 或密码曾经出现在聊天记录、终端截图或 Git 历史中，应立即撤销并重新生成。
- 外部学术 API 可能有速率限制，请合理设置查询频率和候选论文数量。

---

## 测试

项目包含核心单元测试，例如论文去重、相关性排序和 Web API 行为。

安装测试工具后运行：

```bash
pip install pytest
pytest academic_tracker/tests
```

如果希望检查某个模块，可以直接运行：

```bash
pytest academic_tracker/tests/test_core.py
```

---

## 常见问题

### 1. 为什么没有生成高质量中文简报？

请检查：

- `DEEPSEEK_API_KEY` 是否正确。
- `DEEPSEEK_MODEL` 是否为当前账户可用模型。
- 网络是否可以访问 DeepSeek API。
- 论文摘要是否为空或过短。

### 2. Semantic Scholar 经常返回 429 怎么办？

可以申请并配置 `SEMANTIC_SCHOLAR_API_KEY`，同时减少查询频率或降低 `DEFAULT_MAX_RESULTS`。

### 3. 为什么任务创建了但没有自动运行？

周期任务需要启动常驻调度服务：

```bash
python main.py scheduler
```

如果服务退出，定时任务不会在后台继续执行；重新启动服务后会从 SQLite 恢复已保存任务。

### 4. 为什么 GitHub 推送卡住？

通常是 HTTPS 认证提示没有正常显示。可改用 SSH，或使用 GitHub CLI 登录。不要把 Personal Access Token 发到聊天窗口或提交到仓库。

### 5. 报告和数据库会提交到 GitHub 吗？

`data/` 已被 `.gitignore` 忽略，数据库和缓存不会提交。`reports/` 当前可作为课程项目产出展示；如果报告包含敏感信息，请在提交前手动检查。

---

## 项目状态

当前版本适合作为课程项目、科研辅助原型和 Agent 工程实践示例使用。已实现的主要能力包括：

- 自然语言任务解析与指令路由。
- arXiv、DBLP 与 Semantic Scholar 数据获取。
- 论文去重与三维度排序。
- 中文 Markdown 简报生成。
- SQLite 持久化。
- 周期任务调度（APScheduler）。
- Rich CLI 交互界面。
- Web 前端（对话 + 报告管理 + 任务管理）。
- 配置确认、修改、取消流程（CLI + Web）。

当前尚未定位为生产级 SaaS 服务，缺少多用户权限体系、完整 CI/CD、安全审计和大规模并发处理能力。

---

## 路线图

后续可扩展方向：

- [ ] 接入更多学术数据源，例如 CrossRef、PubMed、OpenAlex。
- [ ] 增强 Web UI / Dashboard 的可视化能力。
- [ ] 支持邮件、企业微信、飞书等报告推送渠道。
- [ ] 引入向量数据库，提升相关性排序质量。
- [ ] 增强 Prompt 评测与报告质量评估。
- [ ] 增加 GitHub Actions 自动测试。
- [ ] 增加更细粒度的日志、错误分类和重试策略。
- [ ] 支持多用户、多任务隔离和权限管理。
- [ ] 支持增量更新，只处理上次运行后的新论文。

---

## 贡献指南

欢迎基于课程项目继续扩展。建议遵循以下流程：

1. Fork 本仓库。
2. 创建功能分支：

```bash
git checkout -b feature/your-feature
```

3. 提交修改前运行测试：

```bash
pytest academic_tracker/tests
```

4. 提交清晰的 Commit Message。
5. 发起 Pull Request，并说明修改动机、主要实现和测试结果。

提交代码时请避免：

- 提交真实密钥或私人 Token。
- 提交本地缓存、数据库、大文件。
- 在报告中包含未授权转载内容或隐私信息。
- 将尚未实现的能力描述为已实现功能。

---

## License

当前仓库尚未声明开源许可证。正式开源前建议补充 `LICENSE` 文件，并明确代码、报告和数据的使用范围。

如果只是课程展示，可在仓库描述或文档中说明“仅用于课程学习与研究演示”。
