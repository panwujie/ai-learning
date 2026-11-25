# ai-learning

记录 4 周 AI 学习计划里的代码与笔记。

## 第 1 天：环境与第一个 API 调用

目标：能把一个 Python 项目从零跑起来，并成功调用一次大模型。

### 步骤

1. **建虚拟环境**（每个项目一个，互不污染）

   ```powershell
   cd C:\Users\panda\Documents\deepseek-harness\default-workspace\ai-learning
   python -m venv .venv
   ```

2. **激活**（激活后命令行前面会出现 `(.venv)`）

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   如果报「禁止运行脚本」，执行一次：

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```

3. **装依赖**

   ```powershell
   pip install openai python-dotenv
   ```

4. **配置 Key**

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

   把 `sk-xxx` 换成你在 https://platform.deepseek.com 创建的 Key，保存。

5. **运行**

   ```powershell
   python hello_llm.py
   ```

### 验收标准

- 终端打印出大模型对「什么是电气自动化」的回答
- 打印出 token 用量和花费
- 出现 `[OK] 环境是通的`

### 排错

| 现象 | 原因 |
|---|---|
| `No module named openai` | 忘了激活虚拟环境，或忘了 pip install |
| `AuthenticationError` | Key 错了 / 有空格 / 已失效 |
| `Insufficient Balance` | 账户没余额（DeepSeek 需要充值，几块钱够用很久） |
| 连接超时 | 网络或代理问题 |

### 今日拓展（有时间再做）

- 把 `temperature` 改成 1，再跑一次，对比两次回答有什么不同
- 把 `PROMPT` 换成你自己想问的问题
- 看看 `.env` 里的 `LLM_MODEL` 改成别的模型会怎样

## 第 4 天：仓库结构与分支

- 密钥不进仓库：`.env` 由 `.gitignore` 拦下，仓库里只留 `.env.example`
- 分支只练一件事：在 `feature/readme-day4` 上改这个 README，再用 `--no-ff` 合回 `main`，让历史图里留下一个合并节点
- 代码按职责拆文件：读数据、算数据、输出结果各归各的，别写成一个 500 行的 main.py

## 目录分工

| 路径 | 内容 |
|---|---|
| `hello_llm.py` | Day 1：最小可用的 API 调用 + 用量与花费统计 |
| `day2_exercises.py` | Day 2：20 道语法练习 |
| `day3/` | Day 3：CSV 读取与清洗（`csv_loader.py`）、报告生成（`report.py`） |
| `day5/` | Day 5：token 计费实验、温度与幻觉实验 |
| `day6/` | Day 6：可复用的 LLM 客户端（`llm.py`）、批量抽取与成本统计 |
| `TASKS.md` | 当前任务清单，每日更新 |

运行方式统一用项目自己的虚拟环境，模块脚本用 `-m` 启动：

```powershell
.\.venv\Scripts\python -m day6.batch_cost
```
