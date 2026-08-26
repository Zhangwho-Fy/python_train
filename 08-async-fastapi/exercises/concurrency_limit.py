"""ex3: 信号量限流。"""
import asyncio


async def worker(i: int, sem: asyncio.Semaphore) -> None:
    # TODO: async with sem: 打印开始/结束
    pass


async def main() -> None:
    sem = asyncio.Semaphore(3)
    # TODO: gather 10 个 worker
    pass


if __name__ == "__main__":
    asyncio.run(main())
