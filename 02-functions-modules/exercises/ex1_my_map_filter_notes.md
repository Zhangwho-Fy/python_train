# ex1 my_map_filter 考点详解

## 题目回顾

自己实现 `my_map(fn, xs)` 和 `my_filter(pred, xs)`：都用 for 循环 + `append` 返回新 list，**不许调用内置 `map/filter`**。然后用它们把 `[1..10]` 过滤出偶数再平方，期望 `[4, 16, 36, 64, 100]`。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 高阶函数 | 函数可以当作参数传来传去 | `my_map(fn, xs)` 接收函数 |
| 内置 `map/filter` 的对比 | 它们返回惰性迭代器，本题要求自己写 | 手写 for 循环版 |
| lambda | 一行匿名函数 | `lambda x: x % 2 == 0` |
| `range(1, 11)` | 半开区间序列 | 生成 1..10 |
| `list.append` | 往列表尾部加元素 | 收集结果 |
| 类型注解 `Callable` | 标注“这是个函数” | `fn: Callable[[T], R]` |
| `TypeVar` | 泛型占位符 | 让 `my_map` 的类型注解更通用 |

## 1. 函数是一等公民

C++ 里你见过 `std::function`、函数指针、lambda 捕获；Python 里任何函数都能直接当值传：

```python
def my_map(fn, xs):
    result = []
    for x in xs:
        result.append(fn(x))   # fn 是个“函数”，在这里被调用
    return result

def my_filter(pred, xs):
    result = []
    for x in xs:
        if pred(x):            # pred 返回 True/False
            result.append(x)
    return result
```

`my_map` 的语义：对每个元素调用一次 `fn`，把返回值收集成新列表。`my_filter` 的语义：只留下 `pred(x)` 为真的元素。

## 2. 为什么不直接 `map` / `filter`

内置 `map(fn, xs)` 返回的是**惰性迭代器**，要 `list(...)` 才变成列表：

```python
print(map(lambda x: x * 2, [1, 2, 3]))   # <map object ...>，不是列表
print(list(map(lambda x: x * 2, [1, 2, 3])))  # [2, 4, 6]
```

本题要求手写的是“立刻算完、返回 list”的版本——理解原理后，你会发现内置 map/filter 只是“惰性版 + 极简写法”。

## 3. lambda 匿名函数

```python
evens = my_filter(lambda x: x % 2 == 0, nums)
squares = my_map(lambda x: x * x, evens)
```

- `lambda 参数: 表达式` 只能写**一个表达式**，不能有语句、不能换行写多条逻辑。
- 等价于：

```python
def is_even(x):
    return x % 2 == 0

evens = my_filter(is_even, nums)   # 注意传的是函数名，不是 is_even()
```

lambda 适合一行逻辑；逻辑一复杂就老实 `def`，可读性更好。

## 4. `range` + `append` 收集结果

```python
nums = list(range(1, 11))   # [1, 2, ..., 10]
```

- `range(1, 11)` 是 1..10（不含 11），要转列表就 `list(range(...))`。
- 手写“变换/过滤”的通用骨架就是：建空列表 → for 循环 → 条件判断 → `append` → return。

## 5. 类型注解：`Callable` 与 `TypeVar`

```python
from typing import Callable, List, TypeVar

T = TypeVar("T")                      # 类型变量：调用时自动推断
R = TypeVar("R")

def my_map(fn: Callable[[T], R], xs: List[T]) -> List[R]:
    ...
```

- `Callable[[T], R]` 表示“接收一个 T、返回一个 R 的函数”，对应 C++ 的 `std::function<R(T)>`。
- `TypeVar` 约等于模板参数：`my_map` 对 `List[int]` 用 T=int、R=int；对字符串列表也通用。这些注解运行时不生效，是给 Pylance/mypy 和读代码的人看的。
- 读不懂注解不影响写对代码；但写上后 IDE 能帮你抓类型错误，值得养成习惯。

## 6. 易错点清单

1. **传函数忘了名字，写成调用**：`my_filter(is_even(x), nums)` 会把 `is_even(x)` 的结果当参数传进去。
2. **直接 `return` 循环里拼的字符串而不是列表**：返回类型要是 `List`。
3. **`range(1, 11)` 写成 `range(1, 10)`**：10 就丢了。
4. **lambda 里写多条语句**：语法错误，改用 `def`。
5. **`my_map` 里忘 `return result`**：函数返回 `None`，后面全崩。

## 7. 变式练习

- 用列表推导式重写本题三步：`[x*x for x in nums if x % 2 == 0]`——先理解推导式是“map+filter 的语法糖”（下题专门练）。
- 给 `my_map` 加第三个参数，支持同时 zip 两个列表（对应 C++ 的 transform 双输入版）。
- 把 `my_map` 改成生成器（用 `yield`），体会“惰性版 map”怎么写。
