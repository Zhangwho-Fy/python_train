"""ex3 参考答案。"""
import requests


def starred_repos(username: str) -> list:
    repos = []
    page = 1
    while True:
        resp = requests.get(
            f"https://api.github.com/users/{username}/repos",
            params={"per_page": 100, "page": page},
            timeout=15,
        )
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        for r in batch:
            if r["stargazers_count"] > 0:
                repos.append(
                    {
                        "name": r["name"],
                        "language": r.get("language"),
                        "stars": r["stargazers_count"],
                    }
                )
        page += 1
    return repos


def main() -> None:
    for repo in starred_repos("octocat"):
        print(f"{repo['name']} | {repo.get('language')} | ★{repo['stars']}")


if __name__ == "__main__":
    main()
