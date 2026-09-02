# ex3 shapes 考点详解

## 题目回顾

`Shape(ABC)` 抽象基类 + 抽象方法 `area()`；`Circle(radius)`、`Rectangle(w, h)` 继承实现；`total_area(shapes)` 对列表求和。体会“鸭子类型”：不需要 `isinstance` 检查。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `abc.ABC` + `@abstractmethod` | Python 的抽象基类/纯虚函数 | 强制子类实现 `area()` |
| 继承 `class Circle(Shape)` | 子类复用父类契约 | 两种形状统一接口 |
| `math.pi` | 圆周率 | 圆面积 |
| 多态 | 同一接口不同实现 | `total_area` 不管具体类型 |
| 鸭子类型 | 有 `area()` 就行，不必是 Shape | 直接调用 `sh.area()` |
| 生成器表达式 + `sum` | 一行求总和 | `sum(sh.area() for sh in shapes)` |

## 1. 抽象基类：强制“必须有 area”

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...
```

- `ABC` + `@abstractmethod` ≈ C++ 的纯虚函数/接口：`Shape` 自己不能实例化，子类必须实现 `area()`，否则子类也实例化不了（抛 `TypeError`）。
- `...`（Ellipsis）只是“还没实现”的占位符，函数体写 `pass` 也一样。

## 2. 子类实现

```python
import math

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height
```

- 继承写 `class Circle(Shape):`，不写 `super().__init__()` 也行——`Shape` 没有自己的属性要初始化。
- 每个子类给出**同一接口（area）的不同实现**：这就是多态。

## 3. 多态与鸭子类型

```python
def total_area(shapes: list) -> float:
    return sum(sh.area() for sh in shapes)
```

- `total_area` 不检查 `isinstance(sh, Shape)`，只要对象有 `area()` 方法就能算——这就是“鸭子类型”：“走路像鸭子、叫像鸭子，就是鸭子。”
- C++ 需要基类指针/虚函数表才能多态；Python 运行时动态派发，传什么对象都行。
- `sum(sh.area() for sh in shapes)`：生成器表达式逐个算面积再求和，不需要中间列表。

验证：`Circle(1)` 面积 ≈ 3.14159，`Rectangle(2, 3)` 面积 6，`Circle(2)` ≈ 12.56636，总和 ≈ 21.71。

## 4. 易错点清单

1. **抽象方法漏实现**：`class Triangle(Shape): pass` 想实例化时抛 `TypeError: Can't instantiate abstract class`。
2. **忘继承 ABC**：`class Shape:` + `@abstractmethod` 不生效，Shape 能被实例化。
3. **圆面积写 `2 * pi * r`**：那是周长。
4. **`total_area` 用 isinstance 分支**：`Circle` 一个算法、`Rectangle` 一个算法，以后加 `Triangle` 又要改——多态的目的就是消灭这种分支。
5. **`sum(sh.area() for sh in shapes)` 忘加括号**：`sum(sh.area for sh in shapes)` 会把方法对象求和，报错。

## 5. 变式练习

- 加 `Triangle`、`Square`，`total_area` 不用改一行。
- 加抽象方法 `perimeter()`，让每个形状必须同时实现面积和周长。
- 手写“不是 Shape 但带 area()”的类传进 `total_area`，验证鸭子类型真的生效。
