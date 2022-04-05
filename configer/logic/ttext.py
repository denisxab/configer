from difflib import get_close_matches
from re import finditer, sub
from typing import Optional, Union

from logsmal import logger
from mg_file.file.helpful import read_file_by_module

from re_helpful import SPLIT_REGX_END, SPLIT_REGX_START
from useconf import ttext_func
from .helpful import parse_template, spec_name


class KeyErrorTtext(KeyError): ...


class ttextLogic:
    """
    :doc:`ttext <./ttext>`
    """

    @classmethod
    def ttext(
            cls,
            name_command: str,
            overload_kwargs: dict[str, str],
            path_conf: str
    ) -> Union[tuple[bool, str, list[str]], tuple[bool, str]]:
        return cls._parse_module(name_command, overload_kwargs, path_conf)

    @classmethod
    def _parse_module(
            cls,
            name_command: str,
            overload_kwargs: dict[str, str],
            path_conf: str
    ) -> Union[tuple[bool, str, list[str]], tuple[bool, str]]:
        """

        :param name_command:
        :param overload_kwargs:
        :param path_conf:
        :return:
        """
        # Читаем модуль
        module = read_file_by_module(path_conf)
        # Находим команду в модуле, и выполняем основную логику
        try:
            return cls._parse_export(overload_kwargs, *module.__dict__[spec_name.EXPORT_TEMPLATE.name][name_command])
        except KeyError:
            # Если ключа не существует, то подлегаем возможные ключи
            logger.error("Команды не существует: {0}\nВозможно вы имели ввиду: {1}".format(
                name_command,
                get_close_matches(
                    name_command, list(module.__dict__[spec_name.EXPORT_TEMPLATE.name].keys())
                )),
                flag=cls._parse_module.__name__
            )
            raise KeyErrorTtext

    @classmethod
    def _parse_export(
            cls,
            overload_kwargs: dict[str, str],
            template: str,
            kwargs: dict[str, str],
            func_dict: Optional[dict[str, ttext_func]],
    ) -> Union[tuple[bool, str, list[str]], tuple[bool, str]]:
        """
        :param overload_kwargs: Переопределяемые ключи
        :param template:Шаблон
        :param kwargs: Словарь для замены из конфигурации
        :param func_dict: Словарь с функциями
        :return:
        """
        # Переопределяем ключи
        kwargs.update(overload_kwargs)
        # Если `{"ключ":None}` не переопределен, то запрашиваем переопределение у пользователя
        res: list = [_k for _k, _v in kwargs.items() if _v is None]
        if res:
            return False, template, res
        else:
            return True, cls._parse_template(template, kwargs, func_dict)

    @classmethod
    def _parse_template(
            cls,
            template: str,
            kwargs: dict[str, str],
            func_dict: Optional[dict[str, ttext_func]]
    ) -> str:
        """
        Заменить шаблонные слова на ключи

        :param template: Текст с ключевыми словами
        :param kwargs: Словарь спфв заменой
        :param func_dict: Пользовательские функции
        :return: Отформатированный текст
        """
        # Заменяем функции
        for _find in finditer(
                f"{SPLIT_REGX_START}(?P<key>[\w\d_]+)\|(?P<func>[\w\d_]+){SPLIT_REGX_END}",
                template):
            _key: str = _find.group('key')
            logger.info(_key, flag="FIND_KEY")
            _func = _find.group("func")
            logger.info(_func, flag="FIND_FUNC")
            # Выполняем пользовательскую функцию
            _replay_key: str = func_dict[_func](text=str(kwargs[_key]), kwargs=kwargs, template=template)
            # Создаем ключ вмести с функцией (Экранируем вертикальную черту)
            _key = f'{_key}\|{_func}'
            # Заменить ключевые слова из текста на те которые передали в метод
            template = sub(
                f"{SPLIT_REGX_START}{_key}{SPLIT_REGX_END}",
                _replay_key,
                template
            )
        return parse_template(template, kwargs)
