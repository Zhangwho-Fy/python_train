"""ex4: with 计时，两种实现。"""
import time


class Timer:
    def __enter__(self):
        # TODO: 记录开始时间并返回 self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: 打印耗时
        return False  # 不吞异常


def timed():
    # TODO: @contextmanager 版本，yield 前记录开始时间，yield 后打印耗时
    pass


def main() -> None:
    with Timer() as t:
        time.sleep(0.01)

    with timed():
        time.sleep(0.01)

    print("timer_context OK")


if __name__ == "__main__":
    main()
