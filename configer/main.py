from os.path import splitext

from click import argument, command

from configer import read_file_by_module, ConfFile
from helper import logger


@command()
@argument('infile', nargs=1)
def parse_conf(infile):
    """
    @param infile: Путь к файлу конфигураций
    """
    if splitext(infile)[1] != ".py":  # Проверяем расширение файла
        raise ValueError(f"Файл должен иметь расширение .py")
    __module = read_file_by_module(infile)
    # Получить переменные из файла конфигурации, отсеиваем магические методы и переменные
    for _var in __module.__dict__["export_var"]:
        logger.info(_var[0], flag="VAR")
        ConfFile(*_var)


if __name__ == '__main__':
    parse_conf()
