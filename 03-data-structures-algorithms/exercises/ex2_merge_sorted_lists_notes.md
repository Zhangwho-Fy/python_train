# ex2 merge_sorted_lists 考点详解

## 题目回顾

手写 `ListNode` 链表类（`val` + `next`），合并两个有序链表返回新链头；再写 `from_list` / `to_list` 辅助函数方便断言。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 手写 `class` | Python 里“引用即指针” | `ListNode(val, next_node)` |
| `self.next` | 显式把 next 当属性存 | 指针域 |
| `Optional[ListNode]` | 可能为 None 的类型注解 | 空链表 / 链尾 |
| 哑节点（dummy） | 少写“头节点特判” | `dummy.next` 返回真正头部 |
| 双指针归并 | 谁小接谁 | 合并两个有序链 |
| 构造/遍历辅助函数 | 把 list ↔ ListNode 互转 | 方便断言 |

## 1. Python 里的“指针”

```python
class ListNode:
    def __init__(self, val: int = 0, next_node: Optional["ListNode"] = None):
        self.val = val
        self.next = next_node
```

- Python 对象都是引用；`node.next = other` 就是 C++ 里“让指针指向另一个节点”。**没有 `->`**，一律用 `.`。
- 递归类型注解要写成字符串 `"ListNode"`（或 `from __future__ import annotations`），因为类还没定义完。
- 所有变量都“像指针”：`a = b` 只是让 a 引用 b 指向的对象，改 `a.val` 会反映在 b 上。

## 2. 从 list 建链、遍历成 list

```python
def from_list(xs: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    cur = dummy
    for x in xs:
        cur.next = ListNode(x)   # 新节点挂到链尾
        cur = cur.next           # 前进
    return dummy.next            # 跳过哑节点
```

```python
def to_list(head: Optional[ListNode]) -> List[int]:
    result = []
    cur = head
    while cur is not None:
        result.append(cur.val)
        cur = cur.next
    return result
```

- `dummy` 哑节点让“第一次挂节点”和后面完全一样，不用特判 `head is None`。
- `while cur is not None:` 遍历链表，等价于 C++ 的 `while (cur) { ... cur = cur->next; }`。

## 3. 双指针归并

```python
def merge_two_lists(a, b):
    dummy = ListNode()
    cur = dummy
    while a is not None and b is not None:
        if a.val <= b.val:
            cur.next = a
            a = a.next
        else:
            cur.next = b
            b = b.next
        cur = cur.next
    cur.next = a if a is not None else b   # 接上剩余整段
    return dummy.next
```

要点：

- 直接**复用原节点**（`cur.next = a`），不新建节点——题目允许，原地改 `next`。
- 循环结束后必有一边还剩一串，直接把 `cur.next` 指向剩余链头即可。
- 返回 `dummy.next`：哑节点的存在就是为了最后这一句不用判断“哪个才是头”。

## 4. 易错点清单

1. **`cur = cur.next` 忘写**：死循环或一直改同一个节点。
2. **返回 `dummy` 而不是 `dummy.next`**：多出一个值为 0 的哑节点。
3. **`while a and b` 后剩余段忘了接**：结果丢一半。
4. **建链时头丢了**：只留一个 `cur` 变量来回走，最后找不到链头——用 dummy 解决。
5. **用 `== None` 判断**：规范写法是 `is None`（`==` 比内容、`is` 比身份）。

## 5. 变式练习

- 合并 K 个有序链（两两归并，或维护最小堆，呼应 ex4）。
- 不新建任何节点、原地“拆链重组”排序一个乱序链表。
- 给 `ListNode` 加 `__repr__`，让 `print(node)` 直接显示整条链，调试更爽。
