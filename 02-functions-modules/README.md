# 02 函数与模块

## 本阶段目标

写出可复用、带类型注解的函数；理解 lambda、`*args/**kwargs`；学会拆模块。

## C++ 对照

| Python | C++ 类似物 |
| --- | --- |
| `def f(a, b=1):` | `int f(int a, int b = 1)` |
| `lambda x: x * 2` | `[&](int x) { return x * 2; }` |
| `*args` | `initializer_list` / 变参模板 |
| `**kwargs` | 参数包按名传递 |
| `from mod import f` | `using` 声明 |
| `import mod` | `#include <mod>` |
| 类型注解 `def f(x: int) -> str:` | 强类型声明 |
| 列表推导 `[x*2 for x in xs if x > 0]` | `std::transform` + `std::copy_if` |

## 核心概念

- **类型注解只是提示**：`def add(a: int, b: int) -> int:` 运行时不做检查，Pylance/mypy 才检查。别把注解当成 `static_cast`。
- **默认参数只在定义时求值一次**：`def f(a, lst=[])` 是经典坑——所有调用共享同一个 list。安全写法是 `lst=None` 再在函数里判断。
- **lambda 只能写一个表达式**：想多行就老老实实 `def`。
- **`if __name__ == "__main__":`**：被 import 时不执行，直接运行时才执行——相当于 C++ 里 `main` 的门卫。
- **包**：目录加 `__init__.py`（Python 3.3+ 可省略，但写上更清晰）。

## 与 LangChain 的关系

LangChain 里到处是 `Callable[[str], str]`、lambda 组件、`functools.partial`；
把高阶函数和推导式练熟，读 LangChain 源码会轻松很多。

## 练习题

### ex1 my_map_filter（高阶函数）

实现自己的 `my_map(fn, xs)` 和 `my_filter(pred, xs)`，返回新 list，**不得调用内置 `map/filter`**；
然后用它们把 `[1..10]` 过滤出偶数并平方。

### ex2 fib_cache（记忆化）

`fib(n)` 用 dict 做缓存，统计“总调用次数”和“命中缓存次数”，跑 `fib(30)` 输出两个数字。
对比朴素递归（不缓存）的调用次数，理解指数级与线性的差别。

### ex3 stats（模块化）

写 `stats.py`：`mean` / `median` / `std`（样本标准差即可），带类型注解和 docstring；
`__main__` 里对 `list(range(1, 101))` 自测并打印。

### ex4 comprehensions（推导式专场）

各用一行推导式完成：

1. `[1..20]` 中能被 3 整除的数的平方列表；
2. 用 `zip` 把 `names` 和 `ages` 合成字典（字典推导式）；
3. 把句子拆词、去重、按长度升序排序。

## 期望输出示例

ex1: `[4, 16, 36, 64, 100]`
ex2: 缓存版调用次数远小于朴素版（例如 30 大概几十次 vs 数百万次）
ex3: `mean=50.5, median=50.5, std≈28.87`
ex4: 自己断言，跑通即可
