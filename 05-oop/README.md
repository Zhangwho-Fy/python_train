# 05 面向对象与数据模型

## 本阶段目标

会用 class、property、继承、dataclass；认识 pydantic——它是 LangChain 的模型基座。

## C++ 对照

| Python | C++ 类似物 |
| --- | --- |
| `class A:` | `class A { };` |
| `__init__(self)` | 构造函数 |
| `self.x` | `this->x`（self 显式传） |
| `__add__ / __eq__ / __repr__` | `operator+` / `==` / `<<` |
| `@property` | getter/setter |
| `class B(A)` + `super().__init__()` | 继承 + 基类构造函数 |
| `abc.ABC` + `@abstractmethod` | 纯虚函数 / 接口 |
| `@dataclass` | 手写 POD + 比较/打印样板代码 |
| 没有 `private` | 约定 `_x` 私有；`__x` 名称修饰 |

## 要点

- **`self` 只是惯例**：方法第一个参数就是实例本身，名字叫什么都行，但都写成 `self`。
- **没有重载**：`def f(self, x)` 不能按参数类型重载；用默认参数或类型分派。
- **`__repr__` 给开发者看，`__str__` 给用户看**：`print(obj)` 走 `__str__`，REPL 里显示 `__repr__`。
- **dataclass 自动生成 `__init__/__repr__/__eq__`**，加 `frozen=True` 得不可变对象。
- **pydantic 是“带运行时校验的 dataclass”**：LangChain 的消息、工具参数、输出解析全靠它，这阶段先混个脸熟。

## 与 LangChain 的关系

LangChain 里你写的 `@tool` 函数签名、`PydanticOutputParser`、消息对象，全都基于 pydantic。
把 ex4 做完，后面看 LangChain 的类型报错会淡定很多。

## 练习题

每题在 `exercises/` 里有配套考点详解（`exN_xxx_notes.md`），卡住先翻详解再翻答案。

### ex1 vec2d

考点详解：`exercises/ex1_vec2d_notes.md`

`Vec2d(x, y)`：实现 `__add__`、`__sub__`、`__mul__`（标量）、`dot`、`__eq__`、`__repr__`；
要求 `v * 2` 和 `2 * v` 都成立（后者需要 `__rmul__`，或返回 `NotImplemented` 让 Python 调反向方法）。

### ex2 bank_account

考点详解：`exercises/ex2_bank_account_notes.md`

`BankAccount(owner, balance=0)`：`deposit` / `withdraw`（余额不足抛 `ValueError`）；
`balance` 用 `@property` 只读；`__str__` 输出 `张三: 余额 ¥123.45`。

### ex3 shapes

考点详解：`exercises/ex3_shapes_notes.md`

`Shape(ABC)` 抽象基类 + `area()` 抽象方法；`Circle(radius)`、`Rectangle(w, h)`；
`total_area(shapes)` 对列表求和。体会“鸭子类型”：不用 `isinstance` 检查也能工作。

### ex4 student_models

考点详解：`exercises/ex4_student_models_notes.md`

先用 `@dataclass` 定义 `Student(name, score, email)`，在 `__post_init__` 里校验 score 0~100；
再用 pydantic `BaseModel` 定义同样字段，`score: int = Field(ge=0, le=100)`。
跑一下非法输入，对比两种报错。装依赖：`pip install -r requirements.txt`。

## 期望输出示例

- ex1：`Vec2d(1, 2) + Vec2d(3, 4) == Vec2d(4, 6)`；`2 * Vec2d(1, 2) == Vec2d(2, 4)`
- ex2：取款超额抛 `ValueError`，`__str__` 格式正确
- ex3：`total_area([Circle(1), Rectangle(2, 3)]) ≈ 9.14`
- ex4：非法 score 时，dataclass 抛 `ValueError`，pydantic 抛 `ValidationError`（含详细错误）
