# 09 LangChain：通向最终目标

## 前置

01~08 完成；至少：类与 pydantic（05）、装饰器/生成器（06）、HTTP 概念（07）、async/FastAPI（08）。

## 大模型与 API 基础

- Chat 消息结构：`system / user / assistant` 角色列表；
- 常用参数：`temperature`（随机性）、`max_tokens`、`top_p`；
- 供应商：OpenAI、DeepSeek、通义千问、本地 Ollama 都兼容 OpenAI Chat 格式，
  LangChain 用 `ChatOpenAI(base_url=...)` 都能接。

## LangChain 核心概念（对照你的工程经验）

| 概念 | 一句话 | 工程类比 |
| --- | --- | --- |
| `ChatModel` | 封装模型调用 | 一个 client 类 |
| `PromptTemplate` | 消息模板 + 变量注入 | `std::format` 模板 |
| `OutputParser` | 把模型文本转成结构化数据 | 反序列化 + 校验 |
| LCEL `\|` | 把组件串成管道 | 管道 / 责任链 |
| `Retriever` | 检索相关片段 | 搜索引擎接口 |
| `Tool` | 让模型能调你的函数 | 插件 / RPC 注册表 |
| `Agent` | 模型自己决定调哪个工具 | 决策循环 |

## 五步练习（每步一个文件，按顺序做）

每题在 `exercises/` 里有配套考点详解（`exN_xxx_notes.md`），卡住先翻详解再翻答案。

1. **ex1_chat_direct.py**：先不装 LangChain，直接用 `openai` SDK 跑一轮对话，
   搞懂“调 LLM 到底发生了什么”。
   考点详解：`exercises/ex1_chat_direct_notes.md`
2. **ex2_prompt_and_parse.py**：`ChatPromptTemplate` + `PydanticOutputParser`，
   让模型输出 JSON 并解析成 pydantic 对象（呼应 05 的 pydantic）。
   考点详解：`exercises/ex2_prompt_and_parse_notes.md`
3. **ex3_lcel_chain.py**：`prompt | model | StrOutputParser` 做“中文 → 英文 → 中文总结”两步链，
   体会 `|` 管道和变量流转。
   考点详解：`exercises/ex3_lcel_chain_notes.md`
4. **ex4_rag_chat.py**：加载 `docs/` 下的本地 markdown → 切块 → Chroma 向量库 →
   检索 top-k → 拼进 prompt 回答。这是最终项目的核心。
   考点详解：`exercises/ex4_rag_chat_notes.md`
5. **ex5_agent_tools.py**：定义 `get_current_time`、`search_files` 两个 `@tool`，
   让 Agent 自己选择调用，观察决策过程。
   考点详解：`exercises/ex5_agent_tools_notes.md`

## 环境

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
cp .env.example .env   # 填入你的 key
```

没有 OpenAI key 的替代方案：

- **DeepSeek**：`OPENAI_BASE_URL=https://api.deepseek.com`，模型 `deepseek-chat`
- **本地 Ollama**：`OPENAI_BASE_URL=http://localhost:11434/v1`，模型如 `llama3.1`（需先 `ollama pull llama3.1`）
- **通义千问**：`OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1`，模型 `qwen-plus`

## 常见坑

- 版本：LangChain 0.3 的 API 与旧教程差异较大，装最新后以官方文档为准（本仓库按 0.3+ 写法）。
- API key 放 `.env`，**永远不要提交**（`.gitignore` 已处理）。
- 模型名写错是最常见的 401/404；`base_url` 结尾别丢 `/v1`。
- 中文检索：embedding 选支持中文的，如 `text-embedding-3-small` 或本地 `BAAI/bge-*`。

## 最终项目

做完五步练习，看 `final-project.md`：把 RAG 和 FastAPI 组合成“本地文档问答机器人”。
