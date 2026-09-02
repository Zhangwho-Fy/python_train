# ex1 async_vs_sync 考点详解

## 题目回顾

用 `httpx` 分别以同步和异步方式请求 `https://httpbin.org/delay/1` **三次**，打印两种方式的总耗时，体会“I/O 等待时并发”的收益。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `async def` / `await` | Python 的协程语法 | 定义异步函数、等待 I/O |
| `asyncio.run(main())` | 启动事件循环跑协程 | 入口 |
| `httpx.AsyncClient` | 异步 HTTP 客户端 | 发请求 |
| `asyncio.gather` | 并发跑多个协程 | 三个请求一起发 |
| `httpx.Client` | 同步客户端 | 对照组 |
| I/O 密集 vs CPU 密集 | 等网络时 async 才划算 | 体会 3s vs 1s |

## 1. async/await 是什么

```python
async def one_request():
    ...
```

- `async def` 定义的函数**调用时不执行**，返回一个 coroutine 对象，必须等它被 `await` 或交给事件循环才会跑。
- `await` 表示“这里要等 I/O（网络/磁盘/睡眠），先让出控制权给事件循环，让别的协程跑”。C++ 对照：C++20 coroutine / `co_await`。
- Python 事件循环就像单线程调度器：一个协程在 `await` 处暂停，调度器切到下一个——并发，但不是多线程并行。

## 2. 同步版：一个个等

```python
import httpx
import time

def sync_fetch(url: str, times: int = 3) -> None:
    with httpx.Client() as client:
        for _ in range(times):
            resp = client.get(url, timeout=30)
            print(f"sync 完成, status={resp.status_code}")
```

`httpbin.org/delay/1` 让每个请求“睡 1 秒再返回”。同步版三个请求**串行**：约 3 秒+。

## 3. 异步版：一起等

```python
import asyncio

async def async_fetch_all(url: str, times: int = 3) -> None:
    async with httpx.AsyncClient() as client:

        async def one(_):                 # 单个请求的协程
            resp = await client.get(url, timeout=30)
            print(f"async 完成, status={resp.status_code}")

        await asyncio.gather(*(one(i) for i in range(times)))
```

- `httpx.AsyncClient` 是异步客户端，`await client.get(...)` 发请求。
- `asyncio.gather(*协程们)`：把多个协程交给事件循环**并发**跑，全部完成后返回。这里三个 `delay/1` 请求同时发出，总耗时约 1 秒+。
- `*(one(i) for i in range(times))` 是“展开生成器成 3 个位置参数”的写法。
- 内层 `async def one` 定义在 `async with client` 里面，是为了让每个协程共享同一个 client。

## 4. 主入口与计时

```python
def main() -> None:
    url = "https://httpbin.org/delay/1"

    t0 = time.perf_counter()
    sync_fetch(url)
    print(f"同步总耗时: {time.perf_counter() - t0:.2f}s")

    t1 = time.perf_counter()
    asyncio.run(async_fetch_all(url))     # 事件循环入口
    print(f"异步总耗时: {time.perf_counter() - t1:.2f}s")
```

- `asyncio.run(coro)`：创建事件循环 → 跑完协程 → 关闭。脚本级入口只用它，不要在 `async` 函数里嵌套调用。
- 期望输出：同步约 3s+，异步约 1s+（不是 1/3 的关系之外还要加网络开销）。

## 5. 什么时候值得用 async

- **I/O 密集**（网络请求、读写、等待下游）：await 期间让位，收益大。
- **CPU 密集**（纯计算）：async 帮不上忙（协程不让出 CPU），要用多进程（`concurrent.futures`/`multiprocessing`）。
- Python 的 GIL 使得“多线程跑 CPU 计算”也受限——选型顺序：I/O 并发用 async，CPU 并行用多进程。

## 6. 易错点清单

1. **调 async 函数不加 await**：拿到的是 coroutine 对象，请求根本没发，还有 “coroutine was never awaited” 警告。
2. **`asyncio.run` 嵌在协程里**：只能从“非 async 的入口”调用一次。
3. **忘了 `async with httpx.AsyncClient()`**：用同步 Client 在协程里发请求，会阻塞整个事件循环，async 白写。
4. **`asyncio.gather` 忘 await**：gather 本身是协程，不 await 不执行。
5. **httpbin.org 不稳定**：连不上就先起本地服务（如 FastAPI 的 sleep 端点）测试。

## 7. 变式练习

- 打印每个请求“实际完成时刻”，确认三个请求的重叠区间。
- 用 `asyncio.create_task` + `await asyncio.wait(...)` 重写 gather，对比 API。
- 请求数加到 10，看同步 10s vs 异步 ~1s，加深体感。
