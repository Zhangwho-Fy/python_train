"""ex2: 解析本地 HTML 文章列表。"""


def parse_articles(html_path: str) -> list:
    # TODO: BeautifulSoup 解析 li.article，提取 a 的文本/href 和 span.date
    return []


def main() -> None:
    articles = parse_articles("exercises/sample.html")
    for a in articles:
        print(a)
    # TODO: 写入 articles.json


if __name__ == "__main__":
    main()
