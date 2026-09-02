# ex4 big_file 考点详解

## 题目回顾

不把整个文件读进内存，逐行统计 `sample.txt` 每行的长度分布（分桶 0-9 / 10-19 / 20-29 / ...），打印各桶行数。提示：用生成器 `def lines(path): ... yield line`。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 生成器 `yield` | 函数暂停/恢复，逐个产出值 | 逐行产出文件行 |
| `for line in f` | 文件对象可迭代，逐行读取 | 不 `read()` 全文件 |
| `with` + 生成器 | 耗尽后自动关文件 | 内存安全读大文件 |
| `rstrip("\n")` | 去掉行尾换行符再量长度 | `len(line.rstrip("\n"))` |
| 分桶 | 整除定位桶起点 | `(length // 10) * 10` |
| dict 计数 | `get` + 1 经典模式 | 统计各桶行数 |

## 1. 生成器：yield 关键字

```python
def lines(path: str):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line          # 产出一行，函数在这里暂停
```

- 函数体里出现 `yield`，这个函数就变成**生成器函数**：调用它不执行函数体，而是返回一个生成器对象；每次 `for ... in` 或 `next(gen)` 才推进到下一个 `yield`。
- 对比 C++：最接近“惰性求值”，类似 ranges 的 view——边取边算，不一次性物化。
- 生成器只能**单向走一遍**：`list(gen)` 之后 gen 就空了，不能重放。
- `with open(...)` 包在生成器里：迭代到文件末尾（生成器自然结束）时 `with` 块退出、文件关闭——不会句柄泄漏。

## 2. 逐行读大文件

```python
for line in lines("exercises/sample.txt"):
    ...
```

- `for line in f`（直接遍历文件对象）本来就能逐行读，但把它包进 `lines()` 生成器后，调用方逻辑与“怎么读”解耦，还能随时换数据源。
- **别用 `f.read()`**：它把整个文件读成一个大字符串。1 GB 的文件就吃 1 GB+ 内存。

## 3. 行长度与分桶

```python
def bucket_of(length: int) -> str:
    start = (length // 10) * 10     # 13 → 1*10=10；25 → 20
    return f"{start}-{start + 9}"
```

- `13 // 10 == 1`，再 `* 10` 得到桶起点 10。
- 行 `len(line.rstrip("\n"))`：先去掉行尾换行符，不然每行都多算 1（`\n` 是 1 个字符）。

主逻辑：

```python
buckets = {}
for line in lines("exercises/sample.txt"):
    b = bucket_of(len(line.rstrip("\n")))
    buckets[b] = buckets.get(b, 0) + 1

for b in sorted(buckets):
    print(f"{b}: {buckets[b]} 行")
```

- `buckets.get(b, 0) + 1` 是 01 ex4 学过的计数模式：第一次出现默认 0，加一成 1。
- `sorted(buckets)` 按键排序；`"0-9"`、`"10-19"` 这类桶名按字符串排序刚好也是数字序。

## 4. 易错点清单

1. **把生成器函数当普通函数用**：`lines("x.txt")` 返回的是生成器对象，不是列表；要 `for ... in` 或用 `list()`。
2. **`read()` 全文件**：大文件内存爆掉，这是本题要避免的。
3. **量长度没去 `\n`**：所有桶整体偏大 1，桶边界错乱。
4. **`bucket_of` 用 `length % 10` 当起点**：余数不是桶起点，要用整除。
5. **生成器被消费两次**：第二遍是空的；需要重放就重新调用 `lines(path)`。

## 5. 变式练习

- 统计的不是长度而是每行单词数，输出分布。
- 找出最长的一行：遍历时记住 `(行号, 长度)`，只存一个最大值。
- 06 ex5 会把这个生成器升级成“统计行数 + 打印前 5 行”，两个阶段知识点闭环。
