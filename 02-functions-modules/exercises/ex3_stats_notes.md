# ex3 stats 考点详解

## 题目回顾

写一个可复用的统计模块 `stats.py`：`mean`（均值）、`median`（中位数）、`std`（样本标准差，除以 n-1），带类型注解和 docstring；`__main__` 里对 1..100 自测并打印，期望 `mean=50.5, median=50.5, std≈28.87`。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 模块化 | 一个 `.py` 文件就是一个模块，可被 import | 函数都写在顶层 |
| docstring | 模块/函数第一个字符串即文档 | `"""计算均值"""` |
| `sorted(xs)` vs `xs.sort()` | 返回新列表 vs 原地排序 | 中位数不污染入参 |
| 列表切片 | 取中间元素 | 偶数个取 `n//2` 和 `n//2 - 1` |
| 列表推导式 | 一行构造列表 | `[float(x) for x in range(1, 101)]` |
| `/` 与 `//` | 真除法 vs 整除 | 均值必须 `/` |
| f-string 格式 | `:.2f` 保留两位小数 | 打印输出 |

## 1. 三个统计量怎么算

```python
def mean(xs: List[float]) -> float:
    """算术平均值。"""
    return sum(xs) / len(xs)
```

- `sum(xs)` 是内置求和，`len(xs)` 是元素个数。**必须用 `/`**：`5 / 2 == 2.5`；`//` 是整除。

```python
def median(xs: List[float]) -> float:
    """中位数：排序后取中间；偶数个取中间两数平均。"""
    ys = sorted(xs)                    # 返回新列表，不动原数据
    n = len(ys)
    mid = n // 2
    if n % 2 == 1:
        return ys[mid]
    return (ys[mid - 1] + ys[mid]) / 2
```

- 下标 `n // 2`：奇数个时正好是中间；偶数个时是“右中位”的下标，要和它左边一个平均。
- `sorted(xs)` 返回**新**列表；如果对原列表 `xs.sort()`，调用方手里的数据就被改了——写库函数时不污染入参是基本功。

```python
def std(xs: List[float]) -> float:
    """样本标准差：sqrt(sum((x-mean)^2) / (n-1))。"""
    m = mean(xs)
    n = len(xs)
    variance = sum((x - m) ** 2 for x in xs) / (n - 1)   # 样本方差，分母 n-1
    return variance ** 0.5
```

- `** 0.5` 即开平方（也可 `import math; math.sqrt(...)`）。
- **分母 n-1 是“样本标准差”**：如果按总体标准差用 n，1..100 的结果会不同。题目要求样本标准差。

## 2. docstring 与模块化

```python
def mean(xs: List[float]) -> float:
    """返回 xs 的算术平均值。"""
    ...
```

- 函数体第一行的字符串字面量就是 docstring，`help(mean)` 能看到它——相当于写注释，但能被工具读取。
- 写好后别的文件可以 `from stats import mean` 复用；`if __name__ == "__main__":` 保证 import 时不跑自测。

## 3. 主入口自测

```python
if __name__ == "__main__":
    data = [float(x) for x in range(1, 101)]   # 1.0 ~ 100.0
    print(f"mean={mean(data):.2f}, median={median(data):.2f}, std={std(data):.2f}")
```

- 列表推导式 `[float(x) for x in range(1, 101)]`：对每个 x 执行 `float(x)` 收集成列表，得到 1.0~100.0 共 100 个数。
- 100 是偶数个，中位数取中间两数 `(50.0 + 51.0) / 2 = 50.5`；均值 `(1+100)/2` 也是 50.5，所以打印结果两数相等是巧合但合理。
- `:.2f` 是 f-string 的数字格式：保留两位小数。

## 4. 易错点清单

1. **中位数忘排序**：原顺序直接取下标不是中位数。
2. **偶数个取了一个中间值**：`[1,2,3,4]` 的中位数是 2.5，不是 2 或 3。
3. **均值用 `//` 整除**：`sum // len` 直接截断小数。
4. **标准差分母写成 n**：那是总体标准差，和题目要求不符。
5. **`std` 里 `sum(...)` 忘记除以 n-1 就开方**。
6. **空列表**：`mean([])` 会 `ZeroDivisionError`。可在 docstring 里注明约定，或用 `if not xs: raise ValueError`。

## 5. 变式练习

- 用 `statistics.mean/median/stdev` 标准库函数核对你的实现。
- 增加 `variance(xs, sample=True)` 参数，一个函数同时支持两种标准差。
- 返回 `(mean, median, std)` 元组，或写一个 `describe(xs) -> dict` 汇总。
