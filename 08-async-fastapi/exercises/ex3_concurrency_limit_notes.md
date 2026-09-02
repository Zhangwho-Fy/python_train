# ex3 concurrency_limit 考点详解

## 题目回顾

`asyncio.Semaphore(3)` 限制同时进行的 10 个异步任务：打印每个任务的开始/结束时间戳，观察任意时刻最多 3 个并发。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `asyncio.Semaphore(n)` | 信号量，最多 n 个同时进入 | 限流并发数 |
| `async with sem:` | 进入时 acquire、退出时 release | 自动管理信号量 |
| `asyncio.gather` | 并发跑协程 | 同时启动 10 个 worker |
| `asyncio.sleep` | 异步等待（不阻塞事件循环） | 模拟任务耗时 |
| 时间戳 | 打印观察并发窗口 | `time.time()` |

## 1. 信号量：并发限流

```python
import asyncio
import time

async def worker(i: int, sem: asyncio.Semaphore) -> None:
    async with sem:                       # 拿许可；没有就排队等
        print(f"{time.time():.3f} start  #{i}")
        await asyncio.sleep(1)            # 模拟 1 秒任务
        print(f"{time.time():.3f} end    #{i}")

async def main() -> None:
    sem = asyncio.Semaphore(3)            # 最多 3 个同时执行
    await asyncio.gather(*(worker(i, sem) for i in range(10)))

if __name__ == "__main__":
    asyncio.run(main())
```

- `Semaphore(3)` 内部计数从 3 开始；`async with sem:` 进入时拿一个（计数 -1），退出时还一个（计数 +1）。
- 前 3 个 worker 立刻开始；第 4 个在 `async with sem` 处**排队等待**，直到有 worker 结束释放许可。于是任意时刻最多 3 个在跑。
- 不用 `async with` 而手写 `await sem.acquire() / sem.release()` 容易漏 release（异常时卡死），`async with` 是安全写法。
- C++ 对照：`std::counting_semaphore`；概念一致。

## 2. gather 与事件循环

- `asyncio.gather(*(worker(i, sem) for i in range(10)))`：创建 10 个协程一起调度。谁先谁后由事件循环决定，**打印顺序不保证**。
- `await asyncio.sleep(1)` 和 `time.sleep(1)` 不同：前者让出事件循环（别的任务能跑），后者阻塞整个线程（async 全卡住）。协程里永远用 `asyncio.sleep`。
- 观察时间戳：三个一组开始，约 1 秒后第二批三个开始——总耗时约 4 秒（10 个任务 / 每次 3 个并发，向上取整批次 + 每批 1 秒）。

## 3. 为什么要限流

没有信号量时 `gather` 会**同时**发起 10 个任务；真实场景里可能是 10 个 HTTP 请求打向同一个下游——下游扛不住、你被限流/封禁。信号量让并发数可控（07 的爬虫如果改 async，就用它限速）。

## 4. 易错点清单

1. **`Semaphore` 忘共享**：每个 worker 里 `asyncio.Semaphore(3)` 新建一个，等于没限流；必须在外层建、传进去。
2. **在 `async with sem` 外 await**：任务不占许可也能并发，日志会显示超过 3 个。
3. **协程里用 `time.sleep`**：阻塞整个事件循环，10 个任务变回串行，限流日志会显示“每次只有 1 个”。
4. **`gather` 忘 await**：main 返回协程，什么都不跑。
5. **打印顺序当并发数依据**：start 可能瞬时交错，观察“同一秒内 start 的数量”和 end 的成批出现。

## 5. 变式练习

- 打印“当前进行中数量”：任务里维护一个计数器，start +1、end -1，每步输出最大值。
- 用 `asyncio.wait_for(worker(...), timeout=2)` 给单个任务加超时。
- 改成每任务带随机 sleep 时长，观察信号量的动态让位。
