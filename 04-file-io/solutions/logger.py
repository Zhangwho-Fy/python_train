"""ex3 参考答案。"""
from datetime import datetime
from pathlib import Path


def log(level: str, message: str, filename: str = "app.log") -> None:
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] [{level}] {message}"
    print(line)
    with Path(filename).open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def setup_logging(filename: str = "app.log"):
    import logging

    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename, encoding="utf-8")
    handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(handler)
    return logger


def main() -> None:
    here = Path(__file__).parent
    log("INFO", "手写 logger 启动", filename=str(here / "app.log"))
    log("ERROR", "发生了一个错误", filename=str(here / "app.log"))

    logger = setup_logging(str(here / "app.log"))
    logger.info("logging 模块启动")
    logger.error("logging 模块错误")


if __name__ == "__main__":
    main()
