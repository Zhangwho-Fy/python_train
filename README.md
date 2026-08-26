# Python 练习仓库：从 C++ 到 LangChain

这是一个为“C++ 熟练、Python 零基础”的你准备的渐进式练习仓库。
不用从头啃语法书：每个阶段先讲“Python 里这个东西对应 C++ 的什么”，
再给你一组能直接跑起来的小练习，边写边内化。

## 学习路线

| 阶段 | 目录 | 主题 | 对应你的 C++ 底子 | 练完能做什么 |
| --- | --- | --- | --- | --- |
| 0 | `00-setup` | 环境与工具 | - | 跑通第一个脚本 |
| 1 | `01-basics` | 变量、容器、控制流 | `vector` / `map` / 循环 | 5 个小程序 |
| 2 | `02-functions-modules` | 函数、lambda、模块 | 函数、模板、命名空间 | 自己的工具库 |
| 3 | `03-data-structures-algorithms` | 快排、栈、队列、堆 | 算法功底 | 熟练用 Python 写算法 |
| 4 | `04-file-io` | 文件、JSON、异常 | `fstream` / nlohmann/json | 数据处理脚本 |
| 5 | `05-oop` | 类、dataclass、pydantic | C++ 类与运算符重载 | 模型类设计 |
| 6 | `06-advanced` | 装饰器、生成器、上下文 | RAII / 模板 / 惰性求值 | 写出地道 Python |
| 7 | `07-web-scraping` | requests、HTML 解析 | libcurl / 字符串处理 | 能写爬虫 |
| 8 | `08-async-fastapi` | async/await、FastAPI | C++20 coroutine | 能写 API 服务 |
| 9 | `09-langchain` | LCEL、RAG、Agent | 架构与系统设计 | **最终目标：RAG 问答应用** |

## 怎么用

1. 先看 `00-setup/README.md` 把环境装好（建议直接装 Python 3.10+，别用系统自带的 3.8 走到后面）。
2. 每个阶段：**先读该阶段 README 的知识点**（都是 C++ 对照视角），再打开 `exercises/` 里的题目。
3. 题目文件里有 TODO 和测试样例，写完直接 `python3 exercises/xxx.py` 跑。
4. 卡住 30 分钟再看 `solutions/`；对照完把两版都想想“差异在哪”。
5. 语法想不起来时，打开 `tutorial/python-for-cpp.html`，它是按章节组织的 C++/Python 对照教程。

## 三个约定

- 每题都尽量写成**一行命令可验证**：脚本里带 `if __name__ == "__main__":` 和简单断言。
- 前 6 个阶段零第三方依赖（05 的 pydantic 除外），后面按阶段 `requirements.txt` 装。
- 遇到不懂的语法，先用 `python3 -i` 交互式随便试，再查文档。

## 进度打卡

- [ ] 00 环境跑通
- [ ] 01 语法基础 5 题
- [ ] 02 函数与模块 4 题
- [ ] 03 数据结构与算法 5 题
- [ ] 04 文件与异常 4 题
- [ ] 05 面向对象 4 题
- [ ] 06 进阶特性 5 题
- [ ] 07 爬虫 4 题
- [ ] 08 异步与 FastAPI 3 题
- [ ] 09 LangChain 5 步 + 最终项目

## 关于最终目标 LangChain

LangChain 不是“Python 语法”的延续，它更接近一个**框架**：需要你熟悉类、
pydantic、装饰器/生成器、JSON、网络请求和 async——这正是 01~08 阶段铺的底子。
到了 09 你会看到，真正难的不是 LangChain API，而是：

- 把 prompt / 模型 / 解析器串成一条链（LCEL）
- 把本地文档切碎、向量化、检索回来（RAG）
- 让模型学会调用你写的工具（Agent）

仓库里每个阶段的 README 都标注了“与 LangChain 的关系”，帮助你带着目的学。
