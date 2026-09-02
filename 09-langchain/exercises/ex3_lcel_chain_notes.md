# ex3 lcel_chain 考点详解（第 3 步：用 `|` 串两条链）

## 题目回顾

做“中文 → 英文 → 再总结成一句中文”的两步链：translate prompt → model → `StrOutputParser` → summarize prompt → model → `StrOutputParser`，体会 `|` 管道和变量流转。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| LCEL `|` | 前一个组件输出自动成为下一个的输入 | 串 prompt/model/parser |
| `StrOutputParser` | 把 AIMessage 剥成纯字符串 | 字符串才能喂给下一个 prompt |
| 多段链 | 中段的输出当后段模板的 `{text}` | 中文 → 英文 → 中文总结 |
| `chain.invoke(...)` | 从最左端输入变量 | 只需给第一个 prompt 的变量 |
| Runnable 协议 | 组件都实现 invoke/stream/batch | 同一条链可同步可流式 |

## 1. 为什么中段要接 `StrOutputParser()`

`model` 的输出类型是 `AIMessage` 对象，不是字符串。下一个 `summarize_prompt` 期待“有一个 `{text}` 变量可以填充的字典/消息”：

- 管道里如果直接把 AIMessage 丢给 prompt，变量取不到 → 报错或乱填。
- `StrOutputParser()` 把 AIMessage 变成纯字符串，字符串再作为 `{text}` 注入下一个 prompt——这就是两步链的“接线”。

## 2. 参考实现

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))

translate_prompt = ChatPromptTemplate.from_messages([
    ("system", "把用户的话翻译成英文，只输出译文。"),
    ("human", "{text}"),
])

summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", "用一句简洁的中文总结下面的英文。"),
    ("human", "{text}"),
])

chain = (
    translate_prompt
    | model
    | StrOutputParser()
    | summarize_prompt
    | model
    | StrOutputParser()
)

result = chain.invoke({"text": "我今天写了一个快排，感觉 Python 很顺手。"})
print(result)   # 比如：作者认为用 Python 实现快速排序的体验很流畅。
```

数据流（对着代码走一遍）：

1. `chain.invoke({"text": 中文句子})` 填进 translate_prompt；
2. model 返回“I wrote a quicksort today...”的 AIMessage；
3. `StrOutputParser` 剥出字符串；
4. 字符串自动变成 summarize_prompt 的 `{text}`；
5. 第二个 model 返回一句中文；
6. 最后的 `StrOutputParser` 剥出最终字符串。

## 3. 管道 = 责任链/管道模式

LCEL `|` 和你熟悉的管道设计一模一样：每个组件实现 Runnable 协议（invoke/stream/batch），所以：

- 链可以 `chain.stream(...)` 流式输出（08 阶段 StreamingResponse 就用它）；
- 链可以被别的链嵌套（`chain2 = prompt | chain | parser`）；
- 链是 lazy 组合的：定义时不做任何模型调用，invoke 时才真正执行。

## 4. 易错点清单

1. **中段漏 `StrOutputParser()`**：AIMessage 没法当下一个 prompt 的 `{text}`。
2. **两个 prompt 的变量名不一致**：第一个用 `{text}` 第二个用 `{sentence}`，而管道只透传值不自动改名——中段必须显式接一个能注入的组件或变量对齐。
3. **`invoke` 只给第一个 prompt 的变量**：中间的 prompt 变量必须由上游输出填，别指望 invoke 里再传。
4. **把 `chain.invoke` 的结果再当链**：结果是字符串；要再处理就包一层 RunnableLambda。
5. **忘了 API 配置**：model 建不出来/401，先回 ex1 检查 .env。

## 5. 变式练习

- 在链尾加第三个 prompt：把总结再翻译成英文，验证任意段数都能串。
- 用 `chain.stream(...)` 打印逐字输出，感受流式（09 最终项目要用）。
- 插入 `RunnableLambda(print)` 观察每段输出，理解“管道里流的是什么类型”。
