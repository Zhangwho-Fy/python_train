# ex1 timer_decorator 考点详解

## 题目回顾

写 `@timer` 装饰器：包住函数，调用时打印函数名和耗时（毫秒），用 `time.perf_counter` 测 `sum(range(10**6))`。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 装饰器语法 `@timer` | `@timer` ≡ `f = timer(f)` | 包一层不改原函数 |
| 闭包 wrapper | 内层函数收 `*args, **kwargs` 再透传 | 不挑参数地包装任意函数 |
| 返回值透传 | 包装不能吞掉原函数的返回值 | `return result` |
| `time.perf_counter` | 高精度计时器 | 测毫秒耗时 |
| `functools.wraps` | 保留原函数名字/docstring | 别让 `fn.__name__` 变成 wrapper |

## 1. 装饰器本质：函数的函数

```python
def timer(fn):
    def wrapper(*args, **kwargs):
        ...
    return wrapper
```

`@timer` 写在函数定义前，等价于：

```python
def sum_range(n):
    ...

sum_range = timer(sum_range)   # 用 wrapper 换掉原名
```

- 装饰器接收**函数**，返回**新函数**。C++ 没有直接对应物，最接近的是模板包装/AOP：在调用前后插入逻辑。
- 原函数没被改，只是“名字被换成了包装后的函数”。

## 2. 完整实现

```python
import time
from functools import wraps

def timer(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()             # 计时起点
        result = fn(*args, **kwargs)            # 真正调用原函数
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"{fn.__name__} 耗时 {elapsed_ms:.2f} ms")
        return result                           # 返回值必须透传
    return wrapper

@timer
def sum_range(n: int) -> int:
    return sum(range(n))

print(sum_range(10 ** 6))   # 打印耗时 + 返回结果 499999500000
```

三个容易漏的点：

1. **`*args, **kwargs`**：原函数可能有任意参数（本题是 `n`），wrapper 全部接住再原样传给 `fn`。这是“不挑函数签名”包装的关键。
2. **`return result`**：忘了 return，原函数返回值就被吞成 `None`。
3. **`@wraps(fn)`**：不写的话 `sum_range.__name__` 会变成 `"wrapper"`，docstring 也没了。`@wraps` 把原函数的元信息拷到 wrapper 上，调试/文档都正常。

## 3. 计时器选择

- `time.perf_counter()` 是**最高精度**的单调计时器，适合测耗时。
- 别用 `time.time()` 测短任务：它可能被系统校时影响，精度也不够。
- 毫秒 = 秒 × 1000；`:.2f` 保留两位小数。

## 4. 易错点清单

1. **`@timer` 忘写括号和函数**：`@timer` 用法正确，但有人写 `@timer()`——那是“装饰器工厂”的用法，会先把 timer() 的返回值当装饰器，报错或行为诡异。
2. **wrapper 忘 `*args, **kwargs`**：带参函数调用时报“参数数量不匹配”。
3. **计时完忘 return**：`sum_range(...)` 变 None。
4. **在装饰器里直接调用 `fn` 而不是包起来**：那装饰器根本没“包”。
5. **忘 `@wraps`**：元信息丢失，很多框架靠 `__name__`/签名工作（LangChain 的 `@tool` 就依赖它）。

## 5. 变式练习

- 给 `@timer` 加参数：`@timer(unit="s")`（需要两层函数：装饰器工厂返回装饰器）。
- 统计“平均耗时”：连续调用 10 次取均值。
- 让 timer 可选打印：`@timer(verbose=False)` 只记不打印。
