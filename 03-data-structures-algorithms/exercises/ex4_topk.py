"""ex4: Top K 三种实现。"""
import heapq
from typing import List


def top_k_sorted(nums: List[int], k: int) -> List[int]:
    # TODO
    return []


def top_k_nlargest(nums: List[int], k: int) -> List[int]:
    # TODO
    return []


def top_k_manual_heap(nums: List[int], k: int) -> List[int]:
    # TODO: 维护大小 k 的最小堆：比堆顶大就替换
    return []


def main() -> None:
    nums = [3, 1, 5, 2, 4]
    assert sorted(top_k_sorted(nums, 2)) == [4, 5]
    assert sorted(top_k_nlargest(nums, 2)) == [4, 5]
    assert sorted(top_k_manual_heap(nums, 2)) == [4, 5]
    print("topk OK")


if __name__ == "__main__":
    main()
