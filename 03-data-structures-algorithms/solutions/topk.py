"""ex4 参考答案。"""
import heapq
from typing import List


def top_k_sorted(nums: List[int], k: int) -> List[int]:
    return sorted(nums, reverse=True)[:k]


def top_k_nlargest(nums: List[int], k: int) -> List[int]:
    return heapq.nlargest(k, nums)


def top_k_manual_heap(nums: List[int], k: int) -> List[int]:
    heap = nums[:k]
    heapq.heapify(heap)
    for x in nums[k:]:
        if x > heap[0]:
            heapq.heapreplace(heap, x)
    return heap


def main() -> None:
    nums = [3, 1, 5, 2, 4]
    assert sorted(top_k_sorted(nums, 2)) == [4, 5]
    assert sorted(top_k_nlargest(nums, 2)) == [4, 5]
    assert sorted(top_k_manual_heap(nums, 2)) == [4, 5]
    print("topk OK")


if __name__ == "__main__":
    main()
