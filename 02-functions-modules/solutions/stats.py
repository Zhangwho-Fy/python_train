"""ex3 参考答案。"""
from typing import List


def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)


def median(xs: List[float]) -> float:
    ordered = sorted(xs)
    n = len(ordered)
    mid = n // 2
    if n % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def std(xs: List[float]) -> float:
    m = mean(xs)
    variance = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return variance ** 0.5


if __name__ == "__main__":
    data = [float(x) for x in range(1, 101)]
    print(f"mean={mean(data):.2f}, median={median(data):.2f}, std={std(data):.2f}")
