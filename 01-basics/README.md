# 01 语法基础（对照 C++）

## 本阶段目标

会用变量、容器、控制流写出能跑的小程序，习惯“缩进代替大括号”。

## C++ 对照速览

| Python | C++ 类似物 | 一句话 |
| --- | --- | --- |
| `int / float / str / bool / None` | `int / double / std::string / bool` | 动态类型：不用声明，`x = 3` 后还能 `x = "hi"` |
| `list` | `std::vector` | 可混装不同类型，`arr.append(x)` |
| `dict` | `std::map` / `unordered_map` | `d["k"] = v`，`d.get("k", 默认值)` |
| `tuple` | `std::pair` / struct | 不可变，可解包 `a, b = (1, 2)` |
| `set` | `std::set` | 去重，`x in s` 判断 |
| `for x in xs:` | `for (auto& x : xs)` | 遍历就完事；要下标用 `enumerate` |
| `range(10)` | `for (int i = 0; i < 10; ++i)` | 半开区间；`range(2, 10, 3)` |
| `s[i:j]` 切片 | 迭代器区间 | `s[::-1]` 反转 |
| `f"{name}!"` | `std::format` / `sprintf` | 格式化字符串 |
| `and / or / not` | `&& / \|\| / !` | 短路求值一样 |

## 关键差异（会踩坑的点）

1. **缩进即语法**：同一块代码缩进必须一致，统一用 4 空格。
2. **没有 `{}` 作用域**：`if` 里定义的变量，外面照样能用。
3. **整数除法 `//`，普通 `/` 永远是浮点**：`5 / 2 == 2.5`，`5 // 2 == 2`。
4. **字符串不可变**：`s[0] = 'x'` 会报错；`s.replace(...)` 返回新串。
5. **`==` 比内容，`is` 比身份**：`[1, 2] == [1, 2]` 是 `True`。
6. **布尔值是大写 `True / False`**，不是 `true / false`。
7. 不用 `;`，一行一句；不加分号。

## 与 LangChain 的关系

后面写 prompt 模板、解析模型输出，本质都是字符串 + 容器操作；
这里练熟 `f-string` 和 `dict`，后面会非常顺。

## 练习题（先自己写，卡住再看 `solutions/`）

每道题在 `exercises/` 里配了一份 `exN_xxx_notes.md` 考点详解：先凭 README 的速览做题，卡住再打开对应详解。

### ex1 hello

考点详解：`exercises/ex1_hello_notes.md`

问用户名字，打印 `你好, <名字>! 你的名字有 N 个字符。`

考点：`input()`、`len()`、`f-string`。

### ex2 fizzbuzz

考点详解：`exercises/ex2_fizzbuzz_notes.md`

输入 n，输出 1..n：3 的倍数打 `Fizz`，5 的倍数打 `Buzz`，15 的倍数打 `FizzBuzz`。

考点：`range`、`%`、`if/elif`。期望：n=15 时第 15 行是 `FizzBuzz`。

### ex3 guess_number

考点详解：`exercises/ex3_guess_number_notes.md`

程序随机生成 1~100 的整数，用户猜：大了/小了给提示，猜中后统计次数。

考点：`random`、`while`、`int()` 转换。提示：`import random; random.randint(1, 100)`。

### ex4 word_frequency

考点详解：`exercises/ex4_word_frequency_notes.md`

给一句话，统计每个词出现次数，按次数降序打印前 5。

考点：`dict`、`.get()`、`split()`、排序。
期望：`"the quick brown fox jumps over the lazy dog the"` 中 `the` 出现 3 次（开头 1 次 + `over the` 1 次 + 结尾 1 次）。

### ex5 calculator

考点详解：`exercises/ex5_calculator_notes.md`

命令行计算器：输入 `3 + 5` 这种带空格的表达式，循环计算直到输入 `quit`。支持 `+ - * /`。

考点：`split()`、`float()`、条件分支、`while True`。
提示：不用处理括号，先做两个操作数。
