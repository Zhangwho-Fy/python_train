"""ex4: 统计词频并输出前 top 个。"""


def word_frequency(text: str, top: int = 5) -> list:
    # TODO: 小写化、split() 拆词、dict 计数、按次数降序取前 top
    return []


def main() -> None:
    text = "the quick brown fox jumps over the lazy dog the"
    for word, count in word_frequency(text):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
