# 04 文件、JSON 与异常

## 本阶段目标

读写文本/JSON 文件，处理异常，写出不崩的脚本。

## C++ 对照

| Python | C++ 类似物 |
| --- | --- |
| `with open(p) as f:` | `std::ifstream`（RAII） |
| `f.read()` / `f.readlines()` / `for line in f` | `istreambuf_iterator` / `getline` |
| `json.load` / `json.dump` | `nlohmann::json` |
| `pathlib.Path` | `std::filesystem::path` |
| `try / except / finally` | `try / catch`（C++ 无 finally） |
| `raise ValueError("...")` | `throw std::runtime_error("...")` |
| `logging` 模块 | spdlog / glog |

## 要点

- **`with` 自动关闭**：`with open("a.txt", encoding="utf-8") as f:`，离开缩进块自动 close——和 RAII 一样。
- **读写都显式传 `encoding="utf-8"`**：Windows 默认编码不同，不传会踩坑。
- **`json.dump` 写中文记得 `ensure_ascii=False`**，否则全变 `\uXXXX`。
- **异常先抓具体类型**：`except FileNotFoundError` 而不是裸 `except:`——裸 except 吞掉一切，Debug 噩梦。
- **`for line in f` 逐行迭代**：处理大文件别 `f.read()` 全读进内存。

## 与 LangChain 的关系

RAG 的第一步就是“加载文档”：`Path.read_text()`、`json`、`csv` 处理文档是日常；
`logging` 以后调试 API 调用必备。

## 练习题

每题在 `exercises/` 里有配套考点详解（`exN_xxx_notes.md`），卡住先翻详解再翻答案。

### ex1 word_count

考点详解：`exercises/ex1_word_count_notes.md`

读 `exercises/sample.txt`，统计词频（小写、去标点），输出 Top 10。
标准库答案：`collections.Counter` + `re.findall(r"[a-zA-Z']+", text.lower())`。

### ex2 json_clean

考点详解：`exercises/ex2_json_clean_notes.md`

读 `exercises/students.json`，过滤出 `score >= 80` 的学生，按分数降序，写 `cleaned.json`（中文不转义）。

### ex3 logger

考点详解：`exercises/ex3_logger_notes.md`

先手写 `log(level, message)`：打印 `[2026-08-26 12:00:00] [INFO] 消息` 并追加写入 `app.log`；
再用标准库 `logging` 配一个同样格式的 logger，对比两种写法的取舍。

### ex4 big_file

考点详解：`exercises/ex4_big_file_notes.md`

不把整个文件读进内存，逐行统计 `sample.txt` 的行长度分布（分桶 0-9 / 10-19 / 20-29 / ...），打印各桶行数。
提示：用生成器 `def lines(path): for line in open(path): yield line`（yield 下个阶段细讲，先用起来）。

## 期望输出示例

- ex1：`the: 5` 之类的词频榜
- ex2：`cleaned.json` 里是分数 ≥ 80 且降序的数组
- ex3：终端和 `app.log` 里格式一致
- ex4：打印桶分布，如 `0-9: 2 行, 10-19: 5 行, ...`
