"""Day 2 练习：Python 语法速过（20 题）

怎么用：
    1. 打开本文件，从上往下，找到 `TODO` 的地方
    2. 把 pass 删掉，换成你自己的代码
    3. 全部写完后，在终端运行：

           python day2_exercises.py

    4. 它会自动检查每道题，打印 ✓ 或 ✗。没通过的会告诉你「期望什么、你给了什么」

规则：
    - 只改函数体里 TODO 下面的部分，**不要改函数名和参数**
    - 写完一个就可以先跑一次，不用等 20 题全写完
    - 卡住了就问我，别硬耗超过 20 分钟

题目都用了电气/自动化的小场景，因为后面的项目就是这个味道。
"""

# ============================================================ 第 1 周题目


def ex01_power(voltage: float, current: float) -> float:
    """【变量与类型】电功率 P = U × I。

    例：ex01_power(220, 5.5) -> 1210.0
    """
    # TODO: 返回 电压 × 电流
    return voltage * current


def ex02_split_model(model: str) -> tuple:
    """【字符串】把型号 "PLC-1200" 拆成 ("PLC", "1200")。

    提示：用 str.split("-", 1)，它最多切一刀。
    例：ex02_split_model("S7-1200") -> ("S7", "1200")
    """
    # TODO: 返回一个二元组
    return tuple(model.split("-",1))


def ex03_format(voltage: float, current: float) -> str:
    """【f-string】输出一行中文报告。

    例：ex03_format(220, 5.5)
        -> "电压 220.0 V，电流 5.5 A，功率 1210.0 W"
    提示：数字保留 1 位小数的写法是 {值:.1f}，功率要自己算。
    """
    # TODO: 用 f-string 拼出这句话（注意逗号是中文全角，空格别丢）
    return f"电压 {voltage:.1f} V，电流 {current:.1f} A，功率 {voltage * current:.1f} W"


def ex04_minmax(nums: list) -> tuple:
    """【列表】返回 (最小值, 最大值)。

    例：ex04_minmax([3, 1, 4, 1, 5]) -> (1, 5)
    """
    # TODO: 可以用内置的 min() 和 max()
    return min(nums),max(nums)


def ex05_slice(nums: list) -> tuple:
    """【切片】返回 (前三个, 后三个)。

    例：ex05_slice([1, 2, 3, 4, 5, 6]) -> ([1, 2, 3], [4, 5, 6])
    提示：nums[:3] 是前三个，nums[-3:] 是后三个。
    """
    # TODO
    return nums[:3],nums[3:]


def ex06_ma_to_a(readings: list) -> list:
    """【列表推导式】把毫安列表换算成安培（除以 1000）。

    例：ex06_ma_to_a([500, 1000, 20]) -> [0.5, 1.0, 0.02]
    提示：一行就能写完：[x / 1000 for x in readings]
    """
    # TODO
    return [x / 1000 for x in readings]


def ex07_get_power(table: dict, motor: str):
    """【字典取值】从电机功率表里查，查不到返回字符串 "未知"。

    例：ex07_get_power({"M1": 1.5, "M2": 2.5}, "M1") -> 1.5
        ex07_get_power({"M1": 1.5, "M2": 2.5}, "M9") -> "未知"
    提示：table.get(键, 默认值)
    """
    # TODO
    return table.get(motor, "未知")


def ex08_total_power(table: dict) -> float:
    """【字典遍历】把表里所有功率加起来。

    例：ex08_total_power({"M1": 1.5, "M2": 2.5}) -> 4.0
    提示：对 dict 用 .values() 再 sum()；空字典应该返回 0（考虑加个判断）。
    """
    # TODO
    return sum(table.values())


def ex09_common(a: list, b: list) -> list:
    """【集合】返回两个列表都有的元素，去重并按从小到大排序。

    例：ex09_common([1, 2, 3, 2], [2, 3, 4]) -> [2, 3]
    提示：set(a) & set(b) 是交集，sorted() 排序。
    """
    # TODO
    return sorted(set(a) & set(b))


def ex10_alarm(temperature: float) -> str:
    """【if/elif】温度状态判断。

    小于 60 返回 "正常"；60 到 80 之间（含 60、不含 80）返回 "预警"；80 及以上返回 "报警"。

    例：ex10_alarm(59) -> "正常"
        ex10_alarm(75) -> "预警"
        ex10_alarm(95) -> "报警"
    """
    # TODO
    if temperature < 60:
        return "正常"
    elif temperature < 80:
        return "预警"
    else: 
        return "报警"


def ex11_average(nums: list) -> float:
    """【for + 累加】求平均值，空列表返回 0.0。

    例：ex11_average([1, 2, 3]) -> 2.0
        ex11_average([]) -> 0.0
    提示：先判断 len(nums) == 0。
    """
    # TODO
    sum = 0.0
    x = 0
    if len(nums) != 0:
        for x in nums:
            sum += x
        return sum/len(nums)
    else:
        return 0.0

def ex12_count_steps(start: float, limit: float, step: float) -> int:
    """【while 循环】从 start 开始，每次加 step，直到数值超过 limit，返回加了多少次。

    例：ex12_count_steps(0, 10, 3)
        0 -> 3 -> 6 -> 9 -> 12（超过 10，停）
        -> 4
    """
    # TODO: 用 while 循环
    nums = 0
    while start <= limit:
        start += step
        nums += 1
    return nums

def ex13_resistance(length: float, area: float, rho: float = 0.0175) -> float:
    """【函数默认参数】导线电阻 R = ρ × L / S，结果保留 4 位小数。

    铜的电阻率默认 0.0175（Ω·mm²/m），可以不传。

    例：ex13_resistance(100, 2.5) -> 0.7
    提示：round(值, 4)
    """
    # TODO
    return round(length*rho/area,4)


def ex14_stats(nums: list) -> tuple:
    """【返回多个值】返回 (最大值, 最小值, 平均值)。平均值要除以 len。

    例：ex14_stats([2, 4, 6]) -> (6, 2, 4.0)
    """
    # TODO: 一个 return 返回三个值，用逗号隔开就是元组
    return max(nums),min(nums),round(sum(nums)/len(nums))


# ============================================================ 进阶一点


def ex15_parse_fault(code: str):
    """【字符串方法】故障代码解析。

    以 "E" 开头的返回后面的数字（int 类型）；否则返回 None。

    例：ex15_parse_fault("E102") -> 102
        ex15_parse_fault("A1") -> None
    提示：code.startswith("E")，取后半段用 code[1:]，转数字用 int()。
    """
    # TODO
    if code[0] == "E":
        return int(code[1:])
    else:
        return None


def ex16_devices_by_status(devices: list, status: str) -> list:
    """【列表里套字典】筛出指定状态的设备名。

    devices 长这样：
        [{"name": "电机A", "status": "运行"}, {"name": "泵B", "status": "停机"}]

    例：ex16_devices_by_status(devices, "运行") -> ["电机A"]
    """
    # TODO: 用列表推导式，遍历后取 d["name"] 和 d["status"]
    return [d["name"] for d in devices if d["status"] == status]


def ex17_above_threshold(nums: list, threshold: float) -> list:
    """【推导式 + 条件】筛出大于 threshold 的数。

    例：ex17_above_threshold([1, 5, 9], 4) -> [5, 9]
    提示：[x for x in nums if ...]
    """
    # TODO
    return [x for x in nums if x > threshold]


def ex18_sort_by_power(devices: list) -> list:
    """【排序】按功率从大到小，返回设备名列表。

    devices 长这样：
        [{"name": "电机A", "power": 1.5}, {"name": "泵B", "power": 7.5}]

    例：ex18_sort_by_power(devices) -> ["泵B", "电机A"]
    提示：sorted(devices, key=lambda d: d["power"], reverse=True)
    """
    # TODO
    devices = sorted(devices, key=lambda d: d["power"], reverse=True)
    return [d["name"] for d in devices]


def ex19_safe_int(text: str):
    """【异常处理】把字符串转成整数，转不了就返回 None（不要让它报错崩掉）。

    例：ex19_safe_int("12") -> 12
        ex19_safe_int("abc") -> None
    提示：try: ... except ValueError: ...
    """
    # TODO
    try: 
        return int(text) 
    except ValueError: 
        return None


def ex20_report(readings: list, limit: float) -> dict:
    """【综合】传感器读数报告。

    返回字典，三个键：平均值、最大值、超限个数（大于 limit 的个数）。
    空列表时：平均值 0.0、最大值 0、超限个数 0。

    例：ex20_report([1, 2, 3, 10], 5)
        -> {"平均值": 4.0, "最大值": 10, "超限个数": 1}
    """
    # TODO: 可以复用你前面写的 ex11_average 和 ex04_minmax
    if not readings:
        return{"平均值": 0.0, "最大值": 0, "超限个数": 0}
    mixmin = max(readings)
    average = ex11_average(readings)
    count = len(ex17_above_threshold(readings,limit))
    return {"平均值":average,"最大值":mixmin,"超限个数":count}


# ============================================================ 自动检查（不要改下面）


def _run_checks() -> None:
    cases = [
        (1, "电功率", lambda: ex01_power(220, 5.5), 1210.0),
        (2, "拆型号", lambda: ex02_split_model("S7-1200"), ("S7", "1200")),
        (3, "格式化报告", lambda: ex03_format(220, 5.5),
         "电压 220.0 V，电流 5.5 A，功率 1210.0 W"),
        (4, "最小最大值", lambda: ex04_minmax([3, 1, 4, 1, 5]), (1, 5)),
        (5, "切片", lambda: ex05_slice([1, 2, 3, 4, 5, 6]), ([1, 2, 3], [4, 5, 6])),
        (6, "毫安转安培", lambda: ex06_ma_to_a([500, 1000, 20]), [0.5, 1.0, 0.02]),
        (7, "查表", lambda: ex07_get_power({"M1": 1.5, "M2": 2.5}, "M1"), 1.5),
        (7, "查表_不存在", lambda: ex07_get_power({"M1": 1.5}, "M9"), "未知"),
        (8, "功率总和", lambda: ex08_total_power({"M1": 1.5, "M2": 2.5}), 4.0),
        (8, "功率总和_空表", lambda: ex08_total_power({}), 0),
        (9, "交集", lambda: ex09_common([1, 2, 3, 2], [2, 3, 4]), [2, 3]),
        (10, "正常", lambda: ex10_alarm(59), "正常"),
        (10, "预警", lambda: ex10_alarm(75), "预警"),
        (10, "报警", lambda: ex10_alarm(95), "报警"),
        (11, "平均值", lambda: ex11_average([1, 2, 3]), 2.0),
        (11, "平均值_空", lambda: ex11_average([]), 0.0),
        (12, "循环计数", lambda: ex12_count_steps(0, 10, 3), 4),
        (13, "电阻", lambda: ex13_resistance(100, 2.5), 0.7),
        (14, "三元统计", lambda: ex14_stats([2, 4, 6]), (6, 2, 4.0)),
        (15, "故障码", lambda: ex15_parse_fault("E102"), 102),
        (15, "故障码_非E", lambda: ex15_parse_fault("A1"), None),
        (16, "按状态筛选",
         lambda: ex16_devices_by_status(
             [{"name": "电机A", "status": "运行"}, {"name": "泵B", "status": "停机"}], "运行"),
         ["电机A"]),
        (17, "阈值筛选", lambda: ex17_above_threshold([1, 5, 9], 4), [5, 9]),
        (18, "按功率排序",
         lambda: ex18_sort_by_power(
             [{"name": "电机A", "power": 1.5}, {"name": "泵B", "power": 7.5}]),
         ["泵B", "电机A"]),
        (19, "安全转整数", lambda: ex19_safe_int("12"), 12),
        (19, "安全转整数_失败", lambda: ex19_safe_int("abc"), None),
        (20, "综合报告", lambda: ex20_report([1, 2, 3, 10], 5),
         {"平均值": 4.0, "最大值": 10, "超限个数": 1}),
        (20, "综合报告_空", lambda: ex20_report([], 5),
         {"平均值": 0.0, "最大值": 0, "超限个数": 0}),
    ]

    failed_numbers = set()
    total_ok = 0
    for number, label, call, expected in cases:
        try:
            actual = call()
        except Exception as exc:
            print(f"[{number:02d}] X  {label}：报错了 -> {type(exc).__name__}: {exc}")
            failed_numbers.add(number)
            continue
        if actual == expected:
            total_ok += 1
            print(f"[{number:02d}] OK {label}")
        else:
            print(f"[{number:02d}] X  {label}：期望 {expected!r}，你返回 {actual!r}")
            failed_numbers.add(number)

    done = 20 - len(failed_numbers)
    print()
    print("=" * 56)
    print(f"通过检查 {total_ok} / {len(cases)} 条   完成题目 {done} / 20")
    if failed_numbers:
        print("还没过的题号：" + "、".join(f"{n:02d}" for n in sorted(failed_numbers)))
    else:
        print("全部通过。可以提交了：")
        print('    git add .')
        print('    git commit -m "Day 2: Python 语法 20 题"')
    print("=" * 56)


if __name__ == "__main__":
    _run_checks()
