# ex1 chat_direct 考点详解（第 1 步：先搞清楚“调 LLM 到底发生了什么”）

## 题目回顾

不装 LangChain，直接用 `openai` SDK 跑一轮对话：读 `.env` 配置 → 建客户端 → `chat.completions.create(...)` → 取回答文本。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `.env` + `python-dotenv` | 密钥放环境变量，不进代码库 | `load_dotenv()` + `os.getenv` |
| `OpenAI(api_key=..., base_url=...)` | 兼容 OpenAI 格式的客户端 | DeepSeek/千问/Ollama 都能接 |
| 消息结构 `system / user / assistant` | Chat API 的输入是“角色消息列表” | 系统提示 + 用户问题 |
| `chat.completions.create(...)` | 发起一次补全 | `temperature=0.7` |
| `choices[0].message.content` | 从响应里取文本 | 返回给调用方 |
| 鉴权/模型名错误 | 401/404 最常见 | key 或 model 写错 |

## 1. 配置：`.env` 与 `load_dotenv`

```python
import os
from dotenv import load_dotenv

load_dotenv()        # 把 .env 里的 KEY=VALUE 读进环境变量

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
```

- `.env` 格式：`OPENAI_API_KEY=sk-...` 一行一个。**永远不要把 .env 提交进 git**（仓库 .gitignore 已处理）。
- 没有 OpenAI key 的替代：改 `.env` 里的 `OPENAI_BASE_URL` 和 `OPENAI_MODEL` 即可指向 DeepSeek（`https://api.deepseek.com`）、通义千问或本地 Ollama——它们都兼容 OpenAI Chat 格式。

## 2. 发消息：消息数组是输入

```python
from openai import OpenAI

def chat_once(question: str) -> str:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "你是一个简洁的中文助手。"},
            {"role": "user", "content": question},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content
```

- Chat 模型的输入**不是一句话，而是角色消息列表**：`system` 设定人设/规则，`user` 是当前问题，多轮对话会把历史 `assistant` 消息也加进来。
- `temperature` 控制随机性：0 接近确定，越高越发散。调试时先调到 0 排除随机干扰。
- 返回值是对象不是字符串：`response.choices[0].message.content` 里取文本——`choices` 是列表（未来支持多个候选），下标 0 是默认主回答。

## 3. 常见错误对照表

| 报错 | 原因 |
| --- | --- |
| `401 Unauthorized` / AuthenticationError | API key 错、没配、或环境变量没读到 |
| `404` / model not found | 模型名写错（`deepseek-chat` vs `gpt-4o-mini` 别混） |
| `base_url` 结尾缺 `/v1` | 部分兼容服务必须带 `/v1` |
| 空 `choices` 或 content 为 None | 触发了安全过滤或 max_tokens 太小 |

## 4. 这道题在练什么

后面所有 LangChain 代码（PromptTemplate、LCEL、Agent）最终都归结为“把消息数组发给模型、解析返回”。先裸调一次 SDK，你才知道框架帮你封装了什么：

- PromptTemplate = 自动拼 system/user 消息；
- OutputParser = 自动解析 `content` 字符串；
- ChatModel 封装 = 自动读环境变量建 client。

## 5. 易错点清单

1. **忘了 `load_dotenv()`**：`os.getenv` 全空，客户端拿 None 报 401。
2. **把 key 硬编码进代码**：提交后全网都能看到，立刻作废换新。
3. **`messages` 里角色写错**：只有 system/user/assistant/tool 几个合法角色。
4. **不检查 `response.choices`**：直接 `[0]` 在空列表时 IndexError。
5. **在没网/没 key 的环境跑**：这道题必须能访问模型端点；先用 README 的替代方案（Ollama 本地）兜底。

## 6. 变式练习

- 打印 `response` 全文，观察除 content 外还有哪些字段（usage、finish_reason 等）。
- 实现两轮对话：把上一轮 assistant 回答拼进 messages 再问。
- 用 `max_tokens=50` 强制截断，观察回答被切断时的 finish_reason。
