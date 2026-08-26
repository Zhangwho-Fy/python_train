"""ex2: 过滤并排序学生数据。"""


def clean_students(src: str, dst: str, threshold: int = 80) -> list:
    # TODO: json.load → 过滤 score >= threshold → 按分数降序 → json.dump
    return []


def main() -> None:
    cleaned = clean_students("exercises/students.json", "cleaned.json")
    for s in cleaned:
        print(s["name"], s["score"])


if __name__ == "__main__":
    main()
