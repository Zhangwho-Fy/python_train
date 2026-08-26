"""ex1: 二维向量。"""


class Vec2d:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: "Vec2d") -> "Vec2d":
        # TODO
        return self

    def __sub__(self, other: "Vec2d") -> "Vec2d":
        # TODO
        return self

    def __mul__(self, scalar: float) -> "Vec2d":
        # TODO: v * 2
        return self

    def __rmul__(self, scalar: float) -> "Vec2d":
        # TODO: 2 * v（直接复用 __mul__ 即可）
        return self

    def dot(self, other: "Vec2d") -> float:
        # TODO
        return 0.0

    def __eq__(self, other) -> bool:
        # TODO: 判断类型 + 坐标相等
        return False

    def __repr__(self) -> str:
        # TODO: 返回 "Vec2d(1, 2)" 这种形式
        return ""


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
