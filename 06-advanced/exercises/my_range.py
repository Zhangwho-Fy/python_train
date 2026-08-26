"""ex2: 手写 range 生成器。"""


def my_range(start, stop=None, step=1):
    # TODO: stop 为 None 时 start=0, stop=start；step 不能为 0；
    #       负数 step 要能递减
    pass


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
