"""ex2: 银行账户。"""


class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        # TODO: 只读属性
        return 0.0

    def deposit(self, amount: float) -> None:
        # TODO: amount 必须 > 0
        pass

    def withdraw(self, amount: float) -> None:
        # TODO: amount 必须 > 0 且 <= balance，否则 ValueError
        pass

    def __str__(self) -> str:
        # TODO: "张三: 余额 ¥123.45"
        return ""


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
