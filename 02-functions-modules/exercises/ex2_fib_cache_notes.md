# ex2 fib_cache 考点详解

## 题目回顾

用“闭包 + dict 缓存”实现记忆化 `fib(n)`，统计总调用次数和缓存命中次数；跑 `fib(30)`，和朴素递归对比调用量，体会指数级 vs 线性。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 闭包 | 内层函数能读写外层函数的变量 | `fib` 里访问 `cache` 和 `stats` |
| dict 当缓存 | `n in cache` 判断、`cache[n] = v` 写入 | 记忆化 |
| 递归 | 函数调用自己 | `fib(n - 1) + fib(n - 2)` |
| 可变对象与闭包 | 闭包里改 dict 不用 `nonlocal` | `stats["calls"] += 1` |
| 返回多个值 | `return fib, stats` 直接返回两个东西 | 函数 + 计数器一起拿 |
| 复杂度对比 | 朴素指数级 vs 记忆化线性 | 2692537 次 vs 59 次 |

## 1. 记忆化：用 dict 缓存算过的结果

```python
def make_fib_cached():
    cache = {0: 0, 1: 1}          # 已知的基础情况
    stats = {"calls": 0, "hits": 0}

    def fib(n: int) -> int:
        stats["calls"] += 1       # 每次调用先计数
        if n in cache:            # 命中缓存
            stats["hits"] += 1
            return cache[n]
        value = fib(n - 1) + fib(n - 2)
        cache[n] = value          # 算完存起来
        return value

    return fib, stats
```

核心思想：`fib(28)` 会被 `fib(30)` 和 `fib(29)` 都要用，第一次算完存进 `cache`，第二次直接取，不再递归展开。

## 2. 闭包：内层函数“记住”外层变量

- `fib` 定义在 `make_fib_cached` 里面，它能访问外层函数的 `cache`、`stats`——这叫闭包。
- C++ 对照：`auto fib = [&cache, &stats](int n) { ... };` 按引用捕获外层变量。
- **关键区别**：这里改的是 `stats["calls"]` 这个 **dict 里的元素**，dict 对象本身没被重新赋值，所以不需要 `nonlocal`。如果写的是外层整数 `calls += 1`，Python 会报“引用前未赋值”或静默当成局部变量——需要 `nonlocal calls` 声明。这正是本题用 dict 装统计数字的原因：省掉 `nonlocal` 的复杂度。

## 3. 返回多个值

```python
fib_cached, stats = make_fib_cached()
```

- `return fib, stats` 返回的是一个元组 `(fib, stats)`，调用处解包成两个变量——Python 的天然“多返回值”，对标 C++ 的 `std::pair`/`std::tuple`。
- 函数也是对象，所以能被装进元组返回。

## 4. 复杂度对比

跑 `fib(30)`：

- 朴素递归（每次都重新展开）：**2,692,537 次调用**，指数级爆炸。
- 记忆化版本：**59 次总调用（其中 30 次命中缓存）**，接近线性。

朴素版：

```python
def fib_naive(n: int) -> int:
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)
```

同一个 `fib(30)`，两者相差五万倍。这就是“以空间换时间”的 memoization，后面 06 阶段会用 `@lru_cache` 一行做到同样效果。

## 5. 易错点清单

1. **缓存建在递归函数内部**：每次调用都新建空 dict，等于没缓存。缓存必须建在“外层/全局”，函数只读它。
2. **基础情况没预先入缓存**：`fib(0)`/`fib(1)` 会一路递归到负数。
3. **统计放在 return 之后**：命中判断前忘了 `stats["calls"] += 1`，数字就不对。
4. **想直接改外层整数计数器但不写 `nonlocal`**：要么用 dict/列表装，要么写 `nonlocal`。
5. **`n in cache` 用成 `cache[n]` 判断**：键不存在直接 `KeyError`；要判断用 `in`。

## 6. 变式练习

- 用 `dict.get` 惰性写法：`if n not in cache: cache[n] = fib(n-1) + fib(n-2)`。
- 把 `make_fib_cached` 改成通用 `memoize(fn)` 装饰器（06 ex3 会做）。
- 自底向上动态规划：`for i in range(2, n+1): cache[i] = cache[i-1] + cache[i-2]`，对比两种方向。
