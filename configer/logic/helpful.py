from enum import Enum
from re import finditer, sub

from logsmal import logger
from pydantic import BaseModel

from re_helpful import SPLIT_REGX_END, SPLIT_REGX_START


class spec_name(Enum):
    """
    Специальные(Зарезервированные) имена переменных

    Шаблон файла с конфигурациями
    """
    #: :meth:`useconf.export_var`
    EXPORT_PATH = list[tuple[str, str, str, dict[str, str], bool]]
    #: :meth:`useconf.export_code`
    EXPORT_COMMAND = dict[str, tuple[dict[str, str], dict[str, str]]]
    #: :meth:`useconf.export_template`
    EXPORT_TEMPLATE = dict[str, tuple[str, dict[str, str]]]


def parse_template(template: str, kwargs: dict[str, str]) -> str:
    """
    Заменить шаблонные слова на ключи

    :param template: Текст с ключевыми словами
    :param kwargs: Словарь с заменой
    :return: Отформатированный текст


    >>> parse_template("Привет $$(слово)$$",{"слово":"мир"})
    'Привет мир'
    """
    # Получить ключевые слова из текста
    for _key in finditer(f"{SPLIT_REGX_START}(?P<key>[\w\d_]+){SPLIT_REGX_END}", template):
        _key = _key.group('key')
        logger.info(_key, flag="FIND")
        # Заменить ключевые слова из текста на те которые передали в метод
        template = sub(
            f"{SPLIT_REGX_START}{_key}{SPLIT_REGX_END}",
            str(kwargs[_key]),
            template
        )
    return template


class StoreStruct(BaseModel):
    """
    Структура для хранения настроек
    StoreStruct().dict()
    """
    ttext: str = {"store": ''}
    tcode: str = {"store": ''}
