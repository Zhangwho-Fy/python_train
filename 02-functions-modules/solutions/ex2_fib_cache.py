"""ex2 参考答案。"""


def make_fib_cached():
    cache = {0: 0, 1: 1}
    stats = {"calls": 0, "hits": 0}

    def fib(n: int) -> int:
        stats["calls"] += 1
        if n in cache:
            stats["hits"] += 1
            return cache[n]
        cache[n] = fib(n - 1) + fib(n - 2)
        return cache[n]

    return fib, stats


def main() -> None:
    fib_cached, stats = make_fib_cached()
    print(f"fib(30) = {fib_cached(30)}")
    print(f"缓存版: 总调用 {stats['calls']}, 命中 {stats['hits']}")

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
