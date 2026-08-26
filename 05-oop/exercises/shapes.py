"""ex3: 抽象基类与多态。"""
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        ...


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        # TODO
        return 0.0


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        # TODO
        return 0.0


def total_area(shapes: list) -> float:
    # TODO: sum(sh.area() for sh in shapes)
    return 0.0


def main() -> None:
    shapes = [Circle(1), Rectangle(2, 3), Circle(2)]
    assert abs(total_area(shapes) - (3.14159 + 6 + 12.56636)) < 0.01
    print(f"total area = {total_area(shapes):.2f}")
    print("shapes OK")


if __name__ == "__main__":
    main()
