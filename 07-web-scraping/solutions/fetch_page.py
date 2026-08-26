"""ex1 参考答案。"""
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def fetch(url: str, save_to: str) -> str:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    Path(save_to).parent.mkdir(parents=True, exist_ok=True)
    Path(save_to).write_text(resp.text, encoding="utf-8")
    soup = BeautifulSoup(resp.text, "html.parser")
    return soup.title.get_text(strip=True) if soup.title else ""


def main() -> None:
    here = Path(__file__).parent
    title = fetch("https://example.com", str(here.parent / "data" / "example.html"))
    print(f"标题: {title}")


if __name__ == "__main__":
    main()
