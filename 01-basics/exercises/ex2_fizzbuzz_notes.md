# ex2 fizzbuzz 考点详解

## 题目回顾

输入 n，打印 1 到 n：能被 3 整除打 `Fizz`，能被 5 整除打 `Buzz`，能被 15 整除打 `FizzBuzz`，其余打数字本身。

期望：`n=15` 时第 15 行是 `FizzBuzz`（15 同时是 3 和 5 的倍数）。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `range(1, n + 1)` | 左闭右开的整数序列 | 生成 1..n |
| `for i in range(...)` | 遍历一个序列 | 循环 i 从 1 到 n |
| `%` | 取余判断整除 | `i % 3 == 0` |
| `if / elif / else` | 多分支选择 | 15 → 3 → 5 的顺序判断 |
| `int(input())` | 把字符串转整数 | `n = int(input("n = "))` |
| 整除判断写法 | `i % 15 == 0` 等效 `i % 3 == 0 and i % 5 == 0` | 先判 15 |

## 1. `range` 与 for 循环

```python
for i in range(1, n + 1):   # i = 1, 2, ..., n
    print(i)
```

- `range(start, stop)` 是**左闭右开**：包含 `start`，不包含 `stop`。想打印 1..n 必须写 `range(1, n + 1)`。
- `range(n)` 是 `0..n-1`，**没有 `n`**——这是和 C++ `for (int i = 0; i < n; ++i)` 一致的习惯。
- `range(start, stop, step)` 还能指定步长，步长可为负：`range(10, 0, -2)` 是 `10, 8, ..., 2`。

对比 C++：

| C++ | Python |
| --- | --- |
| `for (int i = 1; i <= n; ++i)` | `for i in range(1, n + 1)` |
| `for (auto& x : xs)` | `for x in xs:` |

## 2. 取余 `%` 与多分支

```python
if i % 15 == 0:
    print("FizzBuzz")     # 15 的倍数
elif i % 3 == 0:
    print("Fizz")         # 3 的倍数
elif i % 5 == 0:
    print("Buzz")         # 5 的倍数
else:
    print(i)
```

- **`elif` 是 Python 的 `else if`**，没有 `else if` 这个写法。
- **判断顺序很重要**：15 的倍数同时满足“3 的倍数”和“5 的倍数”，必须把 `i % 15 == 0` 放在最前面。写反了，15 会先命中 `Fizz` 或 `Buzz`。
- `i % 15 == 0` 与 `i % 3 == 0 and i % 5 == 0` 等价（对整数成立）；用前者最直白。
- Python 用 `and / or / not`，不是 `&& / || / !`。

## 3. 字符串转整数

```python
n = int(input("n = "))
```

- `input()` 返回字符串，`int("15")` 转成整数 15。
- 用户输入的不是数字（比如 `abc`）时，`int()` 抛 `ValueError`，程序崩溃。先不管它，ex5 会讲怎么用 `try/except` 兜住。

## 4. 易错点清单

1. **`range(1, n)` 少了 n**：想含 n 必须 `n + 1`。
2. **`range(n)` 从 0 开始**：0 是任何数的倍数，会打乱结果。
3. **15 的倍数没先判**：被 `Fizz`/`Buzz` 抢走。
4. **Python 没有 `&&`**：条件组合要用 `and`。
5. **`if` 后忘写冒号**：`if i % 3 == 0:` 漏掉 `:` 直接语法错误。

## 5. 变式练习

- 改成“3 的倍数和 5 的倍数分别打印单词，同时是打印拼接结果”（用 `and` 版条件）。
- 把结果收集进列表再 `return`，而不是直接 `print`。
- 换成 7/11 的倍数，体会“公倍数放最前”的通用写法。
