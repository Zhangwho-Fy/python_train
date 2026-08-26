"""ex1: 同步 vs 异步 HTTP 请求。"""


def sync_fetch(url: str, times: int = 3) -> None:
    # TODO: httpx.Client 循环请求
    pass


async def async_fetch_all(url: str, times: int = 3) -> None:
    # TODO: httpx.AsyncClient + asyncio.gather 并发请求
    pass


def main() -> None:
    url = "https://httpbin.org/delay/1"
    # TODO: 分别计时并打印两种总耗时
    pass


if __name__ == "__main__":
    main()
