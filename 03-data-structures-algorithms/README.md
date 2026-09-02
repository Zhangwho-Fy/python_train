# 03 数据结构与算法

## 本阶段目标

用 Python 写算法时不再想“C++ 怎么写的”，而是直接想“Python 的惯用法”。

## C++ 对照

| Python | C++ 类似物 | 注意 |
| --- | --- | --- |
| `list` | `std::vector` | `append` 摊还 O(1)，`insert(0, x)` 是 O(n) |
| `collections.deque` | `std::deque` | 两端 O(1) push/pop |
| `heapq` | `std::priority_queue` | **Python 是最小堆**，取最大要取负数或 `nlargest` |
| `dict` / `set` | `unordered_map` / `unordered_set` | 哈希表，`in` 是 O(1) |
| `sorted(xs)` / `xs.sort()` | `std::sort` | `sorted` 返回新列表，`sort` 原地；都有 `key=` 参数，稳定排序 |
| `ListNode` 手写类 | 指针链表 | Python 里“引用即指针”，没有 `->` |

## 要点

- 交换两个变量：`a, b = b, a`（对标 `std::swap`）。
- 多返回值：直接 `return a, b`，调用处 `x, y = f()`。
- 栈：用 `list` 的 `append / pop()` 就是栈。
- 队列：`list.pop(0)` 是 O(n)，要队列就用 `deque.popleft()`。
- 排序的自定义比较：没有 `std::sort(begin, end, cmp)` 的 `cmp`，用 `key=` 提取键，或用 `functools.cmp_to_key`。

## 与 LangChain 的关系

后面 RAG 里的“Top-K 检索”“相关度排序”“去重”全是这些数据结构；
`heapq` 和 `sorted(key=...)` 在写重排序逻辑时天天用。

## 练习题

每题在 `exercises/` 里有配套考点详解（`exN_xxx_notes.md`），卡住先翻详解再翻答案。

### ex1 quicksort

考点详解：`exercises/ex1_quicksort_notes.md`

写两个版本：

1. `quicksort_functional`：用列表推导式，返回新列表（不修改入参）；
2. `quicksort_inplace`：原地分区（`arr[i], arr[j] = arr[j], arr[i]`），返回 `None`。

用随机数组和空数组/单元素数组做断言。

### ex2 merge_sorted_lists

考点详解：`exercises/ex2_merge_sorted_lists_notes.md`

手写 `ListNode` 类（`val` + `next`），实现合并两个有序链表，返回新链头。
再写一个 `to_list / from_list` 辅助函数方便断言。

### ex3 sliding_window_max

考点详解：`exercises/ex3_sliding_window_max_notes.md`

`max_sliding_window(nums, k)`：用 `deque` 维护单调递减下标，O(n) 求每个窗口最大值。
期望：`[1,3,-1,-3,5,3,6,7]` k=3 → `[3,3,5,5,6,7]`。

### ex4 topk

考点详解：`exercises/ex4_topk_notes.md`

`top_k(nums, k)`：分别用 `sorted` 和 `heapq.nlargest` 实现；
再手动维护一个大小为 k 的最小堆（`heapq.heappush/heappop`）做第三种，验证结果一致。

### ex5 valid_parentheses

考点详解：`exercises/ex5_valid_parentheses_notes.md`

`is_valid(s)`：只含 `()[]{}`，判断括号是否匹配。用 list 当栈。
期望：`"()[]{}"` → True，`"([)]"` → False，`"(]"` → False，`"("` → False。

## 期望输出示例

- ex1：任意随机数组排序后等于 `sorted(原数组)`
- ex2：`[1, 2, 2, 3, 4, 5, 6]`
- ex3：`[3, 3, 5, 5, 6, 7]`
- ex4：`top_k([3,1,5,2,4], 2) == [5, 4]`（顺序不限）
- ex5：见上
