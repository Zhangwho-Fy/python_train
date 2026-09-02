# ex5 lazy_reader 考点详解

## 题目回顾

`lazy_lines(path)` 生成器逐行 yield（不把文件全读进内存），统计总行数并打印前 5 行。这是 04 阶段 ex4 的标准答案，两个阶段做完知识闭环。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 生成器读文件 | `with open + for line in f + yield` | 逐行产出 |
| `pathlib.Path` | 面向对象的路径 | 跨目录定位 sample.txt |
| `Path(__file__).parent` | 相对“本文件”拼路径 | 从哪运行都不迷路 |
| `enumerate` | 同时拿序号和元素 | 打印前 5 行 |
| `rstrip("\n")` | 去行尾换行 | 干净打印 |
| 惰性统计 | 边遍历边计数 | 不 read() 全文件 |

## 1. 生成器逐行读

```python
def lazy_lines(path: str):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line
```

- 直接 `for line in f` 本来就是逐行读；包成生成器后，遍历到文件尾 `with` 自动关文件。
- 04 ex4 练过逐行统计；这里复用它读**另一个目录**的文件，主入口用 pathlib 定位。

## 2. 用 pathlib 定位跨目录文件

```python
from pathlib import Path

here = Path(__file__).parent              # .../06-advanced/exercises
src = here.parent.parent / "04-file-io" / "exercises" / "sample.txt"
```

- `Path(__file__).parent`：`__file__` 是当前脚本路径，`.parent` 取它所在目录。这样不管你在哪个目录运行 `python3 exercises/ex5_lazy_reader.py`，路径都正确——比写死相对路径稳。
- `Path / "子目录"` 拼接路径，相当于 `std::filesystem::path` 的 `operator/`。
- `here.parent.parent`：exercises → 06-advanced → 仓库根目录，再往下拼到 04 的 sample.txt。

## 3. 遍历与计数

```python
count = 0
for i, line in enumerate(lazy_lines(str(src))):
    if i < 5:
        print(line.rstrip("\n"))
    count += 1
print(f"总行数: {count}")
```

- `enumerate(可迭代对象)` 产出 `(序号, 元素)`，`for i, line in ...` 解包——比手写 `i += 1` 干净。
- `line.rstrip("\n")`：去掉换行符再打印，避免每行中间空一行。
- 只遍历一遍就拿到“前 5 行 + 总行数”，内存里永远只有当前一行——这就是生成器的价值。

## 4. 易错点清单

1. **`lazy_lines` 返回生成器，不是列表**：`len(lazy_lines(path))` 会报错（生成器没有 len）。
2. **忘 `with`**：直接用 `open(path)` 遍历后不关文件；在生成器里尤其容易忘。
3. **打印带 `\n`**：`print(line)` 自带换行 + 行尾还有 `\n`，输出多空行。
4. **路径写死相对 cwd**：从仓库根目录运行时找不到 `exercises/sample.txt`，用 `Path(__file__).parent` 规避。
5. **想统计两次**：生成器一次耗尽；需要两遍就重新调用 `lazy_lines(src)`。

## 5. 变式练习

- 把前 5 行改成“第 3~8 行”（enumerate + 范围判断）。
- 统计每行字符数分布（直接复用 04 ex4 的 `bucket_of` 逻辑）。
- 让 `lazy_lines` 支持 `Path` 对象参数（内部 `open(path)` 两者都收，体会鸭子类型）。
