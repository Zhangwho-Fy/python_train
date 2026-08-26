"""ex4 参考答案。"""
import time
from contextlib import contextmanager


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_ms = (time.perf_counter() - self.start) * 1000
        print(f"with 块耗时 {elapsed_ms:.2f} ms")
        return False


@contextmanager
def timed():
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"with 块耗时 {elapsed_ms:.2f} ms")


def main() -> None:
    with Timer() as t:
        time.sleep(0.01)

    with timed():
        time.sleep(0.01)

    print("timer_context OK")


if __name__ == "__main__":
    main()
