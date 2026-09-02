# ex4 timer_context 考点详解

## 题目回顾

两种“with 计时”实现：

1. `Timer` 类：实现 `__enter__ / __exit__`；
2. `@contextmanager` 的 `timed()`：yield 前记录开始，yield 后打印耗时。

`with timer():` 跑点活，结束后自动打印。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 上下文管理器协议 | `__enter__` 进入、`__exit__` 退出 | 自动开始/结束计时 |
| `with ... as t` | 把 `__enter__` 返回值赋给 t | `with Timer() as t:` |
| `@contextmanager` | 用生成器写上下文管理器 | yield 上下分前后逻辑 |
| `try / finally` | 无论如何都执行收尾 | 出异常也打印耗时 |
| `__exit__` 返回值 | False 表示不吞异常 | 异常照常抛 |

## 1. 类实现：`__enter__` / `__exit__`

```python
import time

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self                 # with Timer() as t 时 t 就是这个对象

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_ms = (time.perf_counter() - self.start) * 1000
        print(f"with 块耗时 {elapsed_ms:.2f} ms")
        return False                # False = 异常不要吞，继续往外抛
```

用法：

```python
with Timer():
    time.sleep(0.01)     # 块结束时自动打印耗时
```

- 进入 `with` 时调 `__enter__`，离开时（无论正常还是异常）调 `__exit__`。
- `exc_type/exc_val/exc_tb`：如果块内抛了异常，这三个参数描述异常；没有异常时都是 None。
- `return False`（或不写 return，默认 None）表示“异常继续传播”；`return True` 会把异常吞掉。C++ 对照：`__exit__` 有点像 RAII 析构 + 决定是否抑制异常的哨兵。

## 2. `@contextmanager`：生成器写法

```python
from contextlib import contextmanager

@contextmanager
def timed():
    start = time.perf_counter()
    try:
        yield                    # 这个位置就是 with 块体
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"with 块耗时 {elapsed_ms:.2f} ms")
```

用法与类版本完全一致：

```python
with timed():
    time.sleep(0.01)
```

规则：`yield` **上面**的代码是进入时执行，`yield` **下面**的代码是退出时执行。必须用 `try/finally` 包住 yield，否则块内抛异常时“收尾代码”不会跑。

两种写法选哪个：类适合要暴露属性/方法（比如 `t.start`）、或要处理异常细节；`@contextmanager` 适合“就一段前置 + 一段后置”的简单场景。

## 3. 易错点清单

1. **类忘写 `__enter__` 或 `__exit__`**：`TypeError: 'Timer' object does not support the context manager protocol`。
2. **`__exit__` 返回 True**：块内的异常被吞掉，外面 try/except 永远接不到——除非你确实想吞。
3. **`@contextmanager` 版本忘 `try/finally`**：正常路径能打印，一抛异常后置代码就跳过。
4. **`with Timer() as t:` 里没用 t**：没关系，但要知道 t 是 `__enter__` 的返回值；`__enter__` 忘 `return self` 时 t 是 None。
5. **计时起点记在 `__init__` 而不是 `__enter__`**：对象可能早创建晚使用，计时会偏。

## 4. 变式练习

- 给 `Timer` 加 `elapsed_ms` 属性，块结束后还能取耗时做断言。
- 让 `@contextmanager` 版支持 `as t` 返回计时对象。
- 写一个 `@timer` 装饰器和 `Timer` 上下文管理器共用的计时函数，比较两种包装风格。
