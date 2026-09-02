# ex5 valid_parentheses 考点详解

## 题目回顾

`is_valid(s)`：字符串只含 `()[]{}`，判断括号是否匹配。用 list 当栈。

期望：`"()[]{}"` → True，`"([)]"` → False（交叉不合法），`"(]"` → False，`"("` → False，`""` → True。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| list 当栈 | `append` 入栈、`pop()` 出栈 | 左括号压栈 |
| 栈顶查看 | `stack[-1]` 看最后一个元素 | 和右括号配对 |
| dict 配对表 | 右括号 → 对应左括号 | `pairs = {")": "(", ...}` |
| 空栈判断 | `not stack` | 弹出前先检查 |
| 最终校验 | 遍历完栈必须为空 | 多出的左括号非法 |

## 1. 用 list 模拟栈

```python
stack = []
stack.append("(")     # push
top = stack[-1]       # peek：看最后一个，不弹出
stack.pop()           # pop：弹出并返回最后一个
```

- C++ 里 `std::stack` 的 `push/top/pop` 是三个操作；Python list 用 `append` 入栈、`[-1]` 看顶、`pop()` 弹出。
- 空列表 `stack.pop()` 会 `IndexError`，所以弹出前先 `if not stack:` 判断。

## 2. 完整解法

```python
def is_valid(s: str) -> bool:
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []

    for ch in s:
        if ch in "([{":          # 左括号：入栈
            stack.append(ch)
        else:                    # 右括号：必须和栈顶匹配
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()

    return not stack             # 遍历完，栈空才合法
```

为什么这个结构对：

- `"([)]"`：`(` 入栈，`[` 入栈，遇到 `)` 时栈顶是 `[` 不是 `(` → 提前 False。
- `"("`：遍历完栈里还有一个 `(` → 最后 `return not stack` 是 False。
- `""`：没进循环，栈空 → True。

## 3. 只计数为什么不够

只数左右括号数量相等会误判 `"([)]"`（数量各 2 但交叉）。括号问题的本质是**顺序 + 最近配对**，恰好是栈的语义：最近打开的括号最先被关闭（LIFO）。

## 4. 易错点清单

1. **弹出前不判空**：`"())"` 第二次遇到 `)` 时栈已空，`stack.pop()` 崩。
2. **用 `stack[-1] == ch` 直接比较**：右括号 `)` 和左括号 `(` 永远不相等，要用配对表把右括号映射成对应左括号再比。
3. **忘了最后检查栈空**：`"(("` 会错误返回 True。
4. **把 `not stack` 写反**：空栈返回 True 才是“合法结束”。
5. **字符遍历用 `for i in range(len(s))` 又按下标**：直接 `for ch in s` 更地道。

## 5. 变式练习

- 支持 `< >` 第四种括号（往 `pairs` 里加一项即可）。
- 返回“第一个出错的位置”而不是 bool。
- 进阶：在字符串里同时去掉合法括号段，输出“最少删几个括号才能合法”。
