"""ex1 参考答案。"""
import functools
import time


def timer(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"{fn.__name__} 耗时 {elapsed_ms:.2f} ms")
        return result

    return wrapper


@timer
def sum_range(n: int) -> int:
    return sum(range(n))


def main() -> None:
    result = sum_range(10 ** 6)
    print(f"result = {result}")


if __name__ == "__main__":
    main()
