# ex3 guess_number 考点详解

## 题目回顾

程序随机生成 1~100 的整数；用户循环猜，大了提示“猜大了”、小了提示“猜小了”，猜中结束并统计次数。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `import random` | 引入标准库模块 | 用它生成随机数 |
| `random.randint(1, 100)` | 生成闭区间随机整数 | 目标数字 |
| `while True` + `break` | “先干再判断”的循环模式 | 直到猜中退出 |
| `int(input())` | 字符串转整数 | 把猜的数字转出来 |
| `if / elif / else` | 三路比较 | 大了 / 小了 / 猜中 |
| 计数器 | 循环里累加变量 | 统计猜的次数 |

## 1. `random` 模块

```python
import random

target = random.randint(1, 100)   # 1 <= target <= 100，两端都包含
```

- `random.randint(a, b)` 返回 `[a, b]` 闭区间内的整数，和 `range` 的“不含右端”不一样。
- `import random` 后要写 `random.randint(...)`；也可以 `from random import randint` 后直接 `randint(...)`，但不推荐在脚本里混用。
- C++ 里是 `<random>`/`rand()` 那一套（还要处理取模偏置）；Python 直接 `randint` 就好，但注意它**只在做游戏/测试时用**，密码学场景要用 `secrets`。

## 2. 猜数字主循环

```python
attempts = 0
while True:
    guess = int(input("猜数字，范围：1~100,输入："))
    attempts += 1
    if guess > target:
        print("猜大了")
    elif guess < target:
        print("猜小了")
    else:
        print(f"猜对了！用了 {attempts} 次")
        break
```

- Python 没有 `do { } while (...)`；需要“至少执行一次、退出条件在循环中间”时，惯用 `while True:` + 条件 `break`。
- 也可以用条件变量写：`done = False; while not done: ... done = True`——但 `break` 更直接。
- `break` 只跳出当前一层循环；嵌套循环要注意跳的是哪层。
- 每猜一次 `attempts += 1`，这就是最简单的计数器。Python 没有 `++` 运算符，`attempts++` 是语法错误。

## 3. 输入与比较

```python
guess = int(input(...))   # 字符串 → int
```

- `input()` 永远是字符串，必须 `int()` 转换后才能和 `target` 比大小。
- 用户输入 `abc` 会抛 `ValueError` 直接崩溃；ex5 会教用 `try/except` 处理。

## 4. 常见错误

1. **把 `randint` 写进循环里**：每猜一次就换目标，永远猜不中。
2. **`range` 习惯带歪**：`random.randint(1, 100)` 含 100，别写成 `random.randrange(1, 101)` 又疑惑为什么含 100。
3. **忘写 `break`**：猜中后还会继续问。
4. **`guess = int(...)` 写在判断里但没存**：要先把值取出来再比较。
5. **`while True` 缩进里的代码没推进状态**：没有 `break` 路径的 `while True` 就是死循环。

## 5. 变式练习

- 猜中后输出“猜了 N 次”，并加入“太离谱了”等趣味提示。
- 限制最多 10 次，超了打印目标并结束（在 `while` 条件里判断次数）。
- 用 `try/except ValueError` 处理非数字输入，提示后不算一次机会。
- 让用户选择范围上下界，再开局。
