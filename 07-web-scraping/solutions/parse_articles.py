"""ex2 参考答案。"""
import json
from pathlib import Path

from bs4 import BeautifulSoup


def parse_articles(html_path: str) -> list:
    soup = BeautifulSoup(Path(html_path).read_text(encoding="utf-8"), "html.parser")
    articles = []
    for item in soup.select("li.article"):
        link = item.find("a")
        date = item.find("span", class_="date")
        articles.append(
            {
                "title": link.get_text(strip=True),
                "url": link["href"],
                "date": date.get_text(strip=True) if date else "",
            }
        )
    return articles


def main() -> None:
    here = Path(__file__).parent
    src = here.parent / "exercises" / "sample.html"
    articles = parse_articles(str(src))
    for a in articles:
        print(a)
    (here / "articles.json").write_text(
        json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
