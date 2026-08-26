"""ex2 参考答案。"""


def my_range(start, stop=None, step=1):
    if stop is None:
        start, stop = 0, start
    if step == 0:
        raise ValueError("step 不能为 0")
    current = start
    if step > 0:
        while current < stop:
            yield current
            current += step
    else:
        while current > stop:
            yield current
            current += step


def main() -> None:
    assert list(my_range(5)) == [0, 1, 2, 3, 4]
    assert list(my_range(1, 10, 2)) == [1, 3, 5, 7, 9]
    assert list(my_range(10, 0, -3)) == [10, 7, 4, 1]
    assert list(my_range(0, 5, -1)) == []
    try:
        list(my_range(0, 5, 0))
    except ValueError:
        print("step=0 正确报错")
    print("my_range OK")


if __name__ == "__main__":
    main()
