from typing import Union

import click
from click import argument, command
from mg_file.file.base_file import read_file_by_module, BaseFile, absolute_path_dir
from mg_file.file.txt_file import TxtFile

from configer import ConfFile
from helper import logger
# Создаем группу
from hidiger import HiddenVar


@click.group()
def main_group():
    """Менеджер файлов конфигурации"""
    ...


@command(help="Прочитать файл, и создать конфигурации указанные в `export_var`")
@argument('infile', nargs=1, type=click.Path(dir_okay=False, exists=True))
def parseconf(infile):
    """
    @param infile: Путь к файлу конфигураций
    """
    BaseFile.check_extensions_file(infile, ".py")
    __module = read_file_by_module(infile)
    # Получить переменные из файла конфигурации, отсеиваем магические методы и переменные
    for _var in __module.__dict__["export_var"]:
        ConfFile(*_var)
        logger.info(_var[0], flag="VAR_CREATE")


@command(help="Создать копию конфигураций но скрыть значения переменных указанных в `hide_var`")
@argument('infile', nargs=1, type=click.Path(dir_okay=False, exists=True))
@click.option('outfile', "-o", "--outfile",
              default=None,
              show_default="Там же где исходный файл конфигураций",
              type=click.Path(dir_okay=False, file_okay=True))
def hideconf(infile: str, outfile: str):
    """
    @param infile: Путь к файлу конфигураций
    @param outfile:
    """
    # Получаем исходный текст конфигурации
    __text_conf: str = TxtFile(infile, type_file=".py").readFile()
    # У переменных которые необходимо скрыть, удаляем значения.
    # По умолчанию, для того чтобы пометить переменную, что её нужно скрыть
    # нужно написать в начале её `_hide_`
    __text_conf_rm: dict[str, Union[str, list[str]]] = HiddenVar(__text_conf)
    # Записываем новые текст со скрытыми значениями в файл
    TxtFile(outfile
            if outfile
            else absolute_path_dir(infile) / "conf_pub.py",
            type_file=".py").writeFile(__text_conf_rm["source_text"])
    # Логи
    for _x in __text_conf_rm["res_find_var"]:
        logger.info(_x, flag="VAR_HIDE")


# Добавляем в группу команду
main_group.add_command(parseconf)
# Добавляем в группу команду
main_group.add_command(hideconf)

if __name__ == '__main__':
    main_group()
