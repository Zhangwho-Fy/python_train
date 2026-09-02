"""ex1 参考答案。"""
import re
from collections import Counter
from pathlib import Path


def count_words(path: str) -> list:
    text = Path(path).read_text(encoding="utf-8")
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return Counter(words).most_common(10)


def main() -> None:
    here = Path(__file__).parent
    src = here.parent / "exercises" / "sample.txt"
    for word, count in count_words(str(src)):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
