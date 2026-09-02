"""ex4: dataclass vs pydantic。"""


# TODO: @dataclass 定义 Student(name, score, email)，__post_init__ 校验 0 <= score <= 100


# TODO: pydantic BaseModel 定义 StudentModel，score 用 Field(ge=0, le=100)


def main() -> None:
    # 合法数据两个版本都该能建
    # 非法数据：Student 抛 ValueError，StudentModel 抛 ValidationError
    pass


if __name__ == "__main__":
    main()
