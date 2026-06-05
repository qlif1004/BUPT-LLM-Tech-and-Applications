# 学术论文自动追踪与简报生成 Agent

这是一个面向研究生学者的课程设计演示项目。系统可以根据自然语言任务自动解析研究方向、关键词、来源和时间范围，抓取 arXiv 与 Semantic Scholar 论文，并生成“最新 / 最热门 / 最相关”三类学术简报。

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

## 2. 配置 DeepSeek API Key

推荐使用 `.env` 文件或环境变量，不要把真实密钥提交到代码中。

```bash
python main.py init-env
```

然后编辑 `.env`：

```bash
DEEPSEEK_API_KEY=你的_deepseek_api_key
SEMANTIC_SCHOLAR_API_KEY=可选_semantic_scholar_api_key
```

也可以临时使用环境变量：

```bash
export DEEPSEEK_API_KEY="你的_deepseek_api_key"
```

## 3. 立即生成简报

```bash
python main.py run "帮我追踪大语言模型推理优化方向的论文，关注 arXiv cs.LG 和 Semantic Scholar，最近三个月，每类给我 5 篇" -y
```

生成的报告会保存到 `reports/` 目录。

## 4. 定时任务与交互界面

新增一个周期追踪任务：

```bash
python main.py task "帮我每周一 08:00 追踪 RAG 和大语言模型检索增强方向，最近一个月，每类 5 篇" -y
```

启动常驻调度服务，服务会从 SQLite 恢复已保存的周期任务：

```bash
python main.py scheduler
```

查看、触发和审计任务：

```bash
python main.py list-tasks
python main.py run-task 1
python main.py logs
python main.py reports
```

打开 Rich 终端交互界面：

```bash
python main.py ui
```

支持的定时规则示例：

- `weekly mon 08:00`
- `每天 09:00`
- `每月 1号 08:30`
- `cron: 0 8 * * mon`

## 5. 当前实现范围

- 自然语言任务解析：DeepSeek API，失败时自动降级为规则解析
- 数据源：arXiv API、Semantic Scholar API
- 限流处理：顺序请求、请求间隔、429/503 自动等待重试、本地 6 小时缓存
- Semantic Scholar：支持可选 `SEMANTIC_SCHOLAR_API_KEY`，用于降低 429 限流概率
- 论文去重：DOI / 外部 ID / 标题
- 排序规则：最新、最热门、最相关
- 报告生成：单篇论文中文简报 + 近期研究进展综述
- 存储：SQLite 缓存任务、论文、报告和任务运行日志
- 调度器：APScheduler 周期任务、SQLite 持久化、重启恢复、手动触发
- 交互界面：Rich 终端菜单，可新增任务、查看任务、触发任务、查看日志和历史报告

## 6. 目录结构

```text
academic_tracker/
├── agent/              # DeepSeek 客户端、意图解析、Agent 编排、报告生成
├── config/             # 配置读取
├── fetchers/           # arXiv / Semantic Scholar 数据源
├── rankers/            # 最新 / 热门 / 相关排序器
├── scheduler/          # 定时任务封装
├── storage/            # 数据模型和 SQLite 持久化
└── utils/              # 去重与报告文件保存
```
