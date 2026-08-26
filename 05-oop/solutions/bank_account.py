"""ex2 参考答案。"""


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("存款金额必须为正")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("取款金额必须为正")
        if amount > self._balance:
            raise ValueError("余额不足")
        self._balance -= amount

    def __str__(self) -> str:
        return f"{self.owner}: 余额 ¥{self._balance:.2f}"


def main() -> None:
    acc = BankAccount("张三", 100)
    acc.deposit(50)
    assert acc.balance == 150
    acc.withdraw(30)
    assert acc.balance == 120
    print(acc)
    try:
        acc.withdraw(999)
    except ValueError:
        print("超额取款被拒绝")
    print("bank_account OK")


if __name__ == "__main__":
    main()
