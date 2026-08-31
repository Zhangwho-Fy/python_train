"""ex4: 统计词频并输出前 top 个。"""


def word_frequency(text: str, top: int = 5) -> list:
    # TODO: 小写化、split() 拆词、dict 计数、按次数降序取前 top
    count = {}
    for word in text.lower().split():
        count[word] = count.get(word, 0) + 1
    items = list(count.items())
    sorted_items = sorted(items, key=lambda item: item[1], reverse=True)
    return sorted_items[:top]


def main() -> None:
    text = "the quick brown fox jumps over the lazy dog the"
    for word, count in word_frequency(text):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
