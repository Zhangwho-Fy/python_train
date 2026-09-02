"""ex1 参考答案。"""


class Vec2d:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vec2d") -> "Vec2d":
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2d") -> "Vec2d":
        return Vec2d(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vec2d":
        return Vec2d(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vec2d":
        return self.__mul__(scalar)

    def dot(self, other: "Vec2d") -> float:
        return self.x * other.x + self.y * other.y

    def __eq__(self, other) -> bool:
        return isinstance(other, Vec2d) and (self.x, self.y) == (other.x, other.y)

    def __repr__(self) -> str:
        return f"Vec2d({self.x}, {self.y})"


def main() -> None:
    v = Vec2d(1, 2)
    w = Vec2d(3, 4)
    assert v + w == Vec2d(4, 6)
    assert w - v == Vec2d(2, 2)
    assert v * 2 == Vec2d(2, 4)
    assert 2 * v == Vec2d(2, 4)
    assert v.dot(w) == 11
    print(v)
    print("vec2d OK")


if __name__ == "__main__":
    main()
