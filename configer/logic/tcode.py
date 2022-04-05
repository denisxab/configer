from dataclasses import dataclass
from enum import Enum
from re import sub, search, finditer, escape, Match
from typing import NamedTuple, Literal, Union

from logsmal import logger
from mg_file import BaseHash, read_file_by_module

from re_helpful import SPLIT_REGX_END, SPLIT_REGX_START
from .helpful import spec_name, parse_template


class format_insert_complete_code(Enum):
    """
    Шаблон форматирования кода для различных языков

    Доступные спец имена посмотрите в :meth:`allowed_format_tcod.__new__`

    :Рекомендую:

        - Это должен быть однострочный комментарий
        - Обязательно укажите начало({HEAD}) и конец({TAIL})

    """

    py = "# {HEAD}\n{DATA}\n# {TAIL}"
    cpp = "// {HEAD}\n{DATA}\n// {TAIL}"
    js = cpp


class ParseCodeBlock(NamedTuple):
    """
    Структура для хранения блока с кодом
    """

    @dataclass
    class head_:
        name_command: str = ''
        lang: str = ''

        def parse(self, text: str):
            """Получить данные из заголовка"""
            self.name_command, self.lang = [sub(' ', '', x) for x in text.split(":")]

            return self

        def __str__(self):
            """Создать шапку блока с кодом"""
            return "{START} {NAME}:{LANG}".format(
                # Убираем экранирование
                START=allowed_format_tcod.START.replace('\\', ""),
                NAME=self.name_command,
                LANG=self.lang,
            )

    @dataclass
    class data_:
        text: str = ''

        def parse(self, text=""):
            self.text = text
            return self

        def __str__(self):
            return self.text

    @dataclass
    class tail_:
        hash: str = ''

        def parse(self, text: str, raw_data):
            """Получить данные из концовки"""
            _hash = BaseHash.text(raw_data)
            if _hash != text:
                logger.info(f"{text}", flag="Хеш устарел")
            self.hash = _hash
            return self

        def __str__(self):
            """
            Создать концовку блока с кодом

            :var HASH: Хеш сумма вычитывается без учета заголовка и концовки
            """
            return "{END} {HASH}".format(
                # Убираем экранирование
                END=allowed_format_tcod.END.replace('\\', ""),
                HASH=self.hash,
            )

    head: head_
    data: data_
    tail: tail_

    def __str__(self):
        """Отрендерить готовый блок с кодом"""
        return format_insert_complete_code[self.head.lang].value.format(
            HEAD=self.head,
            DATA=self.data,
            TAIL=self.tail
        )


class allowed_format_tcod:
    """
    Форматирование готового кода.
    """

    #: ! Нужно экранировать спец символы для регулярных выражений
    START: str = "\$\$\(START\)\$\$"
    #: ! Нужно экранировать спец символы для регулярных выражений
    END: str = "\$\$\(END\)\$\$"

    def __new__(
            cls,
            template_lange_program: format_insert_complete_code,
            text: str,
            _name_command: str,
            _lang: str,
    ) -> ParseCodeBlock:
        """

        :param template_lange_program: Шаблон форматирования :meth:`format_insert_complete_code`
        :param text: Готовый код (Полезные данные)

        :param _lang: Язык на котором написан код
        :param _name_command: Имя шаблонного кода
        """
        return ParseCodeBlock(
            head=ParseCodeBlock.head_(name_command=_name_command, lang=_lang),
            data=ParseCodeBlock.data_(text=text),
            tail=ParseCodeBlock.tail_(hash=BaseHash.text(text))
        )


class tcodeLogic:
    """
    :doc:`tcode <./tcode>`
    """

    @classmethod
    def print(cls, name_command: str, lang: str, _path_conf: str):
        """
        Вернуть готовый блок с кодом

        :param name_command:
        :param lang:
        :param _path_conf:
        :return:
        """

        return str(cls._parse_module(name_command, lang, _path_conf))

    @classmethod
    def infile(cls, insert_text: str, _path_conf: str):
        """
        Вставить в текст готовые блоки с кодом

        :param insert_text:
        :param _path_conf:
        :return:
        """
        for _x in finditer(
                f"{SPLIT_REGX_START}(?P<name_command>[\w\d_]+):(?P<lang>[\w\d_]+){SPLIT_REGX_END}",
                insert_text
        ):
            name_command = _x.group('name_command')
            lang = _x.group('lang')
            _replace_key = cls.print(name_command=name_command, lang=lang, _path_conf=_path_conf)
            insert_text = sub(
                f"{SPLIT_REGX_START}{name_command}:{lang}{SPLIT_REGX_END}",
                _replace_key,
                insert_text
            )

        return insert_text

    @classmethod
    def upfile(cls, from_update_text: str, _path_conf: str) -> str:
        """
        Обновить текст если хеш отличается от готового кода

        :param from_update_text:
        :param _path_conf:
        :return:
        """

        _infile: dict[str, ParseCodeBlock] = cls._parse_file(from_update_text)
        for _command in _infile.keys():
            new_code: ParseCodeBlock = cls._parse_module(
                _infile[_command].head.name_command,
                _infile[_command].head.lang, _path_conf
            )

            if _infile[_command].tail.hash != new_code.tail.hash:
                logger.info(f'{_infile[_command].tail.hash}!={new_code.tail.hash}', flag="HASH_DIFF")
                # Заменяем отличившееся по хешу блок кода
                from_update_text = sub("%s" % escape(str(_infile[_command].data)), str(new_code.data),
                                       from_update_text)

        return from_update_text

    @staticmethod
    def _parse_file(from_update_text: str) -> dict[str, ParseCodeBlock]:
        """
        Распарсить текст и найти блоки с кодом

        :param text:

        :return: {ИмяКоманды:ДанныеБлока}
        """
        res: dict[str, ParseCodeBlock] = {}
        for _x in finditer(
                "%s(?P<head>[\w\s\d:]+)\n(?P<data>[\w\W]+)\n+[\w\W^\n]+%s(?P<tail>[\w\d ]+)" %
                (allowed_format_tcod.START, allowed_format_tcod.END),
                from_update_text
        ):
            tmp = ParseCodeBlock(
                head=ParseCodeBlock.head_().parse(_x.group('head')),
                data=ParseCodeBlock.data_().parse(_x.group("data")),
                tail=ParseCodeBlock.tail_().parse(_x.group('tail'), _x.group("data")),
            )
            res[tmp.head.name_command] = tmp
        return res

    @classmethod
    def _parse_module(cls, name_command: str, lang: str, _path_conf: str) -> ParseCodeBlock:
        """
        :param name_command:
        :param lang:
        :param _path_conf:
        :return:
        """
        # Читаем модуль
        module = read_file_by_module(_path_conf)
        # Находим команду в модуле, и выполняем основную логику
        return cls._parse_export(name_command, lang, *module.__dict__[spec_name.EXPORT_COMMAND.name][name_command])

    @classmethod
    def _parse_export(
            cls,
            name_command,
            lang: str,
            template_lange: dict[str, str],
            kwargs: dict[str, str],
    ) -> ParseCodeBlock:
        """
        :param name_command:
        :param lang:
        :param template_lange:
        :param kwargs:
        :return:
        """
        logger.info(lang, flag='SELECT_LANG')
        # Выбираем шаблон по указанному имени ЯП
        template: str = template_lange[lang]
        build_code = cls._parse_template(template, kwargs, lang)
        return allowed_format_tcod(format_insert_complete_code[lang].value, build_code, name_command, lang)

    @classmethod
    def _parse_template(
            cls,
            template: str,
            kwargs: dict[str, Union[str, tuple[dict[Literal["in", "out"], str]]]],
            lang: str
    ) -> str:
        """

        :param template:
        :param kwargs:
        :param lang:
        :return:
        """
        # Находим сколько отступов у теста, для того чтобы его соблюсти
        iftest: Match = search(
            f"(?P<padding>[\t ]*){SPLIT_REGX_START}TEST{SPLIT_REGX_END}",
            template)
        if iftest:
            padding: int = len(iftest.group('padding'))
            logger.info(iftest, flag="FIND_TEST")
            _replay_key: str = cls._compile_tests(args=kwargs['TEST'], padding=padding, lang=lang)
            template = sub(
                f"{SPLIT_REGX_START}TEST{SPLIT_REGX_END}",
                _replay_key,
                template
            )
        template: str = parse_template(template, kwargs)
        return template

    @classmethod
    def _compile_tests(cls, args: tuple[dict[Literal["in", "out"], str], ...], padding: int, lang: str) -> str:
        """
        Создать авто тестов

        :param args:
        :param lang:
        :return:
        """

        def _py(_args, _padding):
            _res = ''
            for _test in _args:
                _res += "{0}>>> {1}\n{0}{2}\n".format(" " * _padding, _test['in'], _test['out'])
            # Убираем отступы в начале
            return _res[_padding:]

        res = ""
        match lang:
            case 'py':
                res = _py(args, padding)
        return res
