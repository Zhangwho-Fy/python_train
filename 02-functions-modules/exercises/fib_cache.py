"""ex2: 记忆化斐波那契。"""


def make_fib_cached():
    cache = {0: 0, 1: 1}
    stats = {"calls": 0, "hits": 0}

    def fib(n: int) -> int:
        # TODO: stats["calls"] += 1；命中缓存时 stats["hits"] += 1
        return 0

    return fib, stats


def fib_naive(n: int) -> int:
    # TODO: 朴素递归，用于对比
    return 0


def main() -> None:
    fib_cached, stats = make_fib_cached()
    print(f"fib(30) = {fib_cached(30)}")
    print(f"缓存版: 总调用 {stats['calls']}, 命中 {stats['hits']}")

    # 朴素版加个计数器对比
    calls = {"n": 0}
    def fib_naive_count(n: int) -> int:
        calls["n"] += 1
        if n < 2:
            return n
        return fib_naive_count(n - 1) + fib_naive_count(n - 2)

    naive_calls = fib_naive_count(30)
    print(f"朴素版 fib(30) 调用次数: {calls['n']}（结果为 {naive_calls}）")


if __name__ == "__main__":
    main()
