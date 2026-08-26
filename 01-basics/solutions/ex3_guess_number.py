"""ex3 参考答案。"""
import random


def main() -> None:
    target = random.randint(1, 100)
    guesses = 0
    while True:
        line = input("猜一个 1~100 的整数: ")
        if not line:  # 空输入直接退出，方便脚本测试
            break
        try:
            guess = int(line)
        except ValueError:
            print("请输入整数")
            continue
        guesses += 1
        if guess < target:
            print("小了")
        elif guess > target:
            print("大了")
        else:
            print(f"猜中! 一共猜了 {guesses} 次")
            break


if __name__ == "__main__":
    main()
