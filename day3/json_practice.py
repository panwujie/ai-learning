"""Day 3 练习：JSON 深入（8 题）

为什么今天专门练 JSON：
    你调大模型时，发出去的请求、收回来的答案，**全是 JSON**。
    第 3 周那个「设备维修知识库 Agent」，本质就是"读 JSON、拼 JSON、解析 JSON"。
    今天这 8 题练完，你再看 API 返回的那一大坨，就不会发怵了。

怎么用：
    1. 打开本文件，找到 TODO，把 pass 换成你的代码
    2. 运行：python json_practice.py
    3. 它会自动检查，打印 OK 或 X
"""

import json

# ============================================================
# 第 1 组：字符串 ↔ 字典（JSON 的基本功）
# ============================================================


def ex1_to_json_text(obj) -> str:
    """【dumps】把 Python 对象转成 JSON 字符串，中文不要转成 \\uXXXX。

    例：ex1_to_json_text({"名称": "电机"}) -> '{"名称": "电机"}'
    提示：json.dumps(obj, ensure_ascii=False)
          ensure_ascii=True（默认）会把中文变成 "\\u7535\\u673a"，人眼没法看
    """
    # TODO
    return json.dumps(obj,ensure_ascii = False)


def ex2_from_json_text(text: str) -> dict:
    """【loads】把 JSON 字符串解析成 Python 字典。

    例：ex2_from_json_text('{"a": 1, "b": [2, 3]}') -> {"a": 1, "b": [2, 3]}
    提示：json.loads(text)
    """
    # TODO
    return json.loads(text)


def ex3_parse_llm_reply(reply: dict) -> str:
    """【嵌套取值】从大模型接口返回的结构里，取出回答的正文。

    reply 长这样（简化版）：
        {"choices": [{"message": {"role": "assistant", "content": "你好"}}]}

    例：ex3_parse_llm_reply(上面的结构) -> "你好"
    提示：一层一层往下取：reply["choices"][0]["message"]["content"]
          choices 是**列表**，所以要 [0] 取第一个
    """
    # TODO
    return reply["choices"][0]["message"]["content"]


def ex4_dig(data: dict, keys: list, default=None):
    """【安全取值】按 keys 一层层往下取，中间任何一步断了就返回 default。

    例：ex4_dig({"a": {"b": 1}}, ["a", "b"]) -> 1
        ex4_dig({"a": {}}, ["a", "b"])       -> None
        ex4_dig({}, ["x"], default="缺")     -> "缺"

    提示：从 data 开始，对每个 key 用 .get(key)；如果取到的不是字典就返回 default。
          写个 for 循环，用变量 current = data 一路往下走。
    """
    # TODO
    current = data
    for key in keys:
        if not isinstance(current,dict):
            return default
        current = current.get(key)
        if current == None:
            return default
    return current


# ============================================================
# 第 2 组：从 JSON 里挖数据（真实接口就是这么用的）
# ============================================================


def ex5_count_by_state(text: str) -> dict:
    """【解析 + 统计】设备列表 JSON 字符串，统计每种状态有几台。

    text 例：'[{"state": "运行"}, {"state": "停机"}, {"state": "运行"}]'
    返回：{"运行": 2, "停机": 1}

    提示：先 json.loads 得到列表，再写个空字典计数。
          counts = {}
          for item in records:
              state = item["state"]
              counts[state] = counts.get(state, 0) + 1
    """
    # TODO
    records = json.loads(text)
    counts = {}
    for item in records:
        state = item["state"]
        counts[state] = counts.get(state, 0) + 1
    return counts

def ex6_total_power(text: str) -> float:
    """【解析 + 求和】把 JSON 里所有 power 字段加起来。

    text 例：'[{"power": 7.5}, {"power": 11}]' -> 18.5
    提示：json.loads 后遍历，累加 item["power"]。
    """
    # TODO
    records = json.loads(text)
    counts={}
    counts["power"] = 0
    for item in records:
        counts["power"] = counts["power"] + item["power"]
    return counts["power"]

def ex7_to_number(value) -> float | None:
    """【清洗】把各种脏数据转成数字，转不了返回 None。

    例：ex7_to_number("7.5kW")  -> 7.5
        ex7_to_number("14.2")   -> 14.2
        ex7_to_number(11)       -> 11.0
        ex7_to_number("")       -> None
        ex7_to_number("abc")    -> None

    提示：先判断是不是数字类型（isinstance(value, (int, float))），直接 float() 返回。
          是字符串的话，去掉单位和空白：value.strip().replace("kW", "")
          然后 try: float(...) except ValueError: return None
    """
    # TODO
    if isinstance(value,(int, float)):
        return float(value)
    else:
        value=value.strip().replace("kW","")
        try:
            return float(value)
        except ValueError: 
            return None


def ex8_extract_field(text: str, field: str) -> list:
    """【解析 + 列表推导】取出 JSON 列表里每个对象的某个字段，组成新列表。

    text  = '[{"name": "泵A", "temp": 58}, {"name": "泵B", "temp": 61}]'
    ex8_extract_field(text, "name") -> ["泵A", "泵B"]

    提示：json.loads 以后 [item[field] for item in records]
    """
    # TODO
    records = json.loads(text)
    return [item[field] for item in records]


# ============================================================ 自动检查（不要改）


def _run_checks() -> None:
    cases = [
        (1, "字典转JSON", lambda: ex1_to_json_text({"名称": "电机"}), '{"名称": "电机"}'),
        (1, "JSON带列表", lambda: ex1_to_json_text({"a": [1, 2]}), '{"a": [1, 2]}'),
        (2, "JSON转字典", lambda: ex2_from_json_text('{"a": 1, "b": [2, 3]}'),
         {"a": 1, "b": [2, 3]}),
        (3, "取回答正文",
         lambda: ex3_parse_llm_reply(
             {"choices": [{"message": {"role": "assistant", "content": "你好"}}]}),
         "你好"),
        (4, "逐层取", lambda: ex4_dig({"a": {"b": 1}}, ["a", "b"]), 1),
        (4, "中间断开", lambda: ex4_dig({"a": {}}, ["a", "b"]), None),
        (4, "自定义默认", lambda: ex4_dig({}, ["x"], default="缺"), "缺"),
        (5, "按状态计数",
         lambda: ex5_count_by_state('[{"state": "运行"}, {"state": "停机"}, {"state": "运行"}]'),
         {"运行": 2, "停机": 1}),
        (6, "功率求和", lambda: ex6_total_power('[{"power": 7.5}, {"power": 11}]'), 18.5),
        (7, "带单位", lambda: ex7_to_number("7.5kW"), 7.5),
        (7, "纯数字串", lambda: ex7_to_number("14.2"), 14.2),
        (7, "本来就是数字", lambda: ex7_to_number(11), 11.0),
        (7, "空字符串", lambda: ex7_to_number(""), None),
        (7, "无法转换", lambda: ex7_to_number("abc"), None),
        (8, "取字段",
         lambda: ex8_extract_field('[{"name": "泵A", "temp": 58}, {"name": "泵B", "temp": 61}]', "name"),
         ["泵A", "泵B"]),
    ]

    failed = set()
    ok = 0
    for number, label, call, expected in cases:
        try:
            actual = call()
        except Exception as exc:
            print(f"[{number}] X  {label}：报错了 -> {type(exc).__name__}: {exc}")
            failed.add(number)
            continue
        if actual == expected:
            ok += 1
            print(f"[{number}] OK {label}")
        else:
            print(f"[{number}] X  {label}：期望 {expected!r}，你返回 {actual!r}")
            failed.add(number)

    done = 8 - len(failed)
    print()
    print("=" * 56)
    print(f"通过检查 {ok} / {len(cases)} 条   完成题目 {done} / 8")
    if failed:
        print("还没过的题号：" + "、".join(str(n) for n in sorted(failed)))
    else:
        print("全部通过，接下来做 report.py（真实数据处理）")
    print("=" * 56)


if __name__ == "__main__":
    _run_checks()
