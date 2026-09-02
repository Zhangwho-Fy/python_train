# ex4 comprehensions 考点详解

## 题目回顾

“推导式专场”，三道题各用**一行推导式**完成：

1. `[1..20]` 中能被 3 整除的数的平方列表；
2. 用 `zip` 把 `names` 和 `ages` 合成 dict；
3. 句子拆词、去重、按长度升序排序。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 列表推导式 | `[表达式 for x in 序列 if 条件]` | 平方 + 过滤 |
| 字典推导式 | `{键表达式: 值表达式 for ...}` | zip 合成 dict |
| `zip` | 把多个序列按位置配对 | `zip(names, ages)` |
| `set` 去重 | `set(列表)` 去掉重复 | `set(sentence.split())` |
| `sorted(xs, key=...)` | 自定义排序依据 | `key=len` 按长度排 |
| `str.split()` | 按空白拆词 | 切句子 |

## 1. 列表推导式：map + filter 的语法糖

```python
# [1..20] 中能被 3 整除的数的平方
squares = [x * x for x in range(1, 21) if x % 3 == 0]
```

读法：**“对 range(1,21) 里的每个 x，如果 x%3==0，就把 x*x 放进列表”**。顺序固定：输出表达式 → for → 可选的 if。

期望结果 `[9, 36, 81, 144, 225, 324]`（3, 6, 9, ..., 18 的平方）。

等价展开：

```python
squares = []
for x in range(1, 21):
    if x % 3 == 0:
        squares.append(x * x)
```

对比 C++：约等于 `std::transform` + `std::copy_if` 串起来，但 Python 把“生成”写在表达式里，一行读完。

## 2. `zip` + 字典推导式

```python
names = ["alice", "bob", "carol"]
ages = [30, 25, 27]

people = {name: age for name, age in zip(names, ages)}
```

- `zip(names, ages)` 按位置配对，产生 `("alice", 30)`、`("bob", 25)`、`("carol", 27)`——像 C++ 里两个 vector 按下标对齐。
- 字典推导式 `{键: 值 for ...}`：解包每个 `(name, age)` 元组，存成字典。
- 更短的等价写法：`people = dict(zip(names, ages))`——`dict()` 直接接收键值对序列。先写推导式是为了理解结构，之后可以直接用 `dict(zip(...))`。

## 3. `set` 去重 + 按长度排序

```python
sentence = "the quick brown fox jumps over the lazy dog"

words = sorted(set(sentence.split()), key=len)
```

拆开看：

1. `sentence.split()` → 单词列表，`"the"` 出现两次。
2. `set(...)` → 去重成集合（无序）。
3. `sorted(..., key=len)` → 按每个词的长度升序排序，返回新列表。

要点：

- `key=len` 意思是“排序依据是 `len(词)`”；等价写法 `key=lambda w: len(w)`。同长度的词之间保持去重后的任意顺序，`sorted` 是稳定排序。
- 这一步**不**需要列表推导式（set 本身就够）；题目要的是“选对工具”。

## 4. 易错点清单

1. **推导式顺序写反**：`for x in ...` 必须在 `if` 前面，`[x for x in range(20) if x % 3 == 0]` 对，`[x if x % 3 == 0 for x in range(20)]` 语法错误。
2. **`range(1, 21)` 少了右端**：要含 20。
3. **忘了 `sorted(..., key=len)` 的 `key`**：默认按字母排，不是按长度。
4. **直接对 `sentence.split()` 排序**：`"the"` 会重复出现，先 `set` 去重。
5. **`zip` 忘了转成想要的容器**：`zip` 本身是惰性迭代器，`dict(zip(...))` 或推导式才会真正建结构。

## 5. 变式练习

- 嵌套推导式：`[(x, y) for x in range(3) for y in range(3)]` 生成坐标对。
- 集合推导式 `{w for w in words if len(w) > 3}`、生成器表达式 `sum(x*x for x in range(10))`。
- 把 people 按年龄过滤再生成新 dict：`{n: a for n, a in people.items() if a >= 26}`。
