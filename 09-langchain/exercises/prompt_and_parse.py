"""第 2 步：PromptTemplate + PydanticOutputParser 结构化输出。"""


# TODO: 定义 Movie(title, year, director) pydantic 模型
# TODO: PydanticOutputParser(pydantic_object=Movie)
# TODO: ChatPromptTemplate.from_messages([...]).partial(format_instructions=...)
# TODO: prompt | model | parser 组成 chain，invoke({"name": "盗梦空间"})
