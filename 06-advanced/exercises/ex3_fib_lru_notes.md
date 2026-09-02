# ex3 fib_lru 考点详解

## 题目回顾

给 `fib` 加 `@lru_cache(maxsize=None)` 跑 `fib(100)`；再手写一个 `memoize` 装饰器（dict 缓存）验证结果一致。期望 `fib(100) == 354224848179261915075`。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `functools.lru_cache` | 内置记忆化装饰器 | `@lru_cache(maxsize=None)` |
| `maxsize=None` | 缓存不设上限 | fib(100) 全量缓存 |
| 手写 memoize | 用 02 的闭包知识做成装饰器 | dict 缓存 + wrapper |
| 装饰后递归 | 递归调用走的是“被装饰的版本” | 缓存才会命中 |
| 大整数 | Python int 无上限 | fib(100) 是 30 位数 |

## 1. `lru_cache` 一行记忆化

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib_lru(n: int) -> int:
    if n < 2:
        return n
    return fib_lru(n - 1) + fib_lru(n - 2)
```

- `lru_cache`（Least Recently Used）自动缓存“参数 → 返回值”：同一参数只算一次。
- `maxsize=None` 表示缓存不淘汰；有上限时（如 128），最久没用过的条目会被清掉，适合内存有限的热点函数。
- 这正是 02 阶段 ex2 手写 dict 缓存的“标准库版”——知识闭环。
- 验证：`fib_lru(100)` 秒出 `354224848179261915075`；朴素递归 fib(100) 在宇宙热寂前都算不完。

## 2. 手写 memoize 装饰器

```python
def memoize(fn):
    cache = {}

    def wrapper(n: int) -> int:
        if n in cache:
            return cache[n]
        result = fn(n)
        cache[n] = result
        return result

    return wrapper
```

```python
@memoize
def fib_memo(n: int) -> int:
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)   # 调的是 wrapper！
```

关键点：`fib_memo` 这个名字经过 `@memoize` 后指向的是 **wrapper**。递归里的 `fib_memo(n-1)` 调用的是 wrapper，wrapper 先查缓存——缓存才能命中。如果内部写 `fn(n-1)` 调原始函数，缓存就废了。

手写版可以补上 06 ex1 教过的 `@wraps(fn)`，并改成收 `*args, **kwargs` 让它通用。

## 3. lru_cache 的限制

- 参数必须**可哈希**（list/dict 不行——和 dict 键的要求一样）。
- 默认只按参数缓存，不区分调用上下文；副作用函数**不能**乱加缓存。
- 想清空缓存用 `fib_lru.cache_clear()`；想看命中情况用 `fib_lru.cache_info()`。

## 4. 易错点清单

1. **忘写 `@lru_cache(...)` 的括号**：`@lru_cache` 也能用但语义不同（默认 maxsize=128，可接受）；规范写法带参数括号。
2. **手写 memoize 忘 return wrapper**：装饰器返回 None，`fib_memo` 变 None。
3. **内部递归调用原始函数而不是 wrapper**：缓存永不命中。
4. **`maxsize=None` 用于无限递归场景**：fib 是自底向上的递归树，缓存没问题；无边界参数组合可能涨爆内存，要权衡。
5. **断言浮点/溢出习惯**：Python int 任意大，`fib(100)` 精确等于那个 30 位数，不用考虑 C++ 的溢出。

## 5. 变式练习

- 打印 `fib_lru.cache_info()` 看命中和未命中次数。
- 给手写 `memoize` 加 `functools.wraps`，并支持任意参数（`*args` 用 `args` 元组当键）。
- 对比 `lru_cache(maxsize=10)` 与 `maxsize=None` 对 `fib(100)` 结果的影响（小缓存会因深度递归不断逐出，反而慢）。
