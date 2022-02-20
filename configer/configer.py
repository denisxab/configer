from os import path
from re import sub, findall

from mg_file.file.txt_file import TxtFile

from helper import logger


class ConfFile:
    """
    Класс для работы с файлом конфигурации
    """
    #: Спец символы для вставки значения по ключу
    split_regx: tuple[str, str] = ("\$\$\(", "\)\$\$")

    @classmethod
    def __new__(cls,
                file_name: str,
                path_out: str,
                template: str,
                kwargs: dict[str, str]):
        """


        :param file_name: Имя файла который будет создам
        :param path_out: Путь куда поместить этот файл
        :param template: Шаблон
        :param kwargs: Словарь для заменой значений в шаблона
        """
        logger.info(f"{file_name}", flag="TEMPLATE")
        template: str = cls.parse_template(template, kwargs)
        _path: str = path.join(path_out, file_name)
        TxtFile(_path, type_file=".py").writeFile(template)
        logger.info(_path, flag="FILE_WRITE")

        return None

    @classmethod
    def parse_template(cls, template: str, kwargs: dict[str, str]) -> str:
        """
        :param template: Текст с ключевыми словами
        :param kwargs: ключи
        :return: Отформатированный текст
        """
        # Получить ключевые слова из текста
        re_obj = findall(f"{cls.split_regx[0]}([\w\d]+){cls.split_regx[1]}", template)
        logger.info(re_obj, flag="FIND")
        # Заменить ключевые слова из текста на те которые передали в метод
        for _key in re_obj:
            var: str = str(kwargs[_key])
            template: str = sub(f"{cls.split_regx[0]}{_key}{cls.split_regx[1]}", var, template)
        return template
