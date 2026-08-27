"""ex2: 1..n 的 FizzBuzz。"""


def fizzbuzz(n: int) -> None:
    # TODO: for i in range(1, n + 1): 判断 15/3/5 的倍数
    for i in range(1, n + 1):
        if i % 15 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

def main() -> None:
    n = int(input("n = "))
    fizzbuzz(n)


if __name__ == "__main__":
    main()
