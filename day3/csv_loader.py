"""从 CSV 读原始行，返回 list[dict]。"""

import csv


def to_number(value):
    """把 "7.5"、"22kW"、7.5、"" 统一转成 float 或 None。"""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace("kW", "").replace("KW", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def clean_rows(rows: list) -> list:
    """清洗原始行（已写好，不用改）。

    做四件事：
        - 功率/电流/温度转成数字，空值变 None
        - 温度大于 200 视为传感器故障，变 None
        - 名称空的填 "未命名"
        - 五项完全相同的重复行只保留第一条
    """
    cleaned = []
    seen = set()

    for item in rows:
        power = to_number(item["功率"])
        current = to_number(item["电流"])
        temp = to_number(item["温度"])

        if temp is not None and temp > 200:
            temp = None

        name = item["名称"].strip()
        if not name:
            name = "未命名"

        fingerprint = (name, item["类型"], power, current, temp)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)

        cleaned.append({
            "设备编号": item["设备编号"],
            "名称": name,
            "类型": item["类型"],
            "功率": power,
            "电流": current,
            "温度": temp,
            "状态": item["状态"].strip(),
        })

    return cleaned



def load_rows(path: str) -> list:
    """读 CSV，返回 [{列名: 值, ...}, ...]。"""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)