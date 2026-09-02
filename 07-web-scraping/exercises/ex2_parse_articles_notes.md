# ex2 parse_articles 考点详解

## 题目回顾

用 BeautifulSoup 解析**本地** `exercises/sample.html`（无需联网）：提取每篇文章的标题、链接、日期，输出列表并写入 `articles.json`。

`sample.html` 结构：`<li class="article">` 里有一个 `<h2><a href="...">标题</a></h2>` 和一个 `<span class="date">日期</span>`，共 4 篇。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| `BeautifulSoup(html, "html.parser")` | 把 HTML 字符串解析成 DOM 树 | 本地文件 read 后解析 |
| CSS 选择器 `.select("li.article")` | 按类名批量选节点 | 拿到 4 个 li |
| `.select_one("a")` | 选第一个匹配子节点 | 拿标题链接 |
| `.get_text(strip=True)` | 取纯文本并去空白 | 标题/日期 |
| `.get("href")` | 取属性值 | 链接 |
| 列表 + dict | 结构化数据 | 每篇一个 dict |
| `json.dump` | 写 JSON | `articles.json` |

## 1. 解析 HTML 为 DOM

```python
from bs4 import BeautifulSoup
from pathlib import Path

html = Path("exercises/sample.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")
```

- BeautifulSoup 把 HTML 变成一棵可查询的树，不用手写正则抠字符串。
- `"html.parser"` 是 Python 标准库解析器，够用且零额外依赖。
- C++ 对照：与其手写字符串处理 + 正则，不如按 DOM 结构选择，稳定得多。

## 2. 用 CSS 选择器取节点

```python
for li in soup.select("li.article"):
    a = li.select_one("a")                  # li 里的第一个 <a>
    date = li.select_one("span.date")       # li 里的 <span class="date">
```

- `soup.select("li.article")` 返回所有匹配 `class="article"` 的 li（CSS 类选择器写法）。
- `select_one` 只取第一个匹配，适合“每个 li 里只有一个 a/span”的结构。
- 若结构变化（比如 `h2` 里包着 a），用 `li.select_one("h2 a")` 这种后代选择器更稳。

## 3. 取文本与属性

```python
articles.append({
    "title": a.get_text(strip=True),    # "Python 装饰器入门"
    "link": a.get("href"),              # "/posts/1"
    "date": date.get_text(strip=True) if date else "",
})
```

- `get_text(strip=True)`：取节点内全部文本并去掉首尾空白。`a.text` 也行，但可能带回换行/空格。
- `.get("href")` 取属性值；属性不存在返回 None（dict 风格）。链接触发相对路径 `/posts/1`，拼接完整 URL 是加分项（用 `urljoin`）。
- `if date else ""`：防御性写法，某个 li 缺日期时不会崩。

## 4. 写入 JSON

```python
import json

with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
```

- 04 阶段练过的套路：`ensure_ascii=False` 保中文，`indent=2` 格式化方便人读。
- 期望 4 篇文章：标题/链接/日期一一对应 sample.html。

## 5. 易错点清单

1. **忘给 BeautifulSoup 传解析器**：`BeautifulSoup(html)` 会警告并猜解析器，行为不稳定。
2. **选择器写错**：`li.article` 的点和 class 值要一致；写成 `select("li article")` 语义完全不同（后代关系）。
3. **`get_text()` 拿到嵌套文本**：如果 a 里还有 span，文本会拼接，注意 strip。
4. **不判空就 `.get("href")`**：None 会写进 JSON，可接受但要意识到。
5. **把整个 soup 塞进 JSON**：`json.dump(soup)` 会失败；先转成纯 dict/list。

## 6. 变式练习

- 给链接拼上 `https://example.com` 前缀（`urllib.parse.urljoin`）。
- 解析 `<h1>`、导航菜单等其他结构，熟悉 select 语法。
- 用 `attrs={"class": "article"}` 的旧式 `find_all` 写一遍，对比 CSS 选择器哪个好读。
