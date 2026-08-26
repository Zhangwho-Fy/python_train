"""ex4 参考答案。"""


def word_frequency(text: str, top: int = 5) -> list:
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return ranked[:top]


def main() -> None:
    text = "the quick brown fox jumps over the lazy dog the"
    for word, count in word_frequency(text):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
