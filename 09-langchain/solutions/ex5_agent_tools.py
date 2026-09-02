"""第 5 步参考答案。"""
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()


@tool
def get_current_time() -> str:
    """返回当前日期时间字符串。"""
    return datetime.now().isoformat()


@tool
def search_files(keyword: str, directory: str = ".") -> str:
    """在 directory 下递归搜索文件名包含 keyword 的文件。"""
    hits = [
        str(p)
        for p in Path(directory).rglob("*")
        if p.is_file() and keyword in p.name
    ]
    return "\n".join(hits) if hits else "没有找到"


def main() -> None:
    tools = [get_current_time, search_files]
    model = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是助手，可以调用工具来回答问题。"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    agent = create_tool_calling_agent(model, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    executor.invoke(
        {"input": "现在几点？然后找名字里带 README 的文件"}
    )


if __name__ == "__main__":
    main()
