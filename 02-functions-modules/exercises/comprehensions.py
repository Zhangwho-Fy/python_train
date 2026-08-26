"""ex4: 推导式专场。"""


def main() -> None:
    # 1. [1..20] 中能被 3 整除的数的平方
    squares = []  # TODO
    print(squares)
    assert squares == [9, 36, 81, 144, 225, 324]

    # 2. zip 合成字典
    names = ["alice", "bob", "carol"]
    ages = [30, 25, 27]
    people = {}  # TODO
    print(people)
    assert people == {"alice": 30, "bob": 25, "carol": 27}

    # 3. 拆词、去重、按长度排序
    sentence = "the quick brown fox jumps over the lazy dog"
    words = []  # TODO
    print(words)
    assert words == sorted(set(sentence.split()), key=len)


if __name__ == "__main__":
    main()
