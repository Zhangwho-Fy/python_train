# ex1 word_count 考点详解

## 题目回顾

读 `exercises/sample.txt`，统计词频：小写化、去标点，用 `collections.Counter` 输出 Top 10。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `with open(path, encoding="utf-8") as f` | RAII 式自动关文件 | 读文件 |
| `f.read()` | 把整个文件读成字符串 | 小文件直接读 |
| 正则 `re.findall` | 按模式摘出所有单词 | `[a-zA-Z']+` 去标点 |
| `str.lower()` | 统一小写 | 大小写归一 |
| `collections.Counter` | 一行做词频统计 | `Counter(words)` |
| `Counter.most_common(10)` | 返回 Top-N 的 `(词, 次数)` 列表 | 输出榜单 |

## 1. 读文件：`with` 语句

```python
with open("exercises/sample.txt", encoding="utf-8") as f:
    text = f.read()
```

- `with ... as f:` 离开缩进块时自动 `f.close()`——和 C++ RAII/析构等价，忘写 `close()` 也不会泄漏句柄。
- **显式传 `encoding="utf-8"`**：否则在 Windows 上可能按系统编码读，中文乱码或报错。
- `f.read()` 一次读完整文件；文件很大时不行（ex4 教逐行方案）。
- 路径是相对“当前工作目录”的：从 `04-file-io/` 目录运行 `python3 exercises/ex1_word_count.py`，文件参数就写 `exercises/sample.txt`。用 `pathlib.Path(__file__).parent` 可以做到“无论从哪运行都对”，06 ex5 会展示。

## 2. 去标点：正则 `re.findall`

```python
import re

words = re.findall(r"[a-zA-Z']+", text.lower())
```

- `text.lower()` 先统一小写：`The` 和 `the` 才能合并统计。
- 模式 `[a-zA-Z']+` 意思是“连续的大小写字母和撇号”，`"dog."` 会摘出 `dog`（点号不是字母，天然被跳过），`"don't"` 会保留成 `don't`。
- `re.findall` 返回所有匹配的列表——这是处理“只留单词”最省事的办法。不想学正则也行：`str.split()` 只能按空白拆，`"dog."` 会带着点号。

## 3. Counter 词频统计

```python
from collections import Counter

def count_words(path: str) -> list:
    with open(path, encoding="utf-8") as f:
        text = f.read()
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return Counter(words).most_common(10)
```

- `Counter(words)` 是 dict 的子类，统计每个词出现次数；相当于 01 阶段 ex4 里手写的“dict + get 计数”，但更快更短。
- `most_common(10)` 返回 `[(词, 次数), ...]`，已按次数降序——正是榜单格式。
- 调用处 `for word, count in count_words(...)` 直接解包打印：

```python
for word, count in count_words("exercises/sample.txt"):
    print(f"{word}: {count}")
```

## 4. 易错点清单

1. **忘写 `encoding="utf-8"`**：跨平台读中文/特殊字符容易崩。
2. **忘了 `lower()`**：`Python` 和 `python` 被当成两个词。
3. **`Counter` 没 `import`**：`NameError`。
4. **从错误目录运行导致路径错**：报 `FileNotFoundError` 时先确认 cwd；不确定就用 `Path(__file__).parent` 拼路径。
5. **`most_common()` 忘给参数**：默认返回全部词频，不是 Top 10。

## 5. 变式练习

- 不用正则，改用 `str.translate` + `string.punctuation` 清标点。
- 改读多行大文件（for line in f 逐行处理，Counter.update），为 ex4 预热。
- 输出到 `top_words.txt`：`with open(..., "w", encoding="utf-8") as out:` 写结果。
