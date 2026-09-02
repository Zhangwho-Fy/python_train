"""ex3 参考答案。"""
import functools
from functools import lru_cache


@lru_cache(maxsize=None)
def fib_lru(n: int) -> int:
    if n < 2:
        return n
    return fib_lru(n - 1) + fib_lru(n - 2)


def memoize(fn):
    cache = {}

    @functools.wraps(fn)
    def wrapper(n: int) -> int:
        if n in cache:
            return cache[n]
        cache[n] = fn(n)
        return cache[n]

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
