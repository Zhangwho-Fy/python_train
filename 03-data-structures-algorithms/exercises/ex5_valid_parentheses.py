"""ex5: 括号匹配。"""


def is_valid(s: str) -> bool:
    # TODO: 左括号入栈，右括号与栈顶匹配；用 dict 存配对
    return False


def main() -> None:
    assert is_valid("()[]{}") is True
    assert is_valid("([)]") is False
    assert is_valid("(]") is False
    assert is_valid("(") is False
    assert is_valid("") is True
    print("parentheses OK")


if __name__ == "__main__":
    main()
