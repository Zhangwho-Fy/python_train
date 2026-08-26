# 00 环境与工具

目标：能运行一个 `.py` 文件，能装第三方包，能交互式试语法。

## 1. Python 版本

系统现在自带 Python 3.8。前 4 个阶段跑得动，但 **LangChain 需要 3.9+（推荐 3.10~3.12）**，所以建议一步到位。

推荐用 `uv` 管理版本和虚拟环境（比 pyenv + pip 简单得多）：

```bash
# 安装 uv（Linux/macOS）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 装一个受控的 Python 版本
uv python install 3.12
```

不想装 uv 也行：去 python.org 装 3.12，后面用 `python3 -m venv .venv` 建虚拟环境。

## 2. 跑起来

```bash
# 交互式试语法（最常用）
python3 -i

# 跑脚本
python3 01-basics/exercises/ex1_hello.py

# 建虚拟环境 + 装依赖（用到时再装）
python3 -m venv .venv
source .venv/bin/activate
pip install -r 07-web-scraping/requirements.txt   # 举例
```

如果用 uv：

```bash
uv venv --python 3.12
uv pip install -r 07-web-scraping/requirements.txt
```

## 3. 编辑器

VS Code + Python 扩展（Pylance）即可。Pylance 的类型提示对 C++ 出身的人非常友好——类型写错会在编辑期标红。

## 4. 国内网络

pip 慢就加清华镜像：

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
```

## 5. 本阶段验收

- [x] `python3 -i` 里能算出 `2 ** 10`
- [x] 能运行并理解 `01-basics/exercises/ex1_hello.py`
- [x] 知道 `print()`、`input()`、`len()`、`type()` 大概在干嘛
