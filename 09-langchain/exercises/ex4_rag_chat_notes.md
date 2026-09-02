# ex4 rag_chat 考点详解（第 4 步：RAG——最终项目的核心）

## 题目回顾

把本地 `docs/` 下的 markdown：加载 → 切块 → 向量化存 Chroma → 检索 top-k → 把资料拼进 prompt 让模型回答。这是最终“本地文档问答机器人”的心脏。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| RAG 全流程 | 检索增强生成：先找资料再回答 | 加载→切块→向量库→检索→拼 prompt |
| `DirectoryLoader` | 批量加载目录文件 | `glob="**/*.md"` + TextLoader |
| `RecursiveCharacterTextSplitter` | 按语义边界切块 | `chunk_size=500, chunk_overlap=50` |
| Embedding + Chroma | 文本变向量、按相似度存查 | `Chroma.from_documents` |
| `as_retriever(k=4)` | 检索器接口 | 拿 top-4 相关块 |
| `RunnablePassthrough` | 原样透传输入 | question 直通给 prompt |
| 上下文拼接 | 多块资料格式化进 system | `format_docs` |

## 1. RAG 在解决什么问题

模型不知道你的私有文档。RAG 的做法：**回答前先去文档里检索最相关的几段，把资料放进 prompt 一起给模型**。效果上像“开卷考试”，还能附上来源。

全流程（对应题目每一步）：

```text
docs/*.md → 加载 → 切块 → 向量库(Chroma) → 检索器 top-k
                                                  ↓
问题 → 检索相关块 → {context} 拼进 prompt → 模型 → 回答
```

## 2. 加载与切块

```python
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = DirectoryLoader("docs/", glob="**/*.md", loader_cls=TextLoader)
docs = loader.load()            # 每个文件一个 Document

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
```

- `TextLoader` 读单个文本文件；`DirectoryLoader` 加 `glob="**/*.md"` 递归取目录下所有 markdown。
- 为什么切块：整篇塞进 prompt 又贵又超长；检索也只需要“相关片段”。切块原则：块要**语义完整**，别把一句话从中间切断。
- `chunk_size=500`（字符）、`chunk_overlap=50`（相邻块重叠 50 字符，防止关键句刚好落在切缝上）。

## 3. 向量化与向量库

```python
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="./chroma_db",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
```

- Embedding 把“一段文本”变成“一个高维向量”，语义相近的文本向量距离近——这是检索的基础。
- Chroma 是本地向量数据库：存向量 + 原文，查询时按相似度返回最相关的块。
- `as_retriever(search_kwargs={"k": 4})` 得到检索器：调用 `retriever.invoke(问题)` 返回 4 个最相关的 Document（03 阶段 topk 的实战版）。
- 中文检索建议 embedding 用支持中文的模型：`text-embedding-3-small` 或本地 `BAAI/bge-*`。
- 没有 `docs/` 目录时先建一个放几篇 md，否则 loader 报错。

## 4. 把检索结果拼进 prompt

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def format_docs(documents) -> str:
    return "\n\n".join(doc.page_content for doc in documents)

prompt = ChatPromptTemplate.from_messages([
    ("system", "根据下面资料回答问题；资料里没有就直说不知道，不要编造。\n\n{context}"),
    ("human", "{question}"),
])

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

answer = chain.invoke("这个仓库的最终目标是什么？")
```

管道里这个 `{...}` 字典是 LCEL 的**并行分支**语法：

- `retriever | format_docs`：问题先进检索器拿 4 个 Document，`format_docs` 拼成一大段资料 → 填进 `{context}`；
- `RunnablePassthrough()`：把原始输入**原样透传** → 填进 `{question}`；
- 两个分支完成后合成一个字典喂给 prompt。

## 5. 为什么这一步是“最终项目核心”

`final-project.md` 的 M1 就是“命令行版 RAG 能回答 docs/ 里的问题”，后续里程碑只是把这个 `chain` 包进 FastAPI、加流式和对话历史。RAG 调通 = 大目标完成一半。

## 6. 易错点清单

1. **没建 `docs/` 目录**：DirectoryLoader 找不到路径直接报错。
2. **chunk_size 太小**：切得稀碎，语义断裂；500 起步，长文档试 1000。
3. **忘了 embedding 模型对中文的支持**：英文模型检索中文，相关块经常召回不准。
4. **prompt 里没有明确“资料里没有就说不知道”**：模型会拿无关上下文硬编。
5. **每次运行重建向量库**：生产场景应该先建库存盘，启动只加载（`Chroma(persist_directory=...)`），最终项目验收清单里就有“重启后还能用”。
6. **`format_docs` 拼的 context 太长**：4 块 × 500 字符对多数模型没问题；k 调大时注意 token 预算。

## 7. 变式练习

- 检索结果里带上 `metadata`（来源文件名），回答后打印来源——最终项目加分项。
- 调 `chunk_overlap` 和 `k`，观察同样问题回答质量的变化。
- 在 system 里要求“如果资料不足，回复：文档中没有相关内容”，验收“不瞎编”的里程碑。
