"""第 1 步：不装 LangChain，直接用 OpenAI SDK 聊天。"""


def chat_once(question: str) -> str:
    # TODO: 读 .env（python-dotenv 的 load_dotenv）
    # TODO: OpenAI(api_key=..., base_url=...) 建客户端
    # TODO: chat.completions.create(messages=[system, user], temperature=0.7)
    # TODO: 返回 choices[0].message.content
    return ""


def main() -> None:
    answer = chat_once("用一句话解释什么是 RAG")
    print(answer)


if __name__ == "__main__":
    main()
