"""ex2 参考答案。"""
from typing import List, Optional


class ListNode:
    def __init__(self, val: int = 0, next_node: Optional["ListNode"] = None):
        self.val = val
        self.next = next_node


def from_list(xs: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    cur = dummy
    for x in xs:
        cur.next = ListNode(x)
        cur = cur.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> List[int]:
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


def merge_two_lists(a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode()
    cur = dummy
    while a and b:
        if a.val <= b.val:
            cur.next = a
            a = a.next
        else:
            cur.next = b
            b = b.next
        cur = cur.next
    cur.next = a or b
    return dummy.next


def main() -> None:
    a = from_list([1, 2, 4])
    b = from_list([1, 3, 4])
    merged = merge_two_lists(a, b)
    assert to_list(merged) == [1, 1, 2, 3, 4, 4]
    assert to_list(merge_two_lists(None, from_list([0]))) == [0]
    print("merge OK")


if __name__ == "__main__":
    main()
