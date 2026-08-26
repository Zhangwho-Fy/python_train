"""ex4 参考答案。"""
from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass
class Student:
    name: str
    score: int
    email: str

    def __post_init__(self):
        if not 0 <= self.score <= 100:
            raise ValueError(f"score 越界: {self.score}")


class StudentModel(BaseModel):
    name: str
    score: int = Field(ge=0, le=100)
    email: str


def main() -> None:
    s1 = Student("张三", 92, "zs@example.com")
    m1 = StudentModel(name="张三", score=92, email="zs@example.com")
    print(s1)
    print(m1)

    for maker in (Student, StudentModel):
        try:
            maker("李四", 150, "ls@example.com")
        except Exception as e:
            print(f"{maker.__name__} 拒绝非法数据: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
