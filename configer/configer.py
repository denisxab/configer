"""
Программа для создания файлов конфигураций
"""
from os import path
from re import sub, findall

from helper import logger


class ConfFile:
    """
    .
    """
    # Спец символы для вставки значения по ключу
    split_regx: tuple[str, str] = ("\$\$\(", "\)\$\$")

    def __init__(self,
                 file_name: str,
                 path_out: str,
                 template: str,
                 kwargs: dict[str, str]):
        logger.info(f"{file_name}", flag="TEMPLATE")
        self.template: str = self.parse_template(template, kwargs)
        self.writeFile(_path=path.join(path_out, file_name), text=self.template)

    @classmethod
    def parse_template(cls, template: str, kwargs: dict[str, str]) -> str:
        """
        @param template: Текст с ключевыми словами
        @param kwargs: ключи
        @return: Отформатированный текст
        """
        # Получить ключевые слова из текста
        re_obj = findall(f"{cls.split_regx[0]}([\w\d]+){cls.split_regx[1]}", template)
        logger.info(re_obj, flag="FIND")
        # Заменить ключевые слова из текста на те которые передали в метод
        for _key in re_obj:
            var: str = str(kwargs[_key])
            template: str = sub(f"{cls.split_regx[0]}{_key}{cls.split_regx[1]}", var, template)
        return template

    @staticmethod
    def writeFile(_path: str, text: str):
        """
        @param _path: Путь для записи файла
        @param text: Текст в файл
        """
        with open(_path, "w") as _file:
            _file.write(text)
        logger.info(_path, flag="FILE_WRITE")
