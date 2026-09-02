# ex4 topk 考点详解

## 题目回顾

`top_k(nums, k)` 用三种方法找最大的 k 个数：

1. `sorted` 排序后取前 k；
2. `heapq.nlargest(k, nums)`；
3. 手动维护大小为 k 的**最小堆**，比堆顶大就替换。

三种结果断言一致。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `sorted(nums, reverse=True)[:k]` | 全排序截断 | 最直白，O(n log n) |
| `heapq.nlargest` | 内置 Top-K | O(n log k) |
| `heapq` 是最小堆 | 和 C++ 默认最大堆相反 | 堆顶是“当前第 k 大” |
| `heappush` / `heappop` / `heapreplace` | 堆三件套 | 维护 size=k |
| `heapreplace(heap, x)` | 弹出堆顶并压入新元素 | 比堆顶大就替换 |
| 复杂度选型 | 数据大时别全排序 | k << n 时堆最优 |

## 1. 方法一：全排序

```python
def top_k_sorted(nums: List[int], k: int) -> List[int]:
    return sorted(nums, reverse=True)[:k]
```

- `sorted(..., reverse=True)` 降序，切片 `[:k]` 取前 k 个。写起来最爽，但全部排完是 O(n log n)。

## 2. 方法二：`heapq.nlargest`

```python
def top_k_nlargest(nums: List[int], k: int) -> List[int]:
    return heapq.nlargest(k, nums)
```

- `heapq.nlargest(k, iterable)` 直接返回最大的 k 个，内部用大小为 k 的堆实现，O(n log k)。
- 另有对称的 `heapq.nsmallest(k, iterable)`。

## 3. 方法三：手写大小 k 的最小堆

```python
def top_k_manual_heap(nums: List[int], k: int) -> List[int]:
    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)          # 堆没满就塞
        elif x > heap[0]:                    # 比堆顶（当前最小候选）大
            heapq.heapreplace(heap, x)       # 弹出堆顶，压入 x
    return heap
```

思路：

- 维护一个**只有 k 个元素的最小堆**，堆顶就是“当前已见过的 Top-K 里最小那个”。
- 新元素 ≤ 堆顶：它进不了 Top-K，忽略。
- 新元素 > 堆顶：把堆顶踢掉换成它。一轮下来堆里就是全局 Top-K。
- `heapreplace(heap, x)` = `heappop()` + `heappush()` 的合并版，效率略高。

**和 C++ 的关键差异**：C++ `std::priority_queue` 默认是**最大堆**；Python `heapq` 只有最小堆。所以：

- Python 找最大 K 个：维护 k 大小的最小堆，比堆顶大就替换（如上）；
- 找最小 K 个：维护 k 大小的最大堆，实现方式是把数存成负数，或用 `nlargest` 的对称 `nsmallest`。

## 4. 复杂度选型

| 方法 | 复杂度 | 适用场景 |
| --- | --- | --- |
| sorted | O(n log n) | 数据小、要全部有序 |
| nlargest | O(n log k) | 只要 Top-K，n 大 |
| 手写堆 | O(n log k) | 流式数据：来一个处理一个，堆常驻 |

手写堆的独特价值是**流式**：数据不用全放内存，来一个比一个。

## 5. 易错点清单

1. **忘了 heap 是最小堆**：`heap[0]` 是最小值不是最大值；堆顶判断“是不是 Top-K 门槛”要用“比堆顶大就替换”。
2. **k 大于数组长度**：`heap` 永远装不满，返回全部即可（循环自然处理）。
3. **`heapq` 要先 `import heapq`**：函数是 `heapq.xxx`，不是裸 `push`。
4. **`sorted` 结果顺序与堆结果不同**：题目断言用 `sorted(...)` 后再比，绕开顺序差异。
5. **`k <= 0`**：`[:0]` 返回空列表没问题；手动堆要防 `k=0` 时 `heap[0]` 越界（实际不会进 elif，因为 `len(heap) < 0` 为假——但 `x > heap[0]` 会崩，注意边界）。

## 6. 变式练习

- 找最小的 k 个：用负数模拟最大堆，或直接 `nsmallest`。
- 数据流场景：写一个 `TopK` 类，`add(x)` 后随时可查当前 Top-K。
- 在 09 的 RAG 里，`retriever` 返回 top-k 相关片段就是“检索打分后取最大 k 个”的应用。
