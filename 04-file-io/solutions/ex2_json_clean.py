"""ex2 参考答案。"""
import json
from pathlib import Path


def clean_students(src: str, dst: str, threshold: int = 80) -> list:
    raw = json.loads(Path(src).read_text(encoding="utf-8"))
    passed = [s for s in raw["students"] if s["score"] >= threshold]
    passed.sort(key=lambda s: s["score"], reverse=True)
    Path(dst).write_text(
        json.dumps(passed, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return passed


def main() -> None:
    here = Path(__file__).parent
    src = here.parent / "exercises" / "students.json"
    dst = here / "cleaned.json"
    cleaned = clean_students(str(src), str(dst))
    for s in cleaned:
        print(s["name"], s["score"])


if __name__ == "__main__":
    main()
