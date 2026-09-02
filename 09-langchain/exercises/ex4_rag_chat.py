"""第 4 步：RAG：本地文档 → 切块 → 向量库 → 检索 → 回答。"""


# TODO: DirectoryLoader 加载 docs/ 下的 .md（TextLoader）
# TODO: RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# TODO: Chroma.from_documents(chunks, embeddings, persist_directory=...)
# TODO: retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
# TODO: prompt: system 里给 {context}，human 里放 {question}
# TODO: chain = {"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | model | parser
