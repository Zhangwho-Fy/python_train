"""ex1 参考答案。"""
from typing import Callable, List, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def my_map(fn: Callable[[T], R], xs: List[T]) -> List[R]:
    result = []
    for x in xs:
        result.append(fn(x))
    return result


def my_filter(pred: Callable[[T], bool], xs: List[T]) -> List[T]:
    result = []
    for x in xs:
        if pred(x):
            result.append(x)
    return result


def main() -> None:
    nums = list(range(1, 11))
    evens = my_filter(lambda x: x % 2 == 0, nums)
    squares = my_map(lambda x: x * x, evens)
    print(squares)
    assert squares == [4, 16, 36, 64, 100]


if __name__ == "__main__":
    main()
