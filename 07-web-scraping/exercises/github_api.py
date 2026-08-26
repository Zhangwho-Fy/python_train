"""ex3: 列出用户 star>0 的仓库。"""


def starred_repos(username: str) -> list:
    # TODO: 逐页请求 repos?per_page=100&page=N，收集 stargazers_count > 0
    return []


def main() -> None:
    for repo in starred_repos("octocat"):
        print(f"{repo['name']} | {repo.get('language')} | ★{repo['stars']}")


if __name__ == "__main__":
    main()
