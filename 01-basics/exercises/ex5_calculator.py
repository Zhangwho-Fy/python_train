"""ex5: 简单命令行计算器。"""


def calculate(a: float, op: str, b: float) -> float:
    if op == "+":
            return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            raise ValueError("divide by zero")
        return a / b
    else:
        raise ValueError("unknown operator")


def main() -> None:
    while True:
        line = input("输入运算：")
        if line == "quit":
            break
        ops = line.split()
        if len(ops) != 3:
            print("非法输入")
            continue
        try:
            num1 = float(ops[0])
            operator = ops[1]
            num2 = float(ops[2])
            res = calculate(num1, operator, num2)
            print(res)
        except ValueError as e:
            print(f"错误：{e}")

if __name__ == "__main__":
    main()
