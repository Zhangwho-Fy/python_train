# ex3 logger 考点详解

## 题目回顾

先手写 `log(level, message)`：打印 `[时间] [级别] 消息` 并**追加**写入 `app.log`；再用标准库 `logging` 配同格式 logger，对比两种写法。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `datetime.now()` | 取当前时间 | 拼时间戳 |
| `strftime` | 把时间格式化成字符串 | `"%Y-%m-%d %H:%M:%S"` |
| 文件模式 `"a"` | 追加写入，不清空旧内容 | 写 app.log |
| `with open(..., "a", encoding="utf-8")` | 自动关文件 | 边打边写 |
| `logging.basicConfig` | 一次性配置根 logger | 配格式和级别 |
| `logger.info / logger.error` | 按级别输出 | 模块化日志 |

## 1. 手写版：时间格式化

```python
from datetime import datetime

def log(level: str, message: str, filename: str = "app.log") -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}"
    print(line)
    with open(filename, "a", encoding="utf-8") as f:
        f.write(line + "\n")
```

- `datetime.now()` 返回当前时间对象；`.strftime(...)` 按格式串输出，`%Y` 年份、`%m` 月份、`%d` 日、`%H:%M:%S` 时分秒。
- 文件模式 `"a"`（append）：每次在**末尾追加**，不会清掉历史日志。`"w"` 会每次清空重写——写日志几乎永远用 `"a"`。
- `f.write(line + "\n")`：写文件不会自动换行，和 `print` 不同，要自己补 `\n`。

## 2. 标准库 `logging` 版

```python
import logging

def setup_logging(filename: str = "app.log"):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)
```

```python
logger = setup_logging()
logger.info("logging 模块启动")
logger.error("logging 模块错误")
```

- `logging.basicConfig` 里的 `format` 是 **`%(名字)s` 占位符风格**：`%(asctime)s` 是自动时间、`%(levelname)s` 是级别、`%(message)s` 是消息。
- `datefmt` 控制时间部分的格式，可以和手写版完全一致。
- `logging.getLogger(__name__)` 按模块名拿 logger；在同一个脚本里 `__name__` 是 `"__main__"`。
- `logger.info / error / warning / debug` 按级别输出，`level=logging.INFO` 以下（如 DEBUG）默认不显示。

## 3. 两种写法怎么取舍

| | 手写版 | logging |
| --- | --- | --- |
| 优点 | 零依赖、逻辑全透明，适合学原理 | 级别过滤、多 handler、轮转、线程安全 |
| 缺点 | 级别/格式都要自己管，越写越乱 | 配置概念多，初学略绕 |
| 适用 | 脚本/教学 | 正式项目、库代码 |

实战结论：写自己的脚本怎么都行；进正式项目直接用 `logging`。后面的 LangChain 阶段会看到框架到处用 `logger`。

## 4. 易错点清单

1. **文件模式写成 `"w"`**：每次运行清空日志，历史全没。
2. **`f.write(line)` 不补 `\n`**：所有日志挤成一行。
3. **`strftime` 的 `%` 写错**：`%M` 是分钟、`%m` 是月份，容易混。
4. **`logging` 的 format 用 f-string 语法**：`format=f"[{asctime}]..."` 不会生效，必须用 `%(asctime)s` 风格。
5. **`basicConfig` 调用多次不生效**：第一次调用后配置就固定了，之后调用会被忽略。

## 5. 变式练习

- 让 `log` 返回写入的那一行，便于测试断言。
- 给 logging 同时配“终端 + 文件”两个 handler（`StreamHandler` + `FileHandler`）。
- 把级别、文件路径抽成配置，函数接收参数而不是写死。
