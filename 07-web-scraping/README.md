# 07 网络与爬虫

## 本阶段目标

用 requests 发 HTTP、用 BeautifulSoup 解析 HTML、写一个礼貌的爬虫。

## C++ 对照

- `requests` ≈ libcurl，但 API 友好一百倍；
- `BeautifulSoup` ≈ 字符串处理 + 正则，但按 DOM 结构选择，稳得多；
- 请求头 / 状态码 / cookie 这些概念你都熟，直接迁移即可。

## 道德与法律（重要）

- 只爬自己有权限/允许的站点，先看 `robots.txt` 和网站 ToS；
- 控制频率（`time.sleep`）、设置 UA、失败重试（指数退避）；
- 不爬需要登录的数据，不把结果用于未经许可的商业用途。

## 练习题

每题在 `exercises/` 里有配套考点详解（`exN_xxx_notes.md`），卡住先翻详解再翻答案。

### ex1 fetch_page

考点详解：`exercises/ex1_fetch_page_notes.md`

`requests.get("https://example.com", timeout=10)`，打印状态码和页面标题（`<title>`），
把 HTML 保存到 `data/example.html`。注意 `data/` 已被 gitignore，不会误提交。

### ex2 parse_articles

考点详解：`exercises/ex2_parse_articles_notes.md`

解析本地 `exercises/sample.html`（**无需联网**）：提取每篇文章的标题、链接、日期，
输出列表并写入 `articles.json`。

### ex3 github_api

考点详解：`exercises/ex3_github_api_notes.md`

调 GitHub API `https://api.github.com/users/{user}/repos?per_page=100`，
列出 star 数 > 0 的仓库（名称 + 语言 + star），并处理分页（超过 100 个仓库时翻页）。
无 token 有 60 次/小时限额，别写死循环。

### ex4 polite_crawler

考点详解：`exercises/ex4_polite_crawler_notes.md`

写通用 `fetch_with_retry(url, retries=3)`：失败后等 `2 ** attempt` 秒再试；
再写 `crawl(urls)`：逐个抓取，每个之间 `time.sleep(1)`，带上浏览器 UA。

## 环境

```bash
pip install -r requirements.txt
```

## 期望输出示例

- ex1：状态码 200 + `Example Domain`
- ex2：4 篇文章的标题/链接/日期
- ex3：`{名称} | 语言 | ★123`
- ex4：带 UA 的请求头、每次间隔 1 秒的日志
