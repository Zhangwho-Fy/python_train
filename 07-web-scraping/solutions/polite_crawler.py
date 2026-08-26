"""ex4 参考答案。"""
import time

import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
}


def fetch_with_retry(url: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            wait = 2 ** attempt
            print(f"第 {attempt + 1} 次失败: {e}，{wait}s 后重试")
            time.sleep(wait)
    raise RuntimeError(f"重试 {retries} 次仍然失败: {url}")


def crawl(urls: list) -> None:
    for url in urls:
        try:
            text = fetch_with_retry(url)
            print(f"{url} -> {len(text)} 字节")
        except RuntimeError as e:
            print(e)
        time.sleep(1)


def main() -> None:
    crawl(["https://example.com", "https://example.org"])


if __name__ == "__main__":
    main()
