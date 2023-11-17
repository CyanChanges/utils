import inspect
import logging
import os


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        logger = __import__("loguru").logger

        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def install():
    import random
    if os.getenv("SNG_INT"):
        random.randint = lambda m, m2: int(os.getenv("SNG_INT"))
    if os.getenv("SNG_RND"):
        random.random = lambda: int(os.getenv("SNG_RND"))

    if os.getenv("USE_LOGURU"):
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
        o_getLogger = logging.getLogger
        logging.getLogger = \
            lambda n: (
                o_getLogger(n).handlers.clear(),
                o_getLogger(n).handlers.append(InterceptHandler()),
                o_getLogger(n)
            )[2]
