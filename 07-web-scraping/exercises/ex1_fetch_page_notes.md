# ex1 fetch_page 考点详解

## 题目回顾

用 `requests.get("https://example.com", timeout=10)` 下载页面，检查状态码，把 HTML 存到 `data/example.html`，解析并返回 `<title>` 文本。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `requests.get(url, timeout=10)` | 发 HTTP GET | 下载网页 |
| `resp.status_code` / `raise_for_status()` | 检查 HTTP 状态 | 200 才继续 |
| `resp.text` | 响应体字符串 | 保存 + 解析 |
| `Path.write_text` | 一行写文件 | 存 HTML |
| `mkdir(parents=True, exist_ok=True)` | 自动建目录 | `data/` 不存在时创建 |
| 标题提取 | 正则或 BeautifulSoup 取 `<title>` | `re.search(r"<title>(.*?)</title>")` |

## 1. requests 基本用法

```python
import requests

resp = requests.get("https://example.com", timeout=10)
print(resp.status_code)          # 200
resp.raise_for_status()          # 非 2xx 时抛 HTTPError
html = resp.text                 # 响应体（已按编码解码的字符串）
```

- `requests` 约等于 libcurl 的“友好版”：GET 一个 URL 就一行。
- **必须传 `timeout`**：不传的话请求可能挂很久，脚本像死了一样。超时会抛 `requests.Timeout`。
- `raise_for_status()` 在 4xx/5xx 时抛异常，逼你处理失败而不是拿着错误页面继续。
- `resp.text` 是解码好的字符串；`resp.content` 是原始 bytes（下载图片/二进制用）。

## 2. 保存页面

```python
from pathlib import Path

out = Path(save_to)                     # save_to = "data/example.html"
out.parent.mkdir(parents=True, exist_ok=True)   # 没有 data/ 就建
out.write_text(resp.text, encoding="utf-8")
```

- `Path.write_text` 一行写文件（自动 open/close），相当于 `with open(...) as f: f.write(...)` 的简写。
- `mkdir(parents=True, exist_ok=True)`：`parents=True` 连上级目录一起建，`exist_ok=True` 目录已存在也不报错——这行几乎是写文件的标配。
- `data/` 已被 .gitignore，不会误提交下载内容。

## 3. 提取标题

正则版：

```python
import re

m = re.search(r"<title>(.*?)</title>", resp.text, re.S)
title = m.group(1).strip() if m else ""
```

- `(.*?)` 非贪婪匹配，`re.S` 让 `.` 能匹配换行（标题可能跨行）。
- 解析 HTML 用正则只能应付简单页面；复杂页面用 BeautifulSoup（ex2 专门练）。

## 4. 完整参考

```python
def fetch(url: str, save_to: str) -> str:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    out = Path(save_to)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(resp.text, encoding="utf-8")
    m = re.search(r"<title>(.*?)</title>", resp.text, re.S)
    return m.group(1).strip() if m else ""
```

## 5. 易错点清单

1. **忘 `timeout`**：请求卡住时脚本无法退出。
2. **不检查状态码**：404 页面也会被保存并“解析成功”，返回空标题。
3. **`data/` 目录不存在直接写**：`FileNotFoundError`；先 `mkdir`。
4. **标题正则没加 `re.S`**：标题里若跨行会匹配失败。
5. **网络不通就报错**：example.com 需要外网；离线练习可起本地 `python3 -m http.server` 换 URL。

## 6. 变式练习

- 保存前打印响应头里的 `Content-Type`。
- 把 fetch 改成接收 `headers={"User-Agent": ...}`，很多站点会拒绝默认 UA（ex4 再讲）。
- 对超时/连接错误做一次重试（ex4 的 `fetch_with_retry` 就是这个的升级）。
