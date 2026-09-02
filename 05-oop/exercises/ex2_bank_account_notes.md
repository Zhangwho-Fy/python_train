# ex2 bank_account 考点详解

## 题目回顾

`BankAccount(owner, balance=0)`：`deposit` / `withdraw`，余额不足抛 `ValueError`；`balance` 用 `@property` 变成**只读**；`__str__` 输出 `张三: 余额 ¥123.45`。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 私有约定 `_balance` | 下划线表示“别直接碰” | 内部余额存 `_balance` |
| `@property` | 方法伪装成属性 | `acc.balance` 不带括号 |
| 只读属性 | 只写 getter 不写 setter | 外部不能改余额 |
| `raise ValueError` | 主动抛业务异常 | 负数/超额取款 |
| `__str__` | 给用户看的字符串 | 打印账户 |
| f-string 数字格式 | `:.2f` 两位小数 | `¥123.45` |

## 1. 属性与“私有”约定

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance
```

- Python 没有 `private` 关键字。约定：`_balance` 下划线开头表示“内部实现，外部别动”——只是约定，不是强制。
- 把存钱的真实字段命名为 `_balance`，是为了和下面的公开属性 `balance` 区分开，避免名字冲突。

## 2. `@property`：把方法变成属性

```python
@property
def balance(self) -> float:
    return self._balance
```

- 加了 `@property` 后，`acc.balance` **不带括号**就能取值，像读字段一样；带括号 `acc.balance()` 反而报错。
- **只写了 getter、没写 setter** → 外部 `acc.balance = 999` 会抛 `AttributeError: property has no setter`，这就是“只读”。
- C++ 对照：就是 getter 函数，但语法上像 public 字段——Python 社区的惯用做法是“先直接写属性，需要约束时再升级成 property”，调用方代码不用改。

## 3. 业务校验：deposit / withdraw

```python
def deposit(self, amount: float) -> None:
    if amount <= 0:
        raise ValueError("存款金额必须大于 0")
    self._balance += amount

def withdraw(self, amount: float) -> None:
    if amount <= 0:
        raise ValueError("取款金额必须大于 0")
    if amount > self._balance:
        raise ValueError("余额不足")
    self._balance -= amount
```

- 金额合法性是“业务不变量”，用 `raise ValueError(...)` 主动拦，类比 C++ 的 `throw std::invalid_argument`。
- 调用方用 `try/except ValueError` 接（01 ex5 讲过）：

```python
try:
    acc.withdraw(999)
except ValueError as e:
    print("超额取款被拒绝")
```

## 4. `__str__` 与打印格式

```python
def __str__(self) -> str:
    return f"{self.owner}: 余额 ¥{self._balance:.2f}"
```

- `__str__` 定义 `str(obj)` 和 `print(obj)` 的输出。
- `:.2f` 把 `123.4` 格式化成 `123.40`——金额显示两位小数。
- `print(acc)` 输出 `张三: 余额 ¥100.00`。用 `_balance` 直接读没问题（类内部不受“私有约定”限制）。

## 5. 易错点清单

1. **字段直接叫 `balance`，property 也叫 `balance`**：名字冲突，要么字段改名 `_balance`，要么 getter 叫别的。
2. **访问属性加了括号**：`acc.balance()` 不是函数，报“not callable”。
3. **`property` 忘加 `@property` 装饰器**：那 `balance` 就是普通方法，读字段语义没了。
4. **校验顺序反了**：先改 `_balance` 再检查，出错时余额已经被污染。先校验、后修改。
5. **`__str__` 忘 return**：`print(acc)` 输出 `None`。

## 6. 变式练习

- 加 `transfer_to(other, amount)`：先 `self.withdraw` 再 `other.deposit`，异常自动回滚。
- 给 `balance` 加 setter 并做审计：每次修改打印日志。
- 实现 `__repr__` 让调试显示 `BankAccount(张三, 120.0)`。
