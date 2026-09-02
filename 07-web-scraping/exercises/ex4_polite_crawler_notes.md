# ex4 polite_crawler 考点详解

## 题目回顾

写 `fetch_with_retry(url, retries=3)`：失败后等 `2 ** attempt` 秒再试；再写 `crawl(urls)`：逐个抓取、每次间隔 1 秒、带浏览器 UA。

## 考点总览

| 考点 | 一句话 | 本题用法 |
| --- | --- | --- |
| 指数退避重试 | 第 n 次失败后等 `2 ** n` 秒 | 瞬时故障自己恢复 |
| `requests.RequestException` | 网络异常的统一父类 | 捕获超时/连接错误 |
| 自定义 User-Agent | 请求头伪装浏览器 | 被拒率大降 |
| `time.sleep(1)` | 控制抓取频率 | 别把站点打爆 |
| `for attempt in range(retries)` | 固定次数重试 | 最后一次仍失败则抛出 |
| 抓取礼仪 | robots.txt / 限速 / 重试 | 面试加分点 |

## 1. 指数退避重试

```python
import time
import requests

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

def fetch_with_retry(url: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            resp = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": UA},
            )
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            print(f"第 {attempt + 1} 次失败: {e}")
            if attempt == retries - 1:      # 最后一次也失败
                raise
            time.sleep(2 ** attempt)        # 等 1s、2s、4s...
    return ""
```

- `attempt` 从 0 开始：失败第一次等 `2**0=1` 秒，第二次 `2` 秒，第三次 `4` 秒——指数退避，给服务端喘息时间。
- `requests.RequestException` 是超时、连接错误等**网络异常**的公共父类，一个 `except` 全接住；HTTP 状态错误由 `raise_for_status()` 抛出（它是 HTTPError，也是 RequestException 子类）。
- 最后一次失败要 `raise` 重新抛出，让调用方知道“彻底失败了”，而不是静默返回空。

## 2. 限速抓取

```python
def crawl(urls: list) -> None:
    for url in urls:
        try:
            text = fetch_with_retry(url)
            print(f"OK {url} ({len(text)} bytes)")
        except requests.RequestException as e:
            print(f"FAIL {url}: {e}")
        time.sleep(1)       # 每两个请求之间至少隔 1 秒
```

- `time.sleep(1)` 控制频率：一次性并发打 100 个请求会把小站点打挂，还可能被 ban。
- 题目样例 `crawl(["https://example.com", "https://example.org"])` 两个请求，间隔 1 秒，很快跑完。

## 3. 抓取礼仪（面试常问）

- 先看目标站点的 `robots.txt` 和 ToS，确认允许抓取；
- 设置能识别身份的 UA，带上 `timeout`；
- 失败指数退避重试，成功之间限速；
- 不做无上限的并发，不抓需要登录的数据。

## 4. 易错点清单

1. **重试时 `2 ** attempt` 写成 `attempt ** 2`**：退避变成 0、1、4，第一次不等待。
2. **最后一次失败不 re-raise**：上层永远不知道失败，日志全是“空结果”。
3. **`raise_for_status` 放在 try 外**：4xx/5xx 不被重试逻辑覆盖。
4. **忘记 `timeout`**：一个挂死的连接会拖住整个爬虫。
5. **没有 UA 或 UA 太假**：很多站点直接 403；requests 默认 UA 容易被拦。

## 5. 变式练习

- 加抖动（jitter）：`time.sleep((2 ** attempt) + random.uniform(0, 0.5))`，避免所有重试者同拍。
- 把 retries 改成按 `Retry-After` 响应头等待（尊重服务端指示）。
- 给 `crawl` 加 `max_workers=2` 的并发但总限速（08 阶段学 asyncio 后可回来重写）。
