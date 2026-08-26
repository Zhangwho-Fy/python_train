"""第 3 步：LCEL 两步链：翻译成英文，再总结成一句中文。"""


# TODO: translate prompt：system "把用户的话翻译成英文，只输出译文" + human {text}
# TODO: summarize prompt：system "用一句中文总结下面的英文" + human {text}
# TODO: chain = translate | model | StrOutputParser() | summarize | model | StrOutputParser()
# TODO: invoke({"text": "我今天写了一个快排，感觉 Python 很顺手。"})
