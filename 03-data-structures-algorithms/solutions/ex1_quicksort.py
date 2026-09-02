"""ex1 参考答案。"""
import random
from typing import List, Optional


def quicksort_functional(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort_functional(left) + mid + quicksort_functional(right)


def _partition(arr: List[int], lo: int, hi: int) -> int:
    pivot = arr[hi]
    i = lo - 1
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


def quicksort_inplace(arr: List[int], lo: int = 0, hi: Optional[int] = None) -> None:
    if hi is None:
        hi = len(arr) - 1
    if lo >= hi:
        return
    p = _partition(arr, lo, hi)
    quicksort_inplace(arr, lo, p - 1)
    quicksort_inplace(arr, p + 1, hi)


def main() -> None:
    for _ in range(5):
        data = [random.randint(-100, 100) for _ in range(20)]
        assert quicksort_functional(data) == sorted(data)
        quicksort_inplace(data)
        assert data == sorted(data)
    assert quicksort_functional([]) == []
    print("quicksort OK")


if __name__ == "__main__":
    main()
