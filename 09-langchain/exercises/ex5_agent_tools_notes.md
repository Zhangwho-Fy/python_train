# ex5 agent_tools 考点详解（第 5 步：让 Agent 自己决定调工具）

## 题目回顾

定义 `get_current_time`、`search_files` 两个 `@tool` 函数，用 `create_tool_calling_agent` 组装 Agent + `AgentExecutor` 运行，观察模型自己选择调哪个工具。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `@tool` | 把函数注册成模型可调用的工具 | 签名 + docstring 就是工具说明书 |
| 工具模式 | 模型输出“工具调用”请求，框架执行再回填 | get_current_time / search_files |
| `create_tool_calling_agent` | 组装“模型 + 工具 + prompt” | 需要一个 placeholder 装执行历史 |
| `AgentExecutor` | 循环执行：模型选工具→跑→再问，直到结束 | `invoke({"input": ...})` |
| `AgentExecutor` 的 `verbose=True` | 打印决策过程 | 观察模型怎么想 |

## 1. 工具函数 = 模型的手脚

```python
from datetime import datetime
from pathlib import Path
from langchain_core.tools import tool

@tool
def get_current_time() -> str:
    """返回当前日期和时间（ISO 格式）。"""
    return datetime.now().isoformat()

@tool
def search_files(keyword: str, directory: str = ".") -> str:
    """在指定目录下递归搜索文件名包含 keyword 的文件，返回路径列表。"""
    hits = [str(p) for p in Path(directory).rglob("*") if keyword in p.name]
    return "\n".join(hits) if hits else "没有找到匹配文件"
```

- `@tool` 会读取**函数签名**（参数名、类型、默认值）和 **docstring** 生成工具 schema，发给模型。所以 docstring 必须写清楚“这个工具干什么、参数什么意思”——模型靠它决定何时调用。
- 函数本身还是普通 Python 函数：模型不直接执行代码，而是**输出一个“调用 search_files(keyword='python')”的请求**，由框架在本地执行，再把结果作为新消息喂回模型。
- 对应工程概念：插件/RPC 注册表——把能力登记成“名字 + 参数说明 + 执行函数”。

## 2. 组装 Agent

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
tools = [get_current_time, search_files]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个能调用工具的助手，工具能回答的就用工具。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(model, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

必懂的两个结构：

- `{agent_scratchpad}` 是**必须**的 placeholder：Agent 循环中“已经调用过哪些工具、得到什么结果”的历史消息填在这里。没有它，模型记不住自己上一步干了啥。
- `create_tool_calling_agent` 只负责“决策一次”：输入 → 模型决定调工具或直接回答。`AgentExecutor` 负责**循环**：模型要调工具 → 执行 → 结果回填 → 再问模型 → ……直到模型给出最终回答或达到上限。

## 3. 运行与观察

```python
result = executor.invoke({
    "input": "现在几点？另外帮我找一下仓库里文件名包含 python 的文件。"
})
print(result["output"])
```

`verbose=True` 时你会看到完整决策轨迹：模型先调 `get_current_time` → 拿到时间 → 再调 `search_files` → 拿到文件列表 → 组织成最终回答。这就是“Agent 决策循环”的可视化。

## 4. 易错点清单

1. **docstring 写得太随意**：模型根据 docstring 判断何时调用，写“返回时间”和写“处理用户查询”效果天差地别。
2. **参数类型/默认值乱写**：schema 错，模型不会传参或调用 422。
3. **prompt 少了 `{agent_scratchpad}` placeholder**：create_tool_calling_agent 直接报错或循环异常。
4. **`AgentExecutor` 忘传 tools**：工具不在执行器里，模型调了也执行不了。
5. **工具没网/路径不存在也不处理**：工具函数要有兜底返回值（如“没有找到”），别抛裸异常让循环崩。
6. **用不支持 function calling 的模型**：`create_tool_calling_agent` 需要模型原生支持工具调用；本地小模型可能要换 ReAct 风格 agent。

## 5. 变式练习

- 加第三个工具 `read_file(path)`，让 Agent 能完成“搜索 → 读内容 → 总结”。
- 用 `@tool` 的参数注解 + `Field(description=...)` 精细描述参数。
- 给 Agent 加“最多 5 步”限制（`max_iterations`），防死循环烧 token。

## 6. 五步完成后的下一步

五步分别对应：直接调 LLM（ex1）、结构化输出（ex2）、链式管道（ex3）、文档检索（ex4）、工具调用（ex5）。打开 `final-project.md` 把它们合成最终项目：FastAPI + RAG 链 + StreamingResponse + 对话历史。
