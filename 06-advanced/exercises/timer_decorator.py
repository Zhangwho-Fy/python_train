"""ex1: 计时装饰器。"""
import time


def timer(fn):
    # TODO: 包一层，记录 perf_counter 差值，打印 fn.__name__ 和毫秒
    return fn


@timer
def sum_range(n: int) -> int:
    return sum(range(n))


def main() -> None:
    result = sum_range(10 ** 6)
    print(f"result = {result}")


if __name__ == "__main__":
    main()
