# 06 进阶特性：装饰器、生成器、上下文管理器

## 本阶段目标

写出地道 Python：用装饰器横切、用生成器省内存、用 `with` 管理资源。

## C++ 对照

| Python | C++ 类似物 |
| --- | --- |
| `@decorator` | AOP / 模板包装（没有直接对应） |
| `def gen(): yield x` | 惰性求值（类似 C++ ranges） |
| `with ...:` + `__enter__/__exit__` | RAII（析构管理资源） |
| `functools.lru_cache` | 手动 memoization |

## 要点

- **装饰器就是“函数的函数”**：`@timer` 等价于 `f = timer(f)`；返回的新函数里用 `*args, **kwargs` 透传。
- **装饰器别忘 `functools.wraps(fn)`**：否则原函数的名字和 docstring 会丢。
- **生成器是惰性的**：`yield` 后函数暂停，`next(gen)` 拉一个值。适合大文件、无限序列。
- **上下文管理器就是“可 with 的对象”**：`__exit__(exc_type, exc_val, tb)` 里能决定吞掉还是传播异常；懒人版用 `@contextmanager` 包一个生成器。

## 与 LangChain 的关系

- LangChain 内部大量装饰器：`@tool`、`@retry`、`@chain`；
- 流式输出 `stream()` 就是生成器；
- 模型调用、文件加载都适合 with/上下文管理。

## 练习题

### ex1 timer_decorator

写 `@timer` 装饰器：打印函数名和耗时（毫秒）。用 `time.perf_counter`。测 `sum(range(10**6))`。

### ex2 my_range

实现 `my_range(start, stop=None, step=1)` 生成器，行为对齐内置 `range`（含负数步长、step=0 抛 `ValueError`）。写断言。

### ex3 fib_lru

给 `fib` 加 `@lru_cache(maxsize=None)` 跑 `fib(100)`；再手写一个 `memoize` 装饰器（dict 缓存）验证两者结果一致。

### ex4 timer_context

两种实现：`Timer` 类（`__enter__/__exit__`）和 `@contextmanager` 的 `timed()`；
`with timer():` 里跑点活，结束后自动打印耗时。

### ex5 lazy_reader

`lazy_lines(path)` 生成器逐行 yield（不把文件全读进内存），统计行数并打印前 5 行。
（这是 04 阶段 ex4 的标准答案，两个阶段做完你会发现知识闭环了。）

## 期望输出示例

- ex1：`sum_range 耗时 12.34 ms`
- ex2：`list(my_range(1, 10, 2)) == [1, 3, 5, 7, 9]`
- ex3：`fib(100) == 354224848179261915075`
- ex4：`with 块耗时 0.05 ms` 之类的输出
- ex5：行数统计 + 前 5 行内容
