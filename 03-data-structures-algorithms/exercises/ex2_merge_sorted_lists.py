"""ex2: 合并两个有序链表。"""
from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next_node: Optional["ListNode"] = None):
        self.val = val
        self.next = next_node


def from_list(xs: List[int]) -> Optional[ListNode]:
    # TODO: 把 list 建成链表
    return None


def to_list(head: Optional[ListNode]) -> List[int]:
    # TODO: 遍历链表转 list
    return []


def merge_two_lists(a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
    # TODO: 双指针归并，返回新链头（可以直接改 next，不用新建节点）
    return None


def main() -> None:
    a = from_list([1, 2, 4])
    b = from_list([1, 3, 4])
    merged = merge_two_lists(a, b)
    assert to_list(merged) == [1, 1, 2, 3, 4, 4]
    assert to_list(merge_two_lists(None, from_list([0]))) == [0]
    print("merge OK")


if __name__ == "__main__":
    main()
