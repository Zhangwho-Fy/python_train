# ex1 quicksort 考点详解

## 题目回顾

写两个版本的快排：

1. `quicksort_functional(arr)`：**函数式**，用列表推导式分组，返回新列表，不改入参；
2. `quicksort_inplace(arr)`：**原地**，用 `_partition` 分区 + 交换，返回 `None`。

用随机数组、空数组、单元素数组做断言验证。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 递归 | 函数调用自己，先写终止条件 | 左右两段分别排序 |
| 列表推导式 | 一次过滤出小于/等于/大于基准 | `[x for x in arr if x < pivot]` |
| 列表拼接 `+` | 把三段拼成一个新列表 | `less + equal + greater` |
| 交换 `a, b = b, a` | 对标 `std::swap` | 原地分区 |
| 默认参数 `hi=None` | 无法在定义时用 `len(arr)-1`，用 None 哨兵 | `lo=0, hi=None` |
| 原地 vs 返回新列表 | 原地函数返回 `None` 是 Python 惯例 | `list.sort()` 同款约定 |
| `random` 造随机数据 | 用断言而不是肉眼检查 | 随机数组 × 5 轮 |

## 1. 函数式快排：三路分组

```python
def quicksort_functional(arr: List[int]) -> List[int]:
    if len(arr) <= 1:                 # 终止条件：空数组/单元素直接返回
        return arr
    pivot = arr[len(arr) // 2]        # 取中间元素当基准
    less = [x for x in arr if x < pivot]
    equal = [x for x in arr if x == pivot]
    greater = [x for x in arr if x > pivot]
    return quicksort_functional(less) + equal + quicksort_functional(greater)
```

为什么分成三组而不是两组：避免大量重复元素时（如全相等的数组）递归退化。`less + equal + greater` 是列表拼接，返回新列表。

- 终止条件 `len(arr) <= 1` 同时覆盖空数组和单元素——漏掉空数组会无限递归。
- 基准取中间元素是为了避免“已排序数组 + 取首元素”导致最坏情况；面试时顺手提一句能加分。

## 2. 原地快排：Lomuto 分区

```python
def _partition(arr: List[int], lo: int, hi: int) -> int:
    pivot = arr[hi]                   # 用右端点当基准
    i = lo                            # i 左侧都是 <= pivot 的
    for j in range(lo, hi):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]   # 交换
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]         # 基准归位
    return i                          # 基准最终下标
```

`arr[i], arr[j] = arr[j], arr[i]` 一行交换，等价于 C++ 的 `std::swap(arr[i], arr[j])`。

```python
def quicksort_inplace(arr: List[int], lo: int = 0, hi: Optional[int] = None) -> None:
    if hi is None:                    # 第一次调用时把 hi 设成最后下标
        hi = len(arr) - 1
    if lo >= hi:
        return
    p = _partition(arr, lo, hi)
    quicksort_inplace(arr, lo, p - 1)   # 左段
    quicksort_inplace(arr, p + 1, hi)   # 右段
```

`hi: Optional[int] = None` 是关键技巧：默认参数在 `def` 执行时求值，`len(arr) - 1` 那时还不知道 arr 是什么，所以用 `None` 当“没传”的哨兵，函数体内再算。这是 Python 里处理“默认值依赖参数”的标准套路。

## 3. 原地 vs 返回新列表

```python
data = [random.randint(-100, 100) for _ in range(20)]
assert quicksort_functional(data) == sorted(data)

quicksort_inplace(data)        # 原地改 data，函数本身返回 None
assert data == sorted(data)
```

- `quicksort_inplace` 修改调用方传入的列表，按 Python 惯例返回 `None`（和 `list.sort()` 一致）。
- `quicksort_functional` 不碰入参，返回新列表（和 `sorted()` 一致）。
- 这是 Python 库设计的两大流派，用哪个取决于“能不能接受入参被改”。

## 4. 易错点清单

1. **漏了空数组终止条件**：`quicksort([])` 死循环/爆栈。
2. **`range(lo, hi)` 不含 hi**：分区循环应遍历到 `hi - 1`。
3. **分区后忘把基准换回 `i` 位置**：返回的下标就不是基准的最终位置。
4. **默认参数写成 `hi=len(arr)-1`**：定义时 arr 还不存在，语法/逻辑都错。
5. **原地版忘了 `if lo >= hi: return`**：无限递归。
6. **相等元素只进小于组**：会死循环；要么三路分组，要么 `<=` 进左侧。

## 5. 变式练习

- 把三路分组的函数式版改成两路，对比重复元素时的表现。
- 实现 Hoare 分区（两个指针从两端相向），对比 Lomuto 的交换次数。
- 给原地版加 `random` 基准（先随机挑一个和右端交换），体会对“已排序输入”的鲁棒性。
