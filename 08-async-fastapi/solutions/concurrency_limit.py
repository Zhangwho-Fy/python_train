"""ex3 参考答案。"""
import asyncio
import time


async def worker(i: int, sem: asyncio.Semaphore) -> None:
    async with sem:
        print(f"[{time.strftime('%H:%M:%S')}] start {i}")
        await asyncio.sleep(0.5)
        print(f"[{time.strftime('%H:%M:%S')}] done  {i}")


async def main() -> None:
    sem = asyncio.Semaphore(3)
    await asyncio.gather(*(worker(i, sem) for i in range(10)))


if __name__ == "__main__":
    asyncio.run(main())
