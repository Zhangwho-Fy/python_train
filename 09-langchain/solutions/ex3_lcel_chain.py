"""第 3 步参考答案。"""
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


def main() -> None:
    model = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.3,
    )

    translate = ChatPromptTemplate.from_messages(
        [
            ("system", "你是翻译官，把用户的话翻译成英文，只输出译文。"),
            ("human", "{text}"),
        ]
    )
    summarize = ChatPromptTemplate.from_messages(
        [
            ("system", "用一句中文总结下面的英文。"),
            ("human", "{text}"),
        ]
    )

    chain = (
        translate
        | model
        | StrOutputParser()
        | summarize
        | model
        | StrOutputParser()
    )
    result = chain.invoke({"text": "我今天写了一个快排，感觉 Python 很顺手。"})
    print(result)


if __name__ == "__main__":
    main()
