# ex2 prompt_and_parse 考点详解（第 2 步：让模型输出结构化 JSON）

## 题目回顾

定义 `Movie(title, year, director)` pydantic 模型 → 用 `PydanticOutputParser` 生成格式要求 → `ChatPromptTemplate` 拼 prompt → `prompt | model | parser` 组成链，`invoke({"name": "盗梦空间"})` 后直接得到 Movie 对象。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `PydanticOutputParser` | 把模型文本解析+校验成 pydantic 对象 | 输出不再靠手撕字符串 |
| `get_format_instructions()` | 自动生成“请输出这种 JSON”的说明 | 拼进 system prompt |
| `ChatPromptTemplate` | 模板 + 变量注入 | `{name}` 替换成电影名 |
| `.partial(...)` | 预先固定部分变量 | format_instructions 不变 |
| LCEL `|` | 前一个的输出是后一个的输入 | prompt → model → parser |
| `chain.invoke({...})` | 传参跑整条链 | 输入模板变量 |

## 1. 问题背景：模型输出是“字符串”

让模型返回结构化数据时，直接 `content` 拿到的是 JSON 文本甚至带解释的文字。手工 `json.loads` 会踩：模型偶尔多写一句、键名不一致、类型不对。pydantic 解析器一次性解决“解析 + 校验”。

## 2. 参考实现

```python
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str
    year: int
    director: str

model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "根据用户给的电影名输出 JSON，字段要严格符合：\n{format_instructions}",
    ),
    ("human", "{name}"),
]).partial(format_instructions=parser.get_format_instructions())

chain = prompt | model | parser
movie = chain.invoke({"name": "盗梦空间"})
print(movie.title, movie.year, movie.director)   # 是 Movie 对象，不是字符串
```

三个关键机制：

1. **`parser.get_format_instructions()`** 自动生成一段“请输出这种格式”的说明（含字段、类型、示例 JSON），`.partial()` 把它预先填进模板——它和 `{name}` 不同，调用时不变。
2. **LCEL 管道**：`prompt | model | parser`。prompt 的输出（消息）喂给 model，model 的输出（字符串）喂给 parser，parser 返回 `Movie` 实例。若模型输出不合 schema，parser 抛 `OutputParserException`，错误信息会告诉你哪里不符。
3. **`chain.invoke({"name": ...})`** 只需提供模板里剩下的变量。

## 3. pydantic 在这里的角色

- 字段声明 = 输出契约：`year: int` 表示模型得给整数，给出 `"2010"` 也会被转成 int。
- 05 阶段练的 `Field(ge=..., le=...)` 等约束直接可用于校验模型输出。
- LangChain 内部还会把 pydantic 模型转成 JSON Schema 放进 format instructions——所以“模型长什么样 = pydantic 类长什么样”。

## 4. 易错点清单

1. **忘了 `.partial(format_instructions=...)`**：模板里 `{format_instructions}` 没值，invoke 报缺参。
2. **`pydantic_object` 忘了传**：`PydanticOutputParser()` 没有默认对象会报错。
3. **解析失败就加 try 重试**：模型偶尔输出不合法 JSON，生产代码通常捕 `OutputParserException` 再问一次或降级。
4. **要求输出 JSON 但没给示例**：光说“输出 JSON”模型可能自由发挥；`get_format_instructions()` 给的示例字段名是关键。
5. **模型不支持 function calling/JSON mode**：靠提示词解析对部分模型不稳定，必要时用 `model.with_structured_output(Movie)`（新版更稳的替代）。

## 5. 变式练习

- 把 Movie 换成你自己的 RAG 答案模型：`Answer(answer: str, sources: list[str])`。
- 故意让模型输出非法 JSON，观察 `OutputParserException` 的内容。
- 对比 `parser.get_format_instructions()` 生成的文本和你手写的提示词，理解“schema → 提示词”的转换。
