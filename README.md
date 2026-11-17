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
