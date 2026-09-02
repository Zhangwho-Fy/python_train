"""ex5 参考答案。"""


def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        else:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def main() -> None:
    assert is_valid("()[]{}") is True
    assert is_valid("([)]") is False
    assert is_valid("(]") is False
    assert is_valid("(") is False
    assert is_valid("") is True
    print("parentheses OK")


if __name__ == "__main__":
    main()
