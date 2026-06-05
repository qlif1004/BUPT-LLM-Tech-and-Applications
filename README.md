# BUPT 大语言模型技术及应用：学术论文自动追踪与简报生成 Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-TBD-lightgrey)](#license)
[![Status](https://img.shields.io/badge/Status-Course%20Project-brightgreen)](#项目状态)

一个面向研究生、科研人员与课程项目场景的学术论文追踪 Agent。用户可以用自然语言描述研究方向、关键词、数据源、时间范围与周期规则，系统会自动从 arXiv 与 Semantic Scholar 获取候选论文，完成去重、排序、摘要生成与 Markdown 简报输出。

本项目来源于“BUPT 大语言模型技术及应用”课程实践，重点展示 LLM Agent 在科研信息获取、结构化任务解析、自动化报告生成和周期任务调度中的应用。

---

## 目录

- [核心能力](#核心能力)
- [系统架构](#系统架构)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [使用指南](#使用指南)
- [命令行参考](#命令行参考)
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
- **多数据源论文获取**：支持 arXiv 与 Semantic Scholar，并预留统一 Fetcher 接口便于扩展。
- **请求限流与缓存**：对外部 API 采用顺序请求、重试等待与本地缓存策略，降低 429/503 风险。
- **论文去重**：基于 DOI、外部 ID 与标题稳定键合并重复论文，并保留更有信息量的记录。
- **多维排序**：支持“最新”“热门”“相关”三类排序视角。
- **中文学术简报生成**：为论文生成中文摘要、方法亮点、贡献解读与原文链接。
- **整体研究进展综述**：基于本轮筛选论文生成方向级综述。
- **持久化任务调度**：支持手动运行、周期任务、调度服务、历史报告和运行日志。
- **Rich 终端交互界面**：提供命令式与自然语言混合交互体验。

---

## 系统架构

```text
用户自然语言需求
      │
      ▼
IntentParser
自然语言 → TaskConfig
      │
      ▼
AcademicTrackerAgent
任务编排 / 数据获取 / 排序 / 报告生成
      │
      ├── Fetchers
      │   ├── arXiv
      │   └── Semantic Scholar
      │
      ├── Rankers
      │   ├── LatestRanker
      │   ├── PopularRanker
      │   └── RelevanceRanker
      │
      ├── ReportGenerator
      │   ├── 单篇论文中文简报
      │   └── 方向级研究综述
      │
      └── Storage / Scheduler
          ├── SQLite 持久化
          ├── APScheduler 周期调度
          ├── 任务配置
          ├── 论文缓存
          ├── 历史报告
          └── 运行日志
```

核心数据流：

1. 用户输入自然语言追踪需求。
2. `IntentParser` 解析为 `TaskConfig`。
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
| CLI / TUI | argparse, Rich |
| 配置管理 | pydantic-settings, python-dotenv |
| 数据模型 | Pydantic v2 |
| HTTP 客户端 | httpx |
| 学术数据源 | arXiv API, Semantic Scholar API |
| 调度 | APScheduler |
| 数据存储 | SQLite, SQLAlchemy |
| 报告格式 | Markdown |
| LLM 服务 | DeepSeek API |

---

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/qlif1004/BUPT-LLM-Tech-and-Applications.git
cd BUPT-LLM-Tech-and-Applications
```

如果你是在当前本地目录开发，也可以直接进入项目目录：

```bash
cd /home/wyd/llmtech
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
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

然后编辑 `.env`：

```bash
DEEPSEEK_API_KEY=你的_deepseek_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
SEMANTIC_SCHOLAR_API_KEY=
DATABASE_URL=sqlite:///data/academic_tracker.db
REPORT_DIR=reports
DEFAULT_MAX_RESULTS=30
```

### 5. 生成第一份简报

```bash
python main.py run "帮我追踪大语言模型推理优化方向的论文，关注 arXiv cs.LG 和 Semantic Scholar，最近三个月，每类给我 5 篇" -y
```

生成的 Markdown 报告会保存到 `reports/` 目录。

---

## 配置说明

项目通过 `.env` 或系统环境变量读取配置。推荐复制或生成 `.env` 后在本地填写，不要提交真实密钥。

| 变量名 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `DEEPSEEK_API_KEY` | 是 | 空 | DeepSeek API Key，用于意图解析与报告生成。 |
| `DEEPSEEK_BASE_URL` | 否 | `https://api.deepseek.com` | DeepSeek API 地址。 |
| `DEEPSEEK_MODEL` | 否 | `deepseek-v4-pro` | 使用的 DeepSeek 模型名称。`.env.example` 中给出的是 `deepseek-chat` 示例，可按账户可用模型调整。 |
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

不加 `-y` 时，程序会展示解析后的任务配置，并询问是否继续执行。

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

### 支持的调度规则示例

```text
weekly mon 08:00
每天 09:00
每月 1号 08:30
cron: 0 8 * * mon
```

---

## 输出结果

系统输出为 Markdown 格式报告，默认保存在 `reports/` 目录。报告通常包含：

- 任务配置摘要
- 最新论文列表
- 热门论文列表
- 最相关论文列表
- 每篇论文的中文简报
- 作者、来源、发布时间、引用数、链接等元数据
- 研究方向近期进展综述

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
│   │   └── report_generator.py       # 论文摘要与报告生成
│   ├── config/
│   │   └── settings.py               # 环境变量与全局配置
│   ├── fetchers/
│   │   ├── arxiv_fetcher.py          # arXiv 数据源
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
│   │   └── models.py                 # Pydantic 数据模型
│   ├── tests/
│   │   └── test_core.py              # 核心逻辑测试
│   └── utils/
│       ├── deduplication.py          # 论文去重
│       └── formatting.py             # 报告文件保存
├── data/                             # 本地数据库与缓存，默认不提交
├── reports/                          # Markdown 报告输出
├── .env.example                      # 环境变量模板
├── .gitignore
├── DESIGN.md                         # 项目设计说明
├── main.py                           # CLI 入口
├── README.md
└── requirements.txt
```

---

## 数据与安全

请特别注意以下安全约束：

- 不要提交 `.env` 或任何真实 API Key。
- 不要提交本地数据库、缓存、大规模论文数据或模型权重。
- 本仓库的 `.gitignore` 已默认排除：
  - `.env`
  - `data/`
  - `*.db`, `*.sqlite`, `*.sqlite3`
  - Python 缓存与虚拟环境
- 如果 Token、API Key 或密码曾经出现在聊天记录、终端截图或 Git 历史中，应立即撤销并重新生成。
- 外部学术 API 可能有速率限制，请合理设置查询频率和候选论文数量。

---

## 测试

项目包含核心单元测试，例如论文去重和相关性排序。

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

- `DEEPSEEK_API_KEY` 是否正确；
- `DEEPSEEK_MODEL` 是否为当前账户可用模型；
- 网络是否可以访问 DeepSeek API；
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

`data/` 已被 `.gitignore` 忽略，数据库和缓存不会提交。`reports/` 当前没有默认忽略，因为它可以作为课程项目产出展示。如果报告包含敏感信息，请在提交前手动检查。

---

## 项目状态

当前版本适合作为课程项目、科研辅助原型和 Agent 工程实践示例使用。已实现的主要能力包括：

- 自然语言任务解析；
- arXiv 与 Semantic Scholar 数据获取；
- 论文去重；
- 最新、热门、相关排序；
- 中文 Markdown 简报生成；
- SQLite 持久化；
- 周期任务调度；
- Rich 终端交互。

当前尚未定位为生产级 SaaS 服务，缺少多用户权限体系、Web UI、完整 CI/CD、安全审计和大规模并发处理能力。

---

## 路线图

后续可扩展方向：

- [ ] 接入更多学术数据源，例如 CrossRef、PubMed、OpenAlex。
- [ ] 增加 Web UI 或 Dashboard。
- [ ] 支持邮件、企业微信、飞书等报告推送渠道。
- [ ] 引入向量数据库，提升相关性排序质量。
- [ ] 增强 Prompt 评测与报告质量评估。
- [ ] 增加 GitHub Actions 自动测试。
- [ ] 增加更细粒度的日志、错误分类和重试策略。
- [ ] 支持多用户、多任务隔离和权限管理。

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

- 提交真实密钥或私人 Token；
- 提交本地缓存、数据库、大文件；
- 在报告中包含未授权转载内容或隐私信息；
- 将尚未实现的能力描述为已实现功能。

---

## License

当前仓库尚未声明开源许可证。正式开源前建议补充 `LICENSE` 文件，并明确代码、报告和数据的使用范围。

如果只是课程展示，可在仓库描述或文档中说明“仅用于课程学习与研究演示”。
