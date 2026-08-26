"""ex3: 滑动窗口最大值（单调队列）。"""
from collections import deque
from typing import List


def max_sliding_window(nums: List[int], k: int) -> List[int]:
    # TODO: deque 存下标，保持队首到队尾单调递减；窗口滑出时 popleft
    return []


def main() -> None:
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    assert max_sliding_window(nums, 3) == [3, 3, 5, 5, 6, 7]
    assert max_sliding_window([1], 1) == [1]
    print("sliding window OK")


if __name__ == "__main__":
    main()
