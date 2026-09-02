"""ex1: 统计 sample.txt 的词频 Top 10。"""


def count_words(path: str) -> list:
    # TODO: 读文件、小写化、去标点、Counter 计数
    return []


def main() -> None:
    for word, count in count_words("exercises/sample.txt"):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
