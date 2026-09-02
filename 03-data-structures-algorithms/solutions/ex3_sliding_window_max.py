"""ex3 参考答案。"""
from collections import deque
from typing import List


def max_sliding_window(nums: List[int], k: int) -> List[int]:
    q = deque()
    result = []
    for i, x in enumerate(nums):
        while q and nums[q[-1]] <= x:
            q.pop()
        q.append(i)
        if q[0] <= i - k:
            q.popleft()
        if i >= k - 1:
            result.append(nums[q[0]])
    return result


def main() -> None:
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    assert max_sliding_window(nums, 3) == [3, 3, 5, 5, 6, 7]
    assert max_sliding_window([1], 1) == [1]
    print("sliding window OK")


if __name__ == "__main__":
    main()
