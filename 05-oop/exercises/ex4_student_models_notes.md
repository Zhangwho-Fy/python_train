# ex4 student_models 考点详解

## 题目回顾

两种方式定义 `Student(name, score, email)`：

1. `@dataclass` + `__post_init__` 校验 score 在 0~100，非法抛 `ValueError`；
2. pydantic `BaseModel`，`score: int = Field(ge=0, le=100)`，非法抛 `ValidationError`。

对比两种报错，装依赖：`pip install -r requirements.txt`（含 `pydantic>=2.5`）。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `@dataclass` | 自动生成 `__init__/__repr__/__eq__` | 少写样板代码 |
| `__post_init__` | 初始化后钩子，做自定义校验 | 检查 score 范围 |
| `raise ValueError` | 运行时手动报错 | dataclass 版校验 |
| pydantic `BaseModel` | 声明式 + 运行时校验的数据类 | 字段级约束 |
| `Field(ge=0, le=100)` | 大于等于/小于等于约束 | 声明 score 范围 |
| `ValidationError` | pydantic 的结构化报错 | 非法输入处理 |

## 1. `@dataclass`：少写样板代码

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    score: int
    email: str

    def __post_init__(self):
        if not 0 <= self.score <= 100:
            raise ValueError(f"score 必须在 0~100，收到 {self.score}")
```

- 普通类要手写 `__init__`、`__repr__`、`__eq__`；`@dataclass` 按字段声明自动生成——等价 C++ 里手写 POD + 一堆样板，或者一个自带比较的结构体。
- `score: int` 是**声明**，dataclass 用它们生成构造参数；类型不写也不影响运行。
- `__post_init__` 在 `__init__` 末尾被自动调用，专门放“字段赋值之外还要做的校验/派生逻辑”。
- 只靠 `@dataclass` **不会自动校验范围**，必须自己在 `__post_init__` 里 `raise`。

## 2. pydantic：声明即校验

```python
from pydantic import BaseModel, Field

class StudentModel(BaseModel):
    name: str
    score: int = Field(ge=0, le=100)   # greater-equal / less-equal
    email: str
```

- `BaseModel` 是“带运行时校验的 dataclass”：构造时 `StudentModel(name="张三", score=150)` 直接抛 `ValidationError`，不用你写一行校验代码。
- `Field(ge=0, le=100)` 声明约束：`ge` = greater or equal，`le` = less or equal。还支持 `gt/lt/min_length/max_length/pattern` 等一大堆。
- 校验失败时，`ValidationError` 里带**结构化错误详情**：哪个字段错、错在哪、收到什么值。

```python
from pydantic import ValidationError

try:
    StudentModel(name="张三", score=150, email="a@b.com")
except ValidationError as e:
    print(e)   # 显示 score 字段：Input should be less than or equal to 100
```

## 3. dataclass vs pydantic 怎么选

| | dataclass | pydantic BaseModel |
| --- | --- | --- |
| 校验 | 不校验，要自己写 `__post_init__` | 声明约束自动校验 |
| 类型转换 | 不转，传 str 就存 str | 尽力转换：`"92"` 会转成 int |
| 报错 | 你 raise 什么就是什么 | 结构化 `ValidationError`（字段级） |
| 性能 | 构造快 | 校验有开销 |
| 适用 | 内部数据容器 | 外部输入（HTTP/JSON/配置文件） |

后面的 LangChain 阶段：消息、工具参数、输出解析全部基于 pydantic——05 练的这一题就是 09 的地基。

## 4. 易错点清单

1. **dataclass 忘了 `@dataclass` 装饰器**：类照常能用，但没有自动 `__init__`/`__eq__`，处处踩坑。
2. **`__post_init__` 拼错**：下划线写法漏一个，校验静默不执行。
3. **pydantic 没装**：`ModuleNotFoundError: No module named 'pydantic'`，先 `pip install -r requirements.txt`。
4. **`Field` 忘 import**：v2 里 `Field` 从 `pydantic` 导入。
5. **捕获用裸 `except:`**：pydantic 的校验错误类型是 `ValidationError`，要用它接，避免吞掉别的异常。
6. **`ge/le` 语义记反**：`ge=0` 是“≥0”，`le=100` 是“≤100”。

## 5. 变式练习

- 给 email 加 `EmailStr`（需要 `email-validator`），让格式也自动校验。
- 用 `field(metadata=...)` / `Field(description=...)` 加文档注释，生成 JSON Schema。
- 写一个 `from_json` 函数把 `{"name": "张三", "score": "92", ...}` 直接喂给 `StudentModel`，观察字符串自动转 int。
