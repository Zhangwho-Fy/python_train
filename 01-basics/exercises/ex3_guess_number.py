"""ex3: 猜数字游戏。"""
import random


def main() -> None:
    target = random.randint(1, 100)
    guesses = 0
    while True:
        guesses = int(input("猜数字，范围：1~100,输入："))
        if guesses > target:
            print("猜大了")
        elif guesses < target:
            print("猜小了")
        else:
            print("猜对了")
            break;


if __name__ == "__main__":
    main()
