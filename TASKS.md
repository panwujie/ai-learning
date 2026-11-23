# TASKS · 当前任务清单

> 最后更新：2026-11-23 16:20　｜　完成一项就把 `[ ]` 改成 `[x]`
> 以后不用翻对话，看这个文件就够了。

## 总进度

- [x] D1 环境与首次 API 调用
- [x] D2 Python 语法 20 题
- [x] D3 文件 IO 与 JSON 深入
- [x] D4 Git 进阶与代码组织（本地完成；GitHub push 被网络卡住，待恢复后补）
- [x] D5 大模型能力边界
- [ ] **D6 第一个 API 程序 ← 现在在这里**

## 每次开工先跑这两条

```powershell
cd C:\Users\panda\Documents\deepseek-harness\default-workspace\ai-learning
.\.venv\Scripts\python --version
```

记住三件事：用 `.\.venv\Scripts\python`（不是系统 Python）；必须在 `ai-learning` 目录下运行；`day6\llm.py` 这类子目录文件要带上路径。

---

# D6 · 第一个 API 程序

**目标**：把 `hello_llm.py` 那种一次性脚本，升级成一个别人能 `import` 的模块，并顺带学会三件事——结构化输出、流式输出、批量成本统计。

**验收物**：一个 30 行左右能复用的 `day6/llm.py` + 一条命令跑完 50 条文本并打印总花费。

**预算**：4 小时（今天先做任务 1、2，任务 3、4 明天上午补）

---

## 任务 1 · 封装模块

文件：`day6/llm.py`（骨架已生成，`ask()` 已写好）

- [x] 跑通下面这条命令，能打印出模型回答

```powershell
.\.venv\Scripts\python -c "from day6.llm import ask; print(ask('用一句话解释 PLC'))"
```

**验收**：有回答、无报错。

**卡点**：
- `ModuleNotFoundError: No module named 'day6'` → 当前目录不是 `ai-learning`
- `RuntimeError: 没找到 DEEPSEEK_API_KEY` → `.env` 不在当前目录，或 Key 还是占位符

---

## 任务 2 · `ask_json()`：强制结构化输出

文件：`day6/llm.py` 里的 `ask_json()`（现在是 `NotImplementedError`）

- [x] 实现 `ask_json()`，要点见函数 docstring
- [x] 跑通正常用例（直接用命令行跑的，没建 `test_json.py`）：

```python
from day6.llm import ask_json

text = """把下面的设备报警整理成 JSON，字段为：设备、现象、可能原因（数组）、建议动作。
报警：3 号线 ABB ACS880 报 F0009，面板显示逆变单元过温，风扇声音异常。"""

print(ask_json(text))
```

- [x] 再故意跑一次失败用例：不给字段名 → 它自己编了 `type`/`报警内容` 字段（教训：重试救格式，救不了需求不清）

**期望结果**：拿到 dict，含 `设备`、`现象`、`可能原因`（列表）、`建议动作`。

**两个硬性要求**：
1. 调用时带 `response_format={"type": "json_object"}`，且提示词里必须出现 `json` 这个词，否则接口直接报错
2. 解析失败要重试，且**把上次的错误信息塞回提示词**；重试用尽就抛异常，不许静默返回 `{}`

**为什么重要**：这个练习是“信息抽取”，不是“问知识”——只让它整理你给的文本，它就不会编。这是第 2 周 RAG、第 3 周项目的雏形。

---

## 任务 3 · `ask_stream()`：流式输出

文件：`day6/llm.py` 里的 `ask_stream()`

- [x] 实现后跑一次，肉眼确认文字是**一点点冒出来**的（首字 0.17s / 总共 0.94s）

```powershell
.\.venv\Scripts\python -c "from day6.llm import ask_stream; ask_stream('写 150 字介绍设备巡检')"
```

**验收**：不是等 2 秒后一次性全出，而是逐字出现；函数最终 return 完整文本。

**提示**：`stream=True` 返回迭代器；每块在 `chunk.choices[0].delta.content`，最后可能是 `None`；打印用 `print(..., end="", flush=True)`。

---

## 任务 4 · 批量 50 条 + 成本统计

文件：`day6/batch_cost.py`

- [x] 造 50 条设备报警文本（模板批量生成即可，别手打）
- [x] 用 `ask_json()` 逐条分类：机械 / 电气 / 工艺 / 其他
- [x] 累计 `LAST_USAGE`，统计总 token、总花费、平均耗时
- [x] 结果写成 `day6/batch_result.csv`（50 条 ok，实测 0.00046 元/条）

**验收**：一条命令跑完，终端打印类似：

```
50 条完成，失败 0 条，总耗时 63.2 秒
输入 8123 token，输出 4102 token，合计 0.049 元
平均每条约 0.001 元
```

**为什么做**：这个数字就是第 3 周评估的预算依据——30 条测试集跑一遍要几分钱，你才知道“评估可以做很多次”。

---

## D6 收尾

- [ ] `git add day6/` + `git commit -m "Day 6: 封装 LLM 客户端 + 结构化/流式/批量"`
- [ ] 把上面的勾选状态更新一遍

---

## 卡点对照表

| 现象 | 原因 | 处理 |
|---|---|---|
| `ModuleNotFoundError: day6` | 不在 `ai-learning` 目录 | `cd` 过去 |
| `No module named 'openai'` | 用了系统 Python | 改用 `.\.venv\Scripts\python` |
| `RuntimeError: 没找到 DEEPSEEK_API_KEY` | `.env` 缺失或占位符 | 检查 `ai-learning/.env` |
| `response_format` 报错 | 提示词里没出现 `json` 这个词 | 提示词明确写“返回 JSON” |
| `json.JSONDecodeError` | 模型多写了说明文字 | 重试 + 把错误塞回提示词 |
| 流式没有“打字机”效果 | 忘了 `flush=True` | 加上 |
| GitHub push 失败 | 网络（curl 52 / 连接重置） | 本地先 commit，网络好了再推 |

## 工作纪律（自己定的，别忘）

1. **不做笔记**，只维护这个 `TASKS.md` 和一个能跑的产出
2. **卡住超过 40 分钟**就换任务，或把报错原文贴给 AI
3. 每天结束时 **至少有一次 commit**
4. 卡点写进 commit message 或这个文件的“卡点对照表”，别留在脑子里
