# ex1 vec2d 考点详解

## 题目回顾

实现 `Vec2d(x, y)`，支持：

- `v + w`、`v - w`（向量加减）
- `v * 2` **和** `2 * v`（标量乘法，两个方向都要成立）
- `v.dot(w)` 点积
- `v == w` 相等判断
- `print(v)` 显示成 `Vec2d(1, 2)`

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `class` + `__init__` | 类定义与构造 | `self.x = x` |
| `self` | 显式的“this” | 方法第一个参数 |
| 运算符重载 | `+ - * ==` 对应 `__add__ __sub__ __mul__ __eq__` | 让 Vec2d 支持算术 |
| `__rmul__` | 左侧不是自己的类型时触发 | 让 `2 * v` 成立 |
| `__repr__` | 开发者可读的字符串表示 | 返回 `"Vec2d(1, 2)"` |
| 返回新对象 | 运算不改自己，返回新实例 | `return Vec2d(...)` |

## 1. 类与构造

```python
class Vec2d:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
```

- `__init__` 是构造方法（对标 C++ 构造函数）。创建 `Vec2d(1, 2)` 时自动调用，`self` 指向新对象。
- `self` 只是惯例名，但必须显式写、且是**第一个参数**——Python 不像 C++ 有隐藏的 `this`。
- `self.x` 存成实例属性，等价 C++ 的 `this->x`。

## 2. 运算符重载 = 双下划线方法

```python
def __add__(self, other: "Vec2d") -> "Vec2d":
    return Vec2d(self.x + other.x, self.y + other.y)

def __sub__(self, other: "Vec2d") -> "Vec2d":
    return Vec2d(self.x - other.x, self.y - other.y)

def __mul__(self, scalar: float) -> "Vec2d":
    return Vec2d(self.x * scalar, self.y * scalar)

def dot(self, other: "Vec2d") -> float:
    return self.x * other.x + self.y * other.y
```

- 运算符被翻译成方法调用：`v + w` 实际执行 `v.__add__(w)`；C++ 里是 `operator+`，概念完全一样。
- **返回新对象，不要改 `self`**：`self.x *= scalar; return self` 会修改调用方，破坏“值语义”。
- 注解写 `"Vec2d"`（引号）是因为方法定义时类还没定义完——这叫前向引用。
- 方法名 `dot` 不是运算符，就是普通方法，和 C++ 的成员函数一样。

## 3. `__rmul__`：让 `2 * v` 成立

`v * 2` 走 `v.__mul__(2)`。但 `2 * v` 时，Python 先试 `(2).__mul__(v)`——整数不认识 Vec2d，返回 `NotImplemented`，于是 Python **再试右侧的 `__rmul__`**：

```python
def __rmul__(self, scalar: float) -> "Vec2d":
    return self * scalar        # 标量乘法可交换，直接复用 __mul__
```

这样 `2 * v == v * 2 == Vec2d(2, 4)`。这是“反射/反向运算符”机制，C++ 里通常用友元或自由函数实现。

## 4. `__eq__` 与 `__repr__`

```python
def __eq__(self, other) -> bool:
    if not isinstance(other, Vec2d):   # 类型不对就不相等，而不是崩
        return NotImplemented
    return self.x == other.x and self.y == other.y

def __repr__(self) -> str:
    return f"Vec2d({self.x}, {self.y})"
```

- 不实现 `__eq__` 时，`v == w` 比的是“是不是同一个对象”（身份），两个内容相同的 Vec2d 会不相等——所以必须重载。
- 对非 Vec2d 返回 `NotImplemented` 而不是 `False` 是规范写法：让 Python 有机会尝试反向比较（比如 `v == 5`）。
- `__repr__` 返回“开发者看”的字符串，`print(v)` 和 REPL 里都会显示它；格式约定尽量能直接 eval：`Vec2d(1, 2)` 就是可执行代码。

## 5. 易错点清单

1. **忘写 `self` 参数**：`def __add__(other):` 一调用就“参数数量不匹配”。
2. **运算改了自己的 x/y**：`v + w` 把 v 改了，后续断言全错。
3. **只写 `__mul__` 不写 `__rmul__`**：`2 * v` 报 `TypeError`。
4. **`__eq__` 里直接 `self.x == other.x`**：`v == "abc"` 会抛 `AttributeError`，先 `isinstance` 判断。
5. **`__repr__` 返回的不是字符串**：比如 `return Vec2d(...)`，必须 `return f"..."`。

## 6. 变式练习

- 实现 `__neg__`（取反）、`__abs__`（模长）、`__truediv__`（除以标量）。
- 实现 `__iadd__` 支持 `v += w` 原地加。
- 加 `length()` / `normalized()`，体会“方法返回新对象”的流畅写法。
