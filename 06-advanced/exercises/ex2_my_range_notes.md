# ex2 my_range 考点详解

## 题目回顾

用生成器实现 `my_range(start, stop=None, step=1)`，行为对齐内置 `range`：支持只传 stop、负数步长递减、`step=0` 抛 `ValueError`，最后写断言。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 生成器 `yield` | 逐个产出，暂停/恢复 | 每次 yield 一个数 |
| 默认参数哨兵 | `stop=None` 区分“只传一个参数” | 一参时 `start, stop = 0, start` |
| 参数重绑定 | 局部变量可以重新赋值 | 把 start 当游标 |
| 步长方向 | 正步长升序、负步长降序 | 两个 while 分支 |
| `raise ValueError` | 非法参数主动报错 | `step == 0` |
| 惰性求值 | 不调 `list()` 不产出 | `list(my_range(5))` |

## 1. 函数签名与哨兵参数

```python
def my_range(start, stop=None, step=1):
    if stop is None:                # 只传了一个参数：my_range(5)
        start, stop = 0, start      # 变成 my_range(0, 5)
```

- 内置 `range(5)` 表示 0..4，`range(1, 5)` 表示 1..4。区别就在“参数是 start 还是 stop”。
- 用 `stop=None` 当哨兵：没人会真把 stop 传成 None，所以能安全区分两种调用。
- `start, stop = 0, start` 是元组解包交换——右边先求值再赋值，不会互相污染。

## 2. 方向分支与生成器

```python
def my_range(start, stop=None, step=1):
    if stop is None:
        start, stop = 0, start
    if step == 0:
        raise ValueError("step 不能为 0")   # range(0, 5, 0) 也是报错

    if step > 0:
        while start < stop:
            yield start
            start += step
    else:
        while start > stop:
            yield start
            start += step
```

- `range(10, 0, -3)` 期望 `[10, 7, 4, 1]`：步长为负时终止条件反过来，用 `>` 而不是 `<`。
- `range(0, 5, -1)` 期望 `[]`：step 负但 start < stop，条件一开始就不成立，一个都不产出——天然正确，不用特判。
- 函数体里有 `yield` 就是生成器函数：`my_range(5)` **不会执行**，返回生成器对象；`list(my_range(5))` 才把它耗尽成列表。
- 生成器只能走一遍：`g = my_range(3); list(g); list(g)` 第二次是 `[]`。

## 3. 断言验证

```python
assert list(my_range(5)) == [0, 1, 2, 3, 4]
assert list(my_range(1, 10, 2)) == [1, 3, 5, 7, 9]
assert list(my_range(10, 0, -3)) == [10, 7, 4, 1]
assert list(my_range(0, 5, -1)) == []
try:
    list(my_range(0, 5, 0))
except ValueError:
    print("step=0 正确报错")
```

- 内置 `range` 返回的是 range 对象（可迭代、可测长度）；本题用生成器实现，只要求“迭代结果一致”，所以都要包 `list()` 比较。
- 半开区间：`my_range(5)` 不含 5；`my_range(1, 10, 2)` 不含 10。

## 4. 易错点清单

1. **`if stop is None` 写成 `if not stop`**：`my_range(0)` 会把 0 当“没传 stop”，逻辑错乱。判断“传没传”必须用 `is None`。
2. **只写升序分支**：负数步长直接死循环或永不产出。
3. **`step == 0` 不检查**：`start += 0` 永远不前进，死循环。
4. **生成器里 `return` 返回值**：生成器的 `return` 不能带值，带值报 `SyntaxError`。
5. **忘 `list()` 就断言**：拿生成器对象和列表比较永远 False。

## 5. 变式练习

- 让 `my_range` 返回“可重放”的迭代对象（实现 `__iter__/__next__` 的类）。
- 给生成器加 `__len__` 语义？体会内置 range 为什么是对象而不是生成器。
- 用 `itertools.count`/`islice` 组合实现无限步进再截断，对比手写 while。
