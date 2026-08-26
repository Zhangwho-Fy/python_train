"""第 1 步参考答案。"""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def chat_once(question: str) -> str:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": "你是简洁的中文助手。"},
            {"role": "user", "content": question},
        ],
        temperature=0.7,
    )
    return resp.choices[0].message.content


def main() -> None:
    answer = chat_once("用一句话解释什么是 RAG")
    print(answer)


if __name__ == "__main__":
    main()
