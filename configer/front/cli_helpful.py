from copy import deepcopy
from difflib import get_close_matches
from os import path, listdir
from os.path import splitext, join, sep
from re import split, match
from typing import Union

from logsmal import logger
from mg_file.file.helpful import read_file_by_module
from mg_file.file.json_file import JsonFile
from rich.panel import Panel
from rich.tree import Tree

from useconf import PATH_SETTINGS_CONFIGER


def get_path_in_store(fun_name: str):
    """Получим путь к файлу из хранилища"""""
    _f = JsonFile(PATH_SETTINGS_CONFIGER)
    store: dict[str, dict[str, str]] = _f.readFile()
    return store[fun_name]['store']


def dict_to_tree(dict_: dict[str, Union[dict, bool]], tree_: Tree):
    """
    Конвертировать словарь в дерево путей `Rich`

    :param dict_: Входной словарь
    :param tree_: Экземпляр дерева `rich`
    """

    def _self(keys, _tree):
        for _k, _v in keys.items():
            if type(_v) != dict:
                # Добавляем файл
                _tree.add(f'[bright_black]{_k}[/]' if not _v else f'[green]{_k}[/]')

            else:
                # Для того чтобы вернутся на папку назад
                _bk = _tree
                # Добавляем папку
                _tree = _tree.add(f'[yellow]{_k}[/]')
                # Перебираем ключи
                _self(_v, _tree)
                # Возвращаемся на папку назад
                _tree = _bk

    _self(dict_, tree_)
    return tree_


def get_path_in_store_from_name_file(name_file: str, func_name: str):
    """
    Получить полный путь к файлам из хранилища

    :param name_file:
    :param func_name:
    :return:
    """
    # Получим путь из хранилища
    store_path: str = get_path_in_store(func_name)
    # Получить полный путь к файлу
    path_conf: str = join(store_path, f"{name_file}.py")

    # Если такой файл существует
    if path.exists(path_conf):
        return path_conf

    else:
        # Если такого файла не существует
        logger.error("Файл не существует: {0}\nВозможно вы имели ввиду: {1}".format(
            path_conf,
            get_close_matches(
                name_file,
                [
                    x.replace('.py', '')
                    for x in listdir(f"{store_path}{sep}")
                    if x.endswith('.py')
                ]
            )
        ), flag=func_name)
        exit(0)


name_in_store_ttext = (
    ('name_in_store',),
    dict(
        required=True,
        type=str,
        callback=lambda *args: get_path_in_store_from_name_file(name_file=args[2], func_name='ttext')
    )
)
name_in_store_tcode = deepcopy(name_in_store_ttext)
name_in_store_tcode[1]['callback'] = lambda *args: get_path_in_store_from_name_file(
    name_file=args[2],
    func_name='tcode'
)

nice_ = (
    ('nice', '-n', '--nice'),
    dict(required=False, is_flag=True, default=True)
)

type_file = (
    ('type_file', "-t", "--type_file"),
    {
        'required': False,
        'help': "Требуемое(ые) расширение(я) файла для проверки",
        'type': str,
        'callback': lambda *args: set(split(', | ', args[2]))
    }
)
name_command_ = (
    ('name_command',),
    {
        "nargs": 1,
        "type": str,
    }
)


def help_name_file_in_store(
        name_in_store_regex: str,
        _fun_name: str,
) -> tuple[list[Panel], str]:
    """
    Получить подсказку о доступных модулях  в хранилище

    :param name_in_store_regex: Шаблон Имя файла в хранилище
    :param _fun_name: Имя функции
    :return: Список панелей которые можно вывести через консоль `rich`, Полный путь к хранилищу
    """
    # Путь к хранилищу
    store_path: str = get_path_in_store(_fun_name)
    # Получить имена модулей и их документацию
    paths_in_store: list[Panel] = [
        Panel(
            # Документация у модуля
            f"[green]{read_file_by_module(path.join(store_path, _path)).__doc__}[/]",
            # Имя модуля
            border_style='yellow',
            title=_path,
            expand=False
        )
        for _path in listdir(store_path)
        # Если это файл,
        if path.isfile(path.join(store_path, _path))
           # Его расширение `.py`
           and _path.endswith('.py')
           # Он соответствует регулярному выражению
           and match(f"{name_in_store_regex}", _path)
    ]
    # Отобразить имена модулей и их документацию
    return paths_in_store, store_path


def recursive_folder_iteration(_insert_file: str, _type_file: set[str]) -> list[str]:
    """
    Если путь указывает на папку, то перебрать все файлы которые в ней находятся.
    Взять файлы, которые имеют расширение ``type_file``

    :param _insert_file: Путь к папке
    :param _type_file: Множество доступных расширений для файлов
    :return:
    """
    paths: list[str] = []
    if path.isdir(_insert_file):
        for _file in listdir(_insert_file):
            if splitext(_file)[1][1:] in _type_file:
                paths.append(_file)
    else:
        paths.append(_insert_file)
    return paths
