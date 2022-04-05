import datetime
import os.path
from os import path
from os.path import exists
from re import search, split, sub, match
from shutil import get_terminal_size
from typing import Union

from click import group, option, argument, command, Path, echo, Choice
from logsmal import logger
from mg_file.file.helpful import absolute_path_dir, read_file_by_module
from mg_file.file.json_file import JsonFile
from pyperclip import copy
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.tree import Tree

from configer import StoreStruct, spec_name
from front.cli_helpful import \
    name_in_store_ttext, name_command_, \
    recursive_folder_iteration, type_file, \
    name_in_store_tcode, nice_, \
    dict_to_tree, help_name_file_in_store
from logic.hideconf import hideconfLogic
from logic.parseconf import parseconfLogic
from logic.tcode import tcodeLogic
from logic.ttext import ttextLogic, KeyErrorTtext
from re_helpful import SPLIT_REGX_END, SPLIT_REGX_START
from useconf import PATH_SETTINGS_CONFIGER

console_rich = Console()


@group()
def main_group():
    """Менеджер файлов конфигурации"""
    ...


@command(help="Создать конфигурации")
@argument(
    'path_conf',
    default='./conf_parseconf.py',
    nargs=1,
    type=Path(dir_okay=False, exists=True)
)
@option(
    'noautohide', '--noautohide',
    help='Отключить автоматическое создание публичной конфигурации',
    required=False,
    is_flag=True
)
@option(*nice_[0], **nice_[1])
def parseconf(path_conf: str, noautohide: bool, nice: bool):
    """
    :param nice:
    :param noautohide:
    :param path_conf: Путь к файлу конфигураций
    """
    res = parseconfLogic.parseconf(path_conf=path_conf)

    # Не скрывать конфигурацию
    if not noautohide:
        hideconfLogic.hideconf(path_conf=path_conf, outfile='./conf_parseconf_pub.py')

    # Для людей
    if nice:
        tree = Tree(f"[yellow]{os.path.abspath(path_conf)}[/]")
        console_rich.print(
            Panel(
                dict_to_tree(res, tree),
                border_style='bold yellow',
                title=f'[green]{datetime.datetime.now()}[/]',
                expand=False
            ),
        )


@command(help="Создать копию конфигураций но скрыть значения переменных")
@argument(
    'path_conf',
    default='./conf_parseconf.py',
    nargs=1,
    type=Path(dir_okay=False, exists=True)
)
@argument(
    'outfile',
    default='./conf_parseconf_pub.py',
    nargs=1,
    type=Path(dir_okay=False, file_okay=True)
)
def hideconf(path_conf: str, outfile: str):
    """
    :param path_conf: Путь к файлу конфигураций
    :param outfile: Путь для сохранения итогового файла
    """
    hideconfLogic.hideconf(path_conf, outfile)


@command(help="Создать блок кода, и вывести его в консоль")
@argument(*name_in_store_tcode[0], **name_in_store_tcode[1])
@argument(*name_command_[0], **name_command_[1])
@option(
    'langs', "-l", "--langs",
    required=True,
    help="На какие языки собрать шаблон",
    type=str,
    callback=lambda *args: split(', | ', args[2])
)
@option(*nice_[0], **nice_[1])
def tcodp(name_in_store: str, name_command: str, langs: str, nice: bool):
    """
    :param name_in_store:
    :param nice:
    :param name_command: Имя команды
    :param langs: Языки
    """
    if not langs:
        return echo(f"Список языков пуст {langs=}")

    logger.info(langs, "LANG_TCODP")

    copy_text: list[str] = []
    for _lang in langs:
        _tmp = tcodeLogic.print(name_command, _lang, name_in_store)
        # Для людей
        if nice:
            syntax = Syntax(_tmp, _lang, line_numbers=False)
            console_rich.print(syntax)
            copy_text.append(_tmp)
        # Для машин
        else:
            echo(_tmp)

    # Копируем в буфер обмена результат всех языков
    if nice:
        try:
            logger.success("Copy Buffer", 'COPY')
            copy(''.join(copy_text))
        except ImportError:
            logger.warning("Dont copy buffer", 'COPY')


@command(help="Информация по хранилищу текстовых шаблонов")
@argument(
    'name_in_store_regex',
    required=True,
    type=str,
    default='.*',
)
@argument(
    'command_regex',
    required=False,
    type=str,
    default='.*',
)
def tcodh(
        name_in_store_regex: str,
        command_regex: str,
):
    """
    :param name_in_store_regex: Регулярное выражение для поиска файла в хранилище (по умолчанию все)
    :param command_regex: Регулярное выражение для поиска команд в файле (по умолчанию все)
    """

    paths_in_store, store_path = help_name_file_in_store(
        name_in_store_regex,
        _fun_name='tcode',
    )

    for _path in paths_in_store:
        console_rich.print(_path)

    # Если выбран один модуль, то показываем доступные команды, и языки
    if len(paths_in_store) == 1:
        console_rich.print(
            '\n'.join([
                f'- [yellow]{_command}: {", ".join(_langs[0].keys())}[/]'
                for _command, _langs in
                # Получим все команды, и языки на которые можно собрать код
                getattr(
                    read_file_by_module(
                        path.join(store_path, paths_in_store[0].title)
                    ), spec_name.EXPORT_COMMAND.name
                ).items()
                # Вернем только те что соответствуют регулярному выражению
                if match(f"{command_regex}", _command)
            ])
        )


@command(help="Просканировать файл или директорию, найти места для вставки шаблона с кодом")
@argument(*name_in_store_tcode[0], **name_in_store_tcode[1])
@argument(
    'insert_file',
    nargs=1,
    type=Path(dir_okay=True, file_okay=True, exists=True)
)
@option(*type_file[0], **type_file[1])
def tcodi(name_in_store: str, insert_file: str, type_file: set[str]):
    """
    :param type_file:
    :param insert_file:
    :param name_in_store: Путь к файлу конфигураций
    """
    paths = recursive_folder_iteration(insert_file, type_file)
    for _file in paths:
        abs_path = absolute_path_dir(insert_file, 0)
        full_path = path.join(abs_path, _file) if path.isdir(abs_path) else abs_path
        with open(full_path, 'r', encoding='utf-8') as _f:
            text = _f.read()
            finished_code = tcodeLogic.infile(text, name_in_store)
        with open(full_path, 'w', encoding='utf-8') as _f:
            logger.info(finished_code)
            _f.write(finished_code)


@command(help="Обновить блоки кода в указанной папке или директории")
@argument(*name_in_store_tcode[0], **name_in_store_tcode[1])
@argument(
    'path_search',
    nargs=1,
    type=Path(dir_okay=True, file_okay=True, exists=True)
)
@option(*type_file[0], **type_file[1])
def tcodu(name_in_store: str, path_search: str, type_file: set[str], ):
    """
    :param type_file:
    :param path_search:
    :param name_in_store:
    """
    paths = recursive_folder_iteration(path_search, type_file)
    for _file in paths:
        abs_path = absolute_path_dir(path_search, 0)
        full_path = path.join(abs_path, _file) if path.isdir(abs_path) else str(abs_path)
        with open(full_path, 'r', encoding='utf-8') as _f:
            text = _f.read()
            finished_code = tcodeLogic.upfile(text, name_in_store)
        with open(full_path, 'w', encoding='utf-8') as _f:
            logger.info(finished_code)
            _f.write(finished_code)


@command(help="Шаблон для простого текста")
@argument(*name_in_store_ttext[0], **name_in_store_ttext[1])
@argument(*name_command_[0], **name_command_[1])
@option(
    'kwargs', '-k', '--kwargs',
    required=False,
    help="Переопределить ключевые имена",
    type=str,
    multiple=True,
    # Переводим ``ключ=значение`` в ``{"ключ":значение}``
    callback=lambda *args: {
        _k: _v for _k, _v in [
            search('([\w\d_]+)=([\w\W]+)', _x).groups()
            for _x in args[2]
        ]
    }
)
@option(*nice_[0], **nice_[1])
def ttext(
        name_in_store: str,
        name_command: str,
        kwargs: dict[str, str],
        nice: bool,
):
    """
    :param nice: Не задавать вопросов. Используется для плагинов
    :param kwargs:
    :param name_command:
    :param name_in_store: Имя файла из хранилища в котором будет искаться команда
    """

    def _self(_name_command, _kwargs, _path_conf):
        response_text: Union[
            tuple[bool, str, list[str]],
            tuple[bool, str]
        ] = ttextLogic.ttext(
            name_command=_name_command,
            overload_kwargs=_kwargs,
            path_conf=_path_conf
        )
        # Если все шаблон готов, то выводи его в консоль, и копируем в буфер обмена
        if response_text[0]:
            console_rich.print(response_text[1])
            try:
                logger.success("Copy Buffer", 'COPY')
                copy(response_text[1])
            except ImportError:
                logger.warning("Dont copy buffer", 'COPY')

        # Если есть не переопределённые ключи, то запрашиваем их у пользователя, а потом снова собираем шаблон
        else:
            again: dict[str, str] = _kwargs
            # Оформляем текст шаблона
            console_rich.print(
                Panel(
                    sub(
                        f"({SPLIT_REGX_START})([\w\d_|]+)({SPLIT_REGX_END})",
                        '[bright_green]\g<1>\g<2>\g<3>[/]',
                        response_text[1]
                    ),
                    border_style='bright_yellow',
                    title=_name_command,
                    expand=False
                )
            )
            # Запрашиваем ключи для переопределения у пользователя
            for x in response_text[2]:
                k = console_rich.input(f"[u]{x} :::[/] ")
                again[x] = k
            # Декоративна разделительная линия
            console_rich.print("_" * (get_terminal_size((80, 20)).columns))
            # Пробуем собрать шаблон заново
            _self(_name_command=_name_command, _kwargs=again, _path_conf=_path_conf)

    try:
        # Для людей
        if nice:
            _self(name_command, kwargs, name_in_store)
        # Для машин
        else:
            res = ttextLogic.ttext(
                name_command=name_command,
                overload_kwargs=kwargs,
                path_conf=name_in_store
            )
            if res[0]:
                echo(res[1])
            else:
                echo(res[2])
    except KeyErrorTtext:
        pass


@command(help="Информация по хранилищу текстовых шаблонов")
@argument(
    'name_in_store_regex',
    required=True,
    type=str,
    default='.*',
)
@argument(
    'command_regex',
    required=False,
    type=str,
    default='.*',
)
def ttexth(
        name_in_store_regex: str,
        command_regex: str,
):
    """
    :param name_in_store_regex: Регулярное выражение для поиска файла в хранилище (по умолчанию все)
    :param command_regex: Регулярное выражение для поиска команд в файле (по умолчанию все)
    """

    paths, store_path = help_name_file_in_store(
        name_in_store_regex,
        _fun_name=ttext.name,
    )
    for _path in paths:
        console_rich.print(_path)

    # Если выбран один модуль, то показываем доступные команды
    if len(paths) == 1:
        console_rich.print(
            '\n'.join([
                f'- [yellow]{_command}[/]'
                for _command in
                # Получим все команды
                getattr(
                    read_file_by_module(
                        path.join(store_path, paths[0].title)
                    ), spec_name.EXPORT_TEMPLATE.name).keys()
                # Вернем только те что соответствуют регулярному выражению
                if match(f"{command_regex}", _command)
            ])
        )


@command(help="Установить пути к хранилищу")
@argument(
    'cli_command',
    required=True,
    nargs=1,
    type=Choice(['ttext', 'tcode'])
)
@argument(
    'path_store',
    required=True,
    nargs=1,
    type=Path(dir_okay=True, file_okay=False)
)
def storeset(path_store: str, cli_command: str):
    """
    :param path_store: Путь к хранилищу
    :param cli_command: Для какой команды
    """

    def _update_store(_file, _pathstore):
        store = _file.readFile()
        store[cli_command]['store'] = _pathstore
        _file.writeFile(store)

    # Отображаем путь к конфигурации
    echo(PATH_SETTINGS_CONFIGER)
    file = JsonFile(PATH_SETTINGS_CONFIGER)
    # Если конфигурации не существует, то заполняем её шаблоном
    if not exists(PATH_SETTINGS_CONFIGER):
        file.writeFile(StoreStruct().dict())
    # Обновляем путь в хранилище
    _update_store(file, path_store)
    echo(file.readFile())


@command(help="Показать данные из хранилища")
def storeh():
    file = JsonFile(PATH_SETTINGS_CONFIGER).readFile()
    console_rich.print(file)


def main():
    # Добавляем в группу команду
    main_group.add_command(parseconf)
    main_group.add_command(hideconf)
    #
    main_group.add_command(tcodh)
    main_group.add_command(tcodp)
    main_group.add_command(tcodi)
    main_group.add_command(tcodu)
    #
    main_group.add_command(ttexth)
    main_group.add_command(ttext)
    #
    main_group.add_command(storeset)
    main_group.add_command(storeh)
    # Создаем команды
    main_group()
