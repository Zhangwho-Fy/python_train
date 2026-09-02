"""ex3: lru_cache 与手写 memoize。"""
from functools import lru_cache


@lru_cache(maxsize=None)
def fib_lru(n: int) -> int:
    # TODO: n < 2 返回 n，否则递归
    return 0


def memoize(fn):
    cache = {}

    def wrapper(n: int) -> int:
        # TODO: 命中直接返回，否则算完存进去
        return fn(n)

    return wrapper


@memoize
def fib_memo(n: int) -> int:
    if n < 2:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


def main() -> None:
    assert fib_lru(100) == 354224848179261915075
    assert fib_memo(100) == fib_lru(100)
    print(f"fib_lru(100) = {fib_lru(100)}")
    print("fib_lru OK")


if __name__ == "__main__":
    main()
