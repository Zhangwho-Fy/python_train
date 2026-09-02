"""ex3: 统计工具模块。"""
from typing import List


def mean(xs: List[float]) -> float:
    # TODO
    return 0.0


def median(xs: List[float]) -> float:
    # TODO: 排序后取中间；偶数个取中间两数平均
    return 0.0


def std(xs: List[float]) -> float:
    # TODO: 样本标准差（除以 n-1）
    return 0.0


if __name__ == "__main__":
    data = [float(x) for x in range(1, 101)]
    print(f"mean={mean(data):.2f}, median={median(data):.2f}, std={std(data):.2f}")
