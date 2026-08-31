# ex4 word_frequency 考点详解

## 题目回顾

给一句话，统计每个词出现的次数，按次数**降序**打印前 `top` 个（默认 5）。

```python
def word_frequency(text: str, top: int = 5) -> list:
    # TODO: 小写化、split() 拆词、dict 计数、按次数降序取前 top
    return []
```

一句话流程：`text.lower().split()` 拆词 → `dict` 计数 → `sorted(..., key=..., reverse=True)` 排序 → `ranked[:top]` 截断。

---

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `str.lower()` | 字符串全部转小写 | `text.lower()` |
| `str.split()` | 按空白拆成单词列表 | `text.lower().split()` |
| `dict` 计数 | 用字典统计出现次数 | `counts[word] = counts.get(word, 0) + 1` |
| `dict.get(key, 默认值)` | 键不存在时返回默认值，不报错 | `counts.get(word, 0)` |
| `dict.items()` | 同时拿到键和值 | `sorted(counts.items(), ...)` |
| 元组解包 | 把 `(键, 值)` 拆成两个变量 | `for word, count in ranked:` |
| `sorted()` + `key` | 自定义排序规则 | `key=lambda item: item[1]` |
| lambda 匿名函数 | 写一个临时小函数 | `lambda item: item[1]` |
| `reverse=True` | 降序排列 | `sorted(..., reverse=True)` |
| 切片 | 取前 N 个元素 | `ranked[:top]` |
| 函数默认参数 | 不传参时用默认值 | `top: int = 5` |
| 类型注解 | 标注参数/返回值类型（不强制） | `text: str -> list` |
| f-string | 把变量格式化进字符串 | `f"{word}: {count}"` |
| `if __name__ == "__main__":` | 只在直接运行脚本时执行 | 主入口惯用法 |

---

## 1. 字符串处理：`lower()` 和 `split()`

### `str.lower()`：转小写

把字符串里所有大写字母转成小写，返回**新字符串**，原字符串不变（字符串本身不可变）。

```python
s = "The Quick Fox"
print(s.lower())   # "the quick fox"
print(s)           # "The Quick Fox"，原字符串没变
```

为什么要做：如果不转小写，`"The"` 和 `"the"` 会被当成两个不同的词，统计就错了。

同类方法：`upper()`（转大写）、`title()`（每个词首字母大写）、`strip()`（去首尾空白）。

### `str.split()`：拆词

默认**按任意空白字符**（空格、`\t`、换行）拆，返回字符串列表。连续空白会自动合并，首尾空白会被忽略。

```python
print("the quick fox".split())        # ['the', 'quick', 'fox']
print("a  b   c".split())             # ['a', 'b', 'c']，多个空格也只算一个分隔
print("  hello  ".split())            # ['hello']，首尾空白被忽略
print("3 + 5".split("+"))             # ['3 ', ' 5']，指定分隔符
print("".split())                     # []，空字符串
```

链式调用：`text.lower().split()` 先转小写、再拆词，一步到位。

---

## 2. 字典计数：`dict` + `.get()`

### dict 基础

`dict`（字典）存的是 `键: 值` 对，键必须可哈希（字符串、数字、元组都可以），类比 C++ 的 `std::map<std::string, int>` 或 `unordered_map`。

```python
d = {}                        # 空字典
d["the"] = 1                  # 新增/覆盖：d["the"] = 2 就是修改
print(d["the"])               # 1，读取
print("the" in d)             # True，判断键是否存在
print(len(d))                 # 1，键值对数量
```

### 经典计数模式

```python
counts = {}
for word in text.lower().split():
    counts[word] = counts.get(word, 0) + 1
```

逐行理解：

1. `counts.get(word, 0)`：如果 `word` 还没出现过，返回默认值 `0`；出现过就返回当前次数。
2. `+ 1`：次数加一。
3. `counts[word] = ...`：把新次数写回字典。

第一次遇到 `"the"`：`get("the", 0)` 返回 0 → 存成 1。
第二次遇到 `"the"`：`get("the", 0)` 返回 1 → 存成 2。

### 为什么不直接 `counts[word] += 1`

键不存在时，`counts[word]` 会直接抛 `KeyError`，所以必须先判断或给默认值。

```python
# 方式一（最简洁）：get + 默认值
counts[word] = counts.get(word, 0) + 1

# 方式二：in 判断（可读性好）
if word in counts:
    counts[word] += 1
else:
    counts[word] = 1

# 方式三：setdefault（不太常用但要知道）
counts.setdefault(word, 0)
counts[word] += 1
```

`.get()` 还有只读的用法：查配置、查表时给个兜底值，避免 KeyError。

```python
config = {"retry": 3}
print(config.get("timeout"))      # None，没传默认值返回 None
print(config.get("timeout", 30))  # 30，键不存在用默认值
```

---

## 3. 遍历字典：`.keys()` / `.values()` / `.items()`

```python
d = {"the": 3, "fox": 1}

for k in d:                       # 遍历键
    print(k)

for k in d.keys():                # 同上，更明确
    print(k)

for v in d.values():              # 只遍历值
    print(v)

for k, v in d.items():            # 键和值一起遍历（本题用法）
    print(k, v)

for item in d.items():            # 不拆包时，item 是 (键, 值) 元组
    print(item[0], item[1])       # ('the', 3) -> the 3
```

`items()` 返回的是 `(键, 值)` 元组视图，所以后面排序时 `item[0]` 是词、`item[1]` 是次数。

---

## 4. 排序：`sorted()`、`key`、lambda、`reverse`

### `sorted()` 基础

`sorted(可迭代对象)` 返回**排序后的新列表**，不改动原数据。默认升序，元素是元组时先比第一个元素、相等再比第二个。

```python
print(sorted([3, 1, 2]))            # [1, 2, 3]
print(sorted([(1, 9), (1, 2)]))     # [(1, 2), (1, 9)]，先比 1 再比第二个数
```

### `key` 参数：按什么排

`key` 接收一个"从元素里取出排序依据"的函数，`sorted` 用这个依据比较。

```python
counts = {"the": 3, "fox": 1, "dog": 1}
items = list(counts.items())        # [('the', 3), ('fox', 1), ('dog', 1)]

# 按次数（item[1]）升序
sorted(items, key=lambda item: item[1])
# [('fox', 1), ('dog', 1), ('the', 3)]

# 按次数降序：reverse=True
sorted(items, key=lambda item: item[1], reverse=True)
# [('the', 3), ('fox', 1), ('dog', 1)]
```

### 不加 `key` 会怎样

直接 `sorted(counts)` 只按**键**排序，因为遍历字典默认拿到的是键；直接 `sorted(counts.items())` 按"词 → 次数"排序，次数只是次要依据——都不对。

```python
sorted(counts)          # ['dog', 'fox', 'the']，按词字母排，不是我们要的
sorted(counts.items())  # [('dog', 1), ('fox', 1), ('the', 3)]，次数相同先比词
```

### lambda：匿名小函数

`lambda item: item[1]` 等价于：

```python
def get_count(item):
    return item[1]

sorted(items, key=get_count, reverse=True)
```

lambda 适合一行能写完的小逻辑；逻辑复杂就命名函数，可读性更好。

### 进阶：多级排序

次数降序、次数相同的按词字母升序（用 `-` 取反次数，实现第一关键字降序）：

```python
sorted(items, key=lambda item: (-item[1], item[0]))
# [('the', 3), ('dog', 1), ('fox', 1)]
```

`sorted` 是**稳定排序**：`key` 相等时保持原相对顺序。本题中并列的词保持字典插入顺序（也就是首次出现顺序）。

---

## 5. 切片：`[:top]` 取前 N 个

```python
ranked = [("the", 3), ("fox", 1), ("dog", 1)]

print(ranked[:2])     # [('the', 3), ('fox', 1)]，前 2 个
print(ranked[:1])     # [('the', 3)]
print(ranked[:99])    # 超出长度不报错，返回全部
print(ranked[1:3])    # [('fox', 1), ('dog', 1)]，下标 1~2
print(ranked[::-1])   # 反转
```

注意 `[:top]` 是**半开区间**，`top=0` 返回空列表；`[:-1]` 是"去掉最后一个"，不是"前 -1 个"。

---

## 6. 元组解包

```python
a, b = ("the", 3)     # a = "the"，b = 3
first, second = [1, 2]
word, count = ranked[0]
```

配合 `for` 循环使用，比 `item[0]` / `item[1]` 清晰得多：

```python
for word, count in ranked:
    print(f"{word}: {count}")
```

---

## 7. 函数：默认参数、类型注解、返回值

```python
def word_frequency(text: str, top: int = 5) -> list:
    ...
```

- `top: int = 5`：**默认参数**，调用时不传就取 5。`word_frequency(text, 3)` 传 3 覆盖。
- `text: str` / `-> list`：**类型注解**，只是给人（和 IDE）看的提示，Python 不强制校验，传别的类型也不会报错。
- 返回值：本题返回"排序后截断"的 `[(词, 次数), ...]` 列表，外层再 `for word, count in ...` 消费。

```python
word_frequency("a a b")      # 用默认 top=5
word_frequency("a a b", 1)   # 只取前 1
```

注意：默认参数写在必填参数后面，`def f(a, b=1)` 合法，`def f(a=1, b)` 会语法报错。

---

## 8. f-string 格式化输出

```python
word, count = "the", 3
print(f"{word}: {count}")      # the: 3
print(f"{word:<10}{count:>3}") # the        3，左对齐/右对齐
print(f"{count:.2f}")          # 3.00，数字格式化
```

花括号里可以直接写表达式：`f"{len(words)} 个词"`。

---

## 9. `if __name__ == "__main__":`

直接运行脚本时，Python 会把模块的 `__name__` 设成 `"__main__"`；被别的文件 `import` 时，`__name__` 是模块名。

```python
# a.py
def main():
    print("run")

if __name__ == "__main__":
    main()
```

```python
# b.py
import a          # 不会打印 "run"，因为 a 的 __name__ 是 "a"
```

好处：把可复用的函数写在 import 时不执行的保护里，测试和复用都方便。

---

## 10. 完整参考实现与运行结果

```python
def word_frequency(text: str, top: int = 5) -> list:
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return ranked[:top]


def main() -> None:
    text = "the quick brown fox jumps over the lazy dog the"
    for word, count in word_frequency(text):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
```

运行结果（`the` 出现 3 次：开头 1 次 + "over the" 1 次 + 结尾 1 次；README 里写 2 次是笔误）：

```text
the: 3
quick: 1
brown: 1
fox: 1
jumps: 1
```

---

## 11. 进阶拓展

### `collections.Counter`：一行完成计数 + 取 top

```python
from collections import Counter

text = "the quick brown fox jumps over the lazy dog the"
counts = Counter(text.lower().split())
print(counts.most_common(5))
# [('the', 3), ('quick', 1), ('brown', 1), ('fox', 1), ('jumps', 1)]
```

`Counter` 本身就是 `dict` 的子类，支持 `counts["the"]`、`+` 合并等，做词频是标准工具。

### 忽略标点

`split()` 只按空白拆，`"hello,"` 会带逗号。简单做法：把非字母字符替换掉。

```python
import re

words = re.findall(r"[a-z']+", text.lower())   # 只保留小写字母和撇号
```

或 `str.translate` 去掉指定标点：

```python
import string

clean = text.lower().translate(str.maketrans("", "", string.punctuation))
words = clean.split()
```

### 返回 `dict` 的版本

如果只想拿全量词频，不排序：

```python
def word_counts(text: str) -> dict:
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

---

## 12. 易错点清单

1. **忘记 `lower()`**：`"The"` 和 `"the"` 被当成两个词，次数统计错误。
2. **直接 `counts[word] += 1`**：键不存在时抛 `KeyError`。
3. **忘记 `reverse=True`**：结果按次数升序，第一名变成出现最少的词。
4. **`key=lambda item: item[1]` 写错下标**：元组只有两个元素，`item[2]` 会 `IndexError`。
5. **直接 `sorted(counts)`**：只按键排序，因为遍历 dict 拿到的是键。
6. **以为 `sorted()` 会改原数据**：它返回新列表；要原地排序用 `list.sort()`。
7. **`[:top]` 当成下标**：`top=5` 取 5 个元素，不是下标 5。
8. **参数顺序**：默认参数必须在必填参数之后。
9. **在 `if __name__` 外直接跑逻辑**：被 import 时会重复执行副作用代码。

---

## 13. 变式练习

- 统计字符频率（把 `split()` 换成 `for ch in text`）。
- 读取一个文件，统计全文词频（`open(...).read()` 后复用本函数）。
- 按次数降序、同次数按字母升序（用 `key=lambda item: (-item[1], item[0])`）。
- 加一个 `ignore_case` 参数，调用方决定是否区分大小写。
- 用 `Counter.most_common(top)` 重写并对比两种写法。
