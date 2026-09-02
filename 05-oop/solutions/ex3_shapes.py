"""ex3 参考答案。"""
import math
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...


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


def total_area(shapes: list) -> float:
    return sum(sh.area() for sh in shapes)


def main() -> None:
    shapes = [Circle(1), Rectangle(2, 3), Circle(2)]
    assert abs(total_area(shapes) - (math.pi + 6 + 4 * math.pi)) < 0.01
    print(f"total area = {total_area(shapes):.2f}")
    print("shapes OK")


if __name__ == "__main__":
    main()
