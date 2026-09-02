"""ex1: 下载一个网页。"""


def fetch(url: str, save_to: str) -> str:
    # TODO: requests.get(url, timeout=10)，检查 status_code，
    #       保存 text，返回标题（可以用 bs4 或正则取 <title>）
    return ""


def main() -> None:
    title = fetch("https://example.com", "data/example.html")
    print(f"标题: {title}")


if __name__ == "__main__":
    main()
