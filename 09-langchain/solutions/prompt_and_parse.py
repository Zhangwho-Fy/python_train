"""第 2 步参考答案。"""
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()


class Movie(BaseModel):
    title: str = Field(description="电影名")
    year: int = Field(description="上映年份")
    director: str = Field(description="导演")


def main() -> None:
    parser = PydanticOutputParser(pydantic_object=Movie)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是电影百科。\n{format_instructions}"),
            ("human", "介绍电影《{name}》"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    model = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
    )
    chain = prompt | model | parser
    movie = chain.invoke({"name": "盗梦空间"})
    print(movie)


if __name__ == "__main__":
    main()
