"""ex1: 快排两版。"""
import random
from typing import List, Optional


def quicksort_functional(arr: List[int]) -> List[int]:
    # TODO: 基准值取中间；小于/等于/大于三组，递归拼接
    return arr


def _partition(arr: List[int], lo: int, hi: int) -> int:
    # TODO: 以 arr[hi] 为基准，原地分区，返回基准最终下标
    return lo


def quicksort_inplace(arr: List[int], lo: int = 0, hi: Optional[int] = None) -> None:
    if hi is None:
        hi = len(arr) - 1
    # TODO: 递归调用 _partition 并处理左右两段


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
