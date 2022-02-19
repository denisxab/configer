import re

import click
from click import argument, command
from mg_file.file.base_file import read_file_by_module, BaseFile
from mg_file.file.txt_file import TxtFile

from configer import ConfFile
from helper import logger


# Создаем группу
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
        logger.info(_var[0], flag="VAR")
        ConfFile(*_var)


@command(help="Создать копию конфигураций но скрыть значения переменных указанных в `hide_var`")
@argument('infile', nargs=1, type=click.Path(dir_okay=False, exists=True))
def hideconf(infile):
    """
    @param infile: Путь к файлу конфигураций
    """
    # re.sub("[\s]*[\w\d]+[\s]*=[\s]*([\w\d])","___",__text_conf)
    # re.sub(r"""[\s]*[\w\d_]+[\s]*=[\s]*[\w\d_'"]+\n""","\1___", __text_conf)
    # re.sub(r"""(\s*[\w\d_]+\s*=\s*)[\w\d\s'"\[\]\(\)_.,/]+""","\g<1>___", __text_conf)
    # re.sub(r"""(\s*[\w\d_]+\s*=\s*)[\w\d\s'"]+(\n+)""","\g<1>___\g<2>", __text_conf)
    #
    # re.sub(r"""(\s*[\w\d_]+\s*=\s*)[\w\d\s'",._/\(\)\[\]#]+(\n+)""","\g<1>___\g<2>", __text_conf)
    # re.sub(r"""(\s*[\w\d_]+\s*=\s*)[\w\d\s'",._/\(\)\[\]\{\}#$:]+(\n+)""","\g<1>___\g<2>", __text_conf)
    # re.sub(r"""(\s*[\w\d_]+\s*=\s*)[\w\d\s'",._/\(\)\[\]\{\}#$:]+(\n+)""","\g<1>___\g<2>", __text_conf)
    #
    # re.sub(r"""(\s*[\w\d_]+\s*=\s*)[\w\d\s'",._/\(\)\[\]\{\}#$:]+(\n+)""","\g<1>___\g<2>", __text_conf)

    ## re.sub(r"""(\s*[\w\d_]+\s*=\s*)[\(\[\{][\w\W]*[\)\]\}]""","\g<1>___", __text_conf)

    ## re.sub(r"""(\s*[\w\d_]+\s*=\s*)(?:[\(\[\{][\w\W]*[\)\]\}]|[\w\d\s'",._]+)(\n+)""","\g<1>___", __text_conf)
    st = """(\s*[\w\d_]+\s*=\s*)"""
    tm = """[\w\d\s'",._/\(\)\[\]\{\}#$:]+"""
    en = """(\n+)"""
    rp = "\g<1>___\g<2>"

    __text_conf = TxtFile(infile, type_file=".py").readFile()

    re.sub("""{0}{1}{2}""".format(st, tm, en), rp, __text_conf)

    __module = read_file_by_module(infile)
    # Получить переменные из файла конфигурации, отсеиваем магические методы и переменные
    for _var in __module.__dict__["hide_var"]:
        logger.info(_var[0], flag="VAR")

        # ConfFile(*_var)


# Добавляем в группу команду
main_group.add_command(parseconf)
# Добавляем в группу команду
main_group.add_command(hideconf)

if __name__ == '__main__':
    main_group()
