"""ex1 参考答案。"""
import asyncio
import time

import httpx

URL = "https://httpbin.org/delay/1"


def sync_fetch(url: str, times: int = 3) -> None:
    with httpx.Client(timeout=20) as client:
        for i in range(times):
            client.get(url)
            print(f"sync #{i + 1} done")


async def async_fetch_all(url: str, times: int = 3) -> None:
    async with httpx.AsyncClient(timeout=20) as client:
        async def one(i: int) -> None:
            await client.get(url)
            print(f"async #{i + 1} done")

        await asyncio.gather(*(one(i) for i in range(times)))


def main() -> None:
    t0 = time.perf_counter()
    sync_fetch(URL)
    print(f"sync 总耗时 {time.perf_counter() - t0:.2f}s")

    t0 = time.perf_counter()
    asyncio.run(async_fetch_all(URL))
    print(f"async 总耗时 {time.perf_counter() - t0:.2f}s")


if __name__ == "__main__":
    main()
