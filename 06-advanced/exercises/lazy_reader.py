"""ex5: 惰性读文件。"""
from pathlib import Path


def lazy_lines(path: str):
    # TODO: with open(...) 逐行 yield
    pass


def main() -> None:
    here = Path(__file__).parent
    src = here.parent.parent / "04-file-io" / "exercises" / "sample.txt"
    count = 0
    for i, line in enumerate(lazy_lines(str(src))):
        if i < 5:
            print(line.rstrip("\n"))
        count += 1
    print(f"总行数: {count}")


if __name__ == "__main__":
    main()
