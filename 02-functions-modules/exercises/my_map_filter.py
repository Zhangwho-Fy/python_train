"""ex1: 手写 map / filter。"""
from typing import Callable, List, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def my_map(fn: Callable[[T], R], xs: List[T]) -> List[R]:
    # TODO: for 循环 + append
    return []


def my_filter(pred: Callable[[T], bool], xs: List[T]) -> List[T]:
    # TODO: for 循环 + 条件 append
    return []


def main() -> None:
    nums = list(range(1, 11))
    evens = my_filter(lambda x: x % 2 == 0, nums)
    squares = my_map(lambda x: x * x, evens)
    print(squares)
    assert squares == [4, 16, 36, 64, 100]


if __name__ == "__main__":
    main()
