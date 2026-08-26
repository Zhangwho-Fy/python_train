"""ex4 参考答案。"""
from pathlib import Path


def lines(path: str):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line


def bucket_of(length: int) -> str:
    start = (length // 10) * 10
    return f"{start}-{start + 9}"


def main() -> None:
    here = Path(__file__).parent
    src = here.parent / "exercises" / "sample.txt"
    buckets = {}
    for line in lines(str(src)):
        b = bucket_of(len(line.rstrip("\n")))
        buckets[b] = buckets.get(b, 0) + 1
    for b in sorted(buckets, key=lambda s: int(s.split("-")[0])):
        print(f"{b}: {buckets[b]} 行")


if __name__ == "__main__":
    main()
