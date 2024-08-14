import logging


def setup_logger(name: str, level: str) -> logging.Logger:
    """Настройка логгера.

    Аргументы:
        – name: имя логгера;
        – level: уровень вывода;

    Возвращаемое значение:
        – логгер.
    """
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - [%(module)s:%(filename)s:%(funcName)s:%(lineno)d] %(message)s",
        "%d.%m.%Y %H:%M:%S",
    )
    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.handlers = []

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
