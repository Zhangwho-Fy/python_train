# 08 异步与 FastAPI

## 本阶段目标

理解 async/await，能写一个简单的 HTTP API——这是 LangChain 最终项目“服务化”的地基。

## C++ 对照

| Python | C++ 类似物 |
| --- | --- |
| `async def f()` / `await` | C++20 coroutine / `co_await` |
| `asyncio.gather` | `std::async` / `when_all` |
| `asyncio.Semaphore` | 信号量 |
| FastAPI + uvicorn | 自带路由、校验、文档的 Web 框架 |
| `httpx.AsyncClient` | 异步 HTTP 客户端 |

## 要点

- **async 函数不执行，返回 coroutine 对象**：要 `await` 或 `asyncio.run(...)` 才有实际效果。
- **I/O 密集用 async 收益大；CPU 密集用多进程**（`concurrent.futures`）。
- **FastAPI 的 `async def` 端点跑在事件循环里，普通 `def` 端点跑在线程池**。
- **请求体用 pydantic 模型接收**，响应自动 JSON 化——呼应 05 阶段。
- 启动服务：`uvicorn ex2_chat_api:app --reload`，打开 `http://127.0.0.1:8000/docs` 有自动生成的交互文档。

## 与 LangChain 的关系

最终项目的形态就是“FastAPI 接收问题 → 调 LangChain 链 → 流式返回”。
`StreamingResponse` 和 `asyncio` 是 LangChain `stream()` 落地的载体。

## 练习题

每题在 `exercises/` 里有配套考点详解（`exN_xxx_notes.md`），卡住先翻详解再翻答案。

### ex1 async_vs_sync

考点详解：`exercises/ex1_async_vs_sync_notes.md`

用 `httpx` 分别同步和异步请求 `https://httpbin.org/delay/1` 三次，打印两种总耗时，体会并发收益。

### ex2 chat_api

考点详解：`exercises/ex2_chat_api_notes.md`

FastAPI：

- `GET /health` → `{"status": "ok"}`
- `POST /api/chat`，接收 `{"message": str}`，返回 `{"reply": "你说了: " + message}`

用 pydantic 定义请求/响应模型。启动后浏览器开 `/docs` 直接测试。
启动命令：`uvicorn ex2_chat_api:app --reload`（在 `08-async-fastapi/` 目录下）。

### ex3 concurrency_limit

考点详解：`exercises/ex3_concurrency_limit_notes.md`

`asyncio.Semaphore(3)` 限制同时进行的 10 个异步任务，打印每个任务的开始/结束时间戳，
观察任意时刻最多 3 个并发。

### ex4 stream（进阶，可选）

把 ex2 的 chat 端点改成 `StreamingResponse`，每次 `yield` 一个字（模拟打字机）。
体会 LangChain 的 `stream()` 为什么这样设计。

## 环境

```bash
pip install -r requirements.txt
```

## 期望输出示例

- ex1：同步约 3s+，异步约 1s+（三个请求并发）
- ex2：`{"reply": "你说了: 你好"}`
- ex3：日志里任意时刻同时进行中的任务数不超过 3
