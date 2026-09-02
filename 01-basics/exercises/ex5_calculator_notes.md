# ex5 calculator 考点详解

## 题目回顾

命令行计算器：输入 `3 + 5` 这种“数字 空格 运算符 空格 数字”的表达式，循环计算；输入 `quit` 退出。支持 `+ - * /`，除零和未知运算符要报错而不是崩溃。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `str.split()` | 按空白拆成字符串列表 | `"3 + 5".split()` → `['3', '+', '5']` |
| `float()` | 字符串转浮点数 | `float(ops[0])` |
| `try / except ValueError` | 捕获指定异常 | 兜住转换失败和计算报错 |
| `raise ValueError(...)` | 主动抛异常 | 除零 / 未知运算符 |
| `while True` + `break` | 直到 `quit` 退出 | 主循环 |
| `if / elif / else` | 按运算符分发 | `+ - * /` |
| 函数 + 参数 | 计算逻辑独立成函数 | `calculate(a, op, b)` |

## 1. 按空格拆表达式

```python
line = input("输入运算：")      # "3 + 5"
ops = line.split()             # ['3', '+', '5']
```

- `split()` 不传参数时按**任意连续空白**拆：`"3  +   5".split()` 同样是 `['3', '+', '5']`，多个空格无所谓。
- 想按指定字符拆就传参：`"a,b,c".split(",")`。
- 用户输入 `3+5`（没空格）时只会拆出一个元素 `['3+5']`，`len(ops) != 3` 会被拦下——这也是“必须带空格”的原因。

## 2. 字符串转浮点

```python
a = float(ops[0])    # "3" → 3.0
b = float(ops[2])
```

- `float("3.14")`、`float("3")` 都行；`float("abc")` 抛 `ValueError`。
- 用 `float` 而不是 `int`，这样 `1 / 2` 能算出 `0.5`（Python 的 `/` 永远是浮点除法）。

## 3. 函数 + 异常：`raise` 与 `except`

```python
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
```

- 除零不会像 C++ 浮点那样给出 `inf`，这里主动 `raise ValueError(...)`，等价于 C++ 的 `throw`。
- 调用侧用 `try / except` 接住，等价于 `try / catch`：

```python
try:
    num1 = float(ops[0])        # 字符串转换失败也抛 ValueError
    operator = ops[1]
    num2 = float(ops[2])
    res = calculate(num1, operator, num2)
    print(res)
except ValueError as e:         # 只接 ValueError
    print(f"错误：{e}")
```

关键点：

- `except ValueError as e:` 里 `e` 就是异常对象，`print(e)` 显示 `raise` 时给的信息。
- **异常类型要对上**：`float()` 和你的 `raise ValueError` 都是 `ValueError`，一个 `except` 全接住。类型不匹配就接不住，程序照样崩。
- 别写裸 `except:` 吞一切——Debug 时会把问题全藏起来。

## 4. 主循环

```python
while True:
    line = input("输入运算：")
    if line == "quit":
        break              # 退出循环，程序结束
    ops = line.split()
    if len(ops) != 3:
        print("非法输入")
        continue           # 跳过本次，回到 while 开头
    ...
```

- `break` 结束循环，`continue` 跳过本次回到条件判断——和 C++ 一样。
- 本题没有单独写 `main()`；简单脚本可以直接写在 `if __name__ == "__main__":` 下面。

## 5. 易错点清单

1. **忘了 `float()` 转换**：字符串 `"3"` 和数字相加会 `TypeError`。
2. **除法不检查 `b == 0`**：整数场景会直接崩（`float` 会得到 `inf`，行为不对）。
3. **`except` 写在 `try` 外面**：异常会继续向上抛，程序崩。
4. **用户输入 `quit` 前有空格**：`line.strip() == "quit"` 更稳。
5. **`line.split()` 结果少于 3 个元素就下标访问**：先 `len(ops) != 3` 拦截。

## 6. 变式练习

- 支持 `//`（整除）、`%`（取余）、`**`（幂）。
- 输入不用空格也能算：用 `re` 正则把数字和运算符拆开。
- 算完显示算式：`print(f"{num1} {operator} {num2} = {res}")`。
- 加 `history` 列表，记录每次运算，输入 `history` 时打印。
