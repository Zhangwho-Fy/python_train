# ex2 chat_api 考点详解

## 题目回顾

写一个 FastAPI 服务：

- `GET /health` → `{"status": "ok"}`
- `POST /api/chat`，接收 `{"message": str}`，返回 `{"reply": "你说了: " + message}`

请求/响应都用 pydantic 模型定义，启动后浏览器开 `/docs` 直接测试。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `FastAPI()` | 应用实例 | `app = FastAPI()` |
| `@app.get / @app.post` | 注册路由 | 两个端点 |
| pydantic 请求模型 | 函数参数声明模型即自动校验 | `req: ChatRequest` |
| pydantic 响应模型 | `response_model=` 约束返回结构 | `ChatResponse` |
| uvicorn | ASGI 服务器 | `uvicorn ex2_chat_api:app --reload` |
| `/docs` | 自动生成交互文档 | 浏览器测试 |

## 1. 完整代码

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return ChatResponse(reply="你说了: " + req.message)
```

- `@app.get(...)` / `@app.post(...)` 注册路由；函数返回 dict 或 pydantic 模型，FastAPI 自动序列化成 JSON。
- 函数参数声明成 `req: ChatRequest` 后，FastAPI 会把请求体 JSON 解析+校验成模型：`message` 缺失或不是字符串时，自动返回 422 和详细错误——05 阶段练的 pydantic 在这里正式上岗。
- 端点函数可以不用 `async def`：FastAPI 会把普通 `def` 端点放到线程池跑。只有需要自己 `await` 时才写 `async def`。

## 2. 启动与测试

```bash
cd 08-async-fastapi
uvicorn ex2_chat_api:app --reload
```

- `ex2_chat_api:app` = “模块名:应用变量名”。文件名现在带 ex 前缀，启动命令跟着变（README/代码注释里旧写的 `chat_api:app` 已过时，以这个为准）。
- `--reload` 改代码自动重启，适合开发。
- 浏览器开 `http://127.0.0.1:8000/docs`：Swagger UI 自动生成，每个端点有“Try it out”，不用 curl 也能测。

命令行验证：

```bash
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'
# {"reply":"你说了: 你好"}
```

## 3. 路由与 HTTP 语义

- `GET` 无副作用，适合健康检查；`POST` 提交数据，适合聊天这种“请求体驱动”的接口。
- 路径 `/api/chat` 是设计约定：把“业务 API”和页面区分开，后续版本化（`/v1/...`）也方便。

## 4. 易错点清单

1. **没装依赖**：`pip install -r requirements.txt`（fastapi + uvicorn + pydantic）。
2. **uvicorn 模块名写错**：要在 `08-async-fastapi/` 目录下运行，且模块名用文件名（现在叫 `ex2_chat_api`）。
3. **请求模型字段名对不上**：客户端发 `{"text": ...}` 而模型声明 `message`，会 422。
4. **`response_model` 忘记**：返回 dict 也能跑，但少了结构约束和文档；加上更规范。
5. **端点函数忘了 `req` 参数类型注解**：不注解 FastAPI 不知道从哪取数，直接 422 或当成 query 参数。

## 5. 变式练习

- 给 `ChatRequest` 加 `history: list = []` 可选字段，为 09 最终项目的对话历史做准备。
- 加 `GET /api/chat/{message}` 路径参数版，体会 query/path/body 三种取参方式。
- 改 `async def` + 端点里 `await asyncio.sleep(0.1)`，模拟慢响应；进阶版（README ex4）用 `StreamingResponse` 逐字输出。
