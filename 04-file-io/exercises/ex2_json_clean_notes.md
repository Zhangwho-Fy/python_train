# ex2 json_clean 考点详解

## 题目回顾

读 `exercises/students.json`，从里取出学生数组，过滤出 `score >= 80` 的学生，按分数降序，写入 `cleaned.json`（**中文不转义**），并返回列表供打印。

数据长这样：

```json
{
  "students": [
    {"name": "张三", "score": 92, ...},
    ...
  ]
}
```

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `json.load(f)` | 从文件对象读 JSON | 打开 src 后 load |
| `json.dump(obj, f)` | 把对象写进文件 | 写 cleaned.json |
| 根节点不是数组 | JSON 顶层是个对象，数组在 `"students"` 键里 | `data["students"]` |
| 列表推导式过滤 | `[s for s in xs if 条件]` | `score >= threshold` |
| `sorted(..., key=..., reverse=True)` | 按字典的键排序 | `key=lambda s: s["score"]` |
| `ensure_ascii=False` | 写中文不变成 `\uXXXX` | `json.dump(..., ensure_ascii=False)` |

## 1. 读和写的对称 API

```python
import json

# 读
with open(src, encoding="utf-8") as f:
    data = json.load(f)          # 文件对象 → Python dict/list

# 写
with open(dst, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)
```

- `json.load(文件对象)` / `json.dump(对象, 文件对象)`：操作**文件对象**。
- `json.loads(字符串)` / `json.dumps(对象)`：操作**字符串**（多一个 s）。写 HTTP 接口时天天用 `dumps`。
- Python dict ↔ JSON object，list ↔ JSON array，str ↔ string，int/float ↔ number。C++ 对照：约等于 nlohmann/json 的 `parse` 和 `dump`。

## 2. 先看数据结构再取数

```python
def clean_students(src: str, dst: str, threshold: int = 80) -> list:
    with open(src, encoding="utf-8") as f:
        data = json.load(f)

    students = data["students"]          # 顶层是 {"students": [...]}
    cleaned = [s for s in students if s["score"] >= threshold]
    cleaned.sort(key=lambda s: s["score"], reverse=True)   # 分数降序

    with open(dst, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    return cleaned
```

本题最大的“坑”在结构：JSON 顶层**不是数组**而是 `{"students": [...]}`。先 `json.load` 拿到的是 dict，必须 `data["students"]` 才拿到学生列表。做题前先 `cat students.json` 看结构，是正经流程。

过滤后 92（张三）、88（王五）、81（孙七）留下，76/79/55 被过滤。

## 3. 排序与写中文

- `sorted` 配 `key=lambda s: s["score"]`：排序依据是每个学生字典的 score 键。
- `reverse=True` 降序；`list.sort(...)` 原地排序也行（`cleaned` 本来就是新列表）。
- `ensure_ascii=False` 让中文原样写入；不写的话 `张三` 会变成 `"\u5f20\u4e09"`——数据没坏，但人没法读、diff 没法看。

## 4. 易错点清单

1. **忘了顶层 `"students"` 键**：直接把 dict 当列表过滤，`TypeError: 'dict' object is not iterable`。
2. **`json.load` 写成 `json.loads` 且传文件名**：`loads` 需要字符串，传路径会 `AttributeError` 或把文件名当 JSON 解析。
3. **写文件忘 `"w"` 模式**：默认 `"r"`，`json.dump` 时报错。
4. **忘 `ensure_ascii=False`**：中文全变 `\u` 转义。
5. **过滤条件写成 `>` 而不是 `>=`**：正好 80 分的孙七会被丢掉（题目要求 `>=`）。

## 5. 变式练习

- 分数相同时按名字排序：`key=lambda s: (-s["score"], s["name"])`。
- 把结果写成“按分数分组”的 dict 再 dump。
- 从命令行接收 src/dst 参数（`sys.argv`），让脚本可复用。
