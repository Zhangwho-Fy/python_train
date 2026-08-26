"""ex4: 带重试和限速的爬虫。"""


def fetch_with_retry(url: str, retries: int = 3) -> str:
    # TODO: 循环尝试 requests.get；失败 sleep(2 ** attempt) 后重试
    return ""


def crawl(urls: list) -> None:
    # TODO: 逐个抓取，每次间隔 1 秒，打印状态码
    pass


def main() -> None:
    crawl(["https://example.com", "https://example.org"])


if __name__ == "__main__":
    main()
