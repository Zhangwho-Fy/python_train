# ex3 github_api 考点详解

## 题目回顾

调 GitHub API `https://api.github.com/users/{user}/repos?per_page=100`，列出 star 数 > 0 的仓库（名称 + 语言 + star），并处理分页：超过 100 个仓库时翻页继续。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| REST API + JSON | HTTP 接口返回 JSON，用 `resp.json()` 转 Python | GitHub 仓库列表 |
| `params={...}` | requests 把参数拼成查询串 | `per_page=100&page=N` |
| 分页循环 | 返回不足一页就停 | `while True` + 条件 break |
| `stargazers_count` | GitHub 返回的星数字段 | 过滤 > 0 |
| `dict.get("language")` | 字段可能为 null，安全取值 | 语言可能是 None |
| 限流意识 | 无 token 60 次/小时 | 别写死循环 |

## 1. API 返回的 JSON 结构

GitHub 仓库列表接口返回一个 **JSON 数组**，每个元素是仓库对象，相关字段：

- `name`：仓库名
- `stargazers_count`：star 数
- `language`：主语言（可能为 `null`）

```python
resp = requests.get(
    f"https://api.github.com/users/{username}/repos",
    params={"per_page": 100, "page": 1},
    timeout=10,
)
data = resp.json()        # list[dict]
```

`params=` 会把 dict 拼成 `?per_page=100&page=1`，还自动处理转义——比手拼 f-string 稳。

## 2. 分页循环

```python
def starred_repos(username: str) -> list:
    repos = []
    page = 1
    while True:
        resp = requests.get(
            f"https://api.github.com/users/{username}/repos",
            params={"per_page": 100, "page": page},
            headers={"Accept": "application/vnd.github+json"},
            timeout=10,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:                    # 空页 = 到底了
            break
        repos.extend(r for r in batch if r["stargazers_count"] > 0)
        if len(batch) < 100:             # 不足一页 = 没有下一页
            break
        page += 1
    return [
        {"name": r["name"], "language": r.get("language"), "stars": r["stargazers_count"]}
        for r in repos
    ]
```

- 分页通用套路：请求第 page 页 → 处理 → 如果**返回数量 < 每页上限**就停，否则 `page += 1` 继续。
- `extend(生成器)` 只把满足条件的仓库加入列表；最后用列表推导式整理成要输出的形状。
- 仓库没有 star 时 `stargazers_count` 是 `0`；`> 0` 过滤掉它们。

## 3. 限流与礼貌

- 未带 token 的 GitHub API 限额约 **60 次/小时**；`octocat` 的仓库远不到 100 个，一两页就结束，安全。
- 别在测试时对超大用户写无限翻页循环——每页都消耗配额。
- `Accept: application/vnd.github+json` 是 GitHub 建议的请求头；正式调用加 `Authorization: Bearer <token>` 可提到 5000 次/小时。

## 4. 易错点清单

1. **忘 `resp.json()`**：直接对 Response 对象遍历/取下标，报错。
2. **分页条件写反**：`len(batch) < 100` 才停；写成 `> 100` 会死循环（单页最多 100）。
3. **`language` 为 null 时 KeyError**：字段存在但值是 null 不会 KeyError，但直接存 None 没问题；用 `.get()` 更稳。
4. **per_page 超出 API 上限**：GitHub 最多 100，写 1000 会被忽略或报错。
5. **不检查状态码**：401/403（限流）时把错误 JSON 当正常数据处理。

## 5. 变式练习

- 按 star 降序输出前 10 个（`sorted(..., key=lambda r: r["stars"], reverse=True)`）。
- 把结果连同抓取时间写入 `repos.json`。
- 加 `since=...` 参数体验 GitHub API 的增量拉取。
