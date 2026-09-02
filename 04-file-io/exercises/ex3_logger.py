"""ex3: 手写 logger + logging 模块对比。"""
from datetime import datetime


def log(level: str, message: str, filename: str = "app.log") -> None:
    # TODO: 拼 "[时间] [级别] 消息"，print 一份、追加写文件一份
    pass


def setup_logging(filename: str = "app.log"):
    # TODO: 用 logging.basicConfig 配同样格式，返回 logger
    import logging
    return logging.getLogger(__name__)


def main() -> None:
    log("INFO", "手写 logger 启动")
    log("ERROR", "发生了一个错误")

    logger = setup_logging()
    logger.info("logging 模块启动")
    logger.error("logging 模块错误")


if __name__ == "__main__":
    main()
