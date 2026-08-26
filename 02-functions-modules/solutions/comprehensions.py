"""ex4 参考答案。"""


def main() -> None:
    squares = [x * x for x in range(1, 21) if x % 3 == 0]
    print(squares)
    assert squares == [9, 36, 81, 144, 225, 324]

    names = ["alice", "bob", "carol"]
    ages = [30, 25, 27]
    people = {name: age for name, age in zip(names, ages)}
    print(people)
    assert people == {"alice": 30, "bob": 25, "carol": 27}

    sentence = "the quick brown fox jumps over the lazy dog"
    words = sorted(set(sentence.split()), key=len)
    print(words)
    assert words == sorted(set(sentence.split()), key=len)


if __name__ == "__main__":
    main()
