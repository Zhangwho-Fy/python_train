"""ex5 参考答案。"""


def calculate(a: float, op: str, b: float) -> float:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ValueError("除数不能为 0")
        return a / b
    raise ValueError(f"未知运算符: {op}")


def main() -> None:
    while True:
        line = input("表达式 (如 3 + 5, 输入 quit 退出): ")
        if line.strip() == "quit":
            break
        parts = line.split()
        if len(parts) != 3:
            print("格式: 数字 运算符 数字")
            continue
        try:
            result = calculate(float(parts[0]), parts[1], float(parts[2]))
            print(f"= {result}")
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
