"""ex4: 逐行处理大文件，统计行长度分布。"""


def lines(path: str):
    # TODO: 逐行 yield，不 read() 全文件
    pass


def bucket_of(length: int) -> str:
    # TODO: 0-9 → "0-9", 10-19 → "10-19", ...
    return ""


def main() -> None:
    buckets = {}
    for line in lines("exercises/sample.txt"):
        b = bucket_of(len(line.rstrip("\n")))
        buckets[b] = buckets.get(b, 0) + 1
    for b in sorted(buckets):
        print(f"{b}: {buckets[b]} 行")


if __name__ == "__main__":
    main()
