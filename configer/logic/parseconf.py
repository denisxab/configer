from os import path
from typing import Union

from logsmal import logger
from mg_file.file.helpful import absolute_path_dir, read_file_by_module, BaseHash
from mg_file.file.txt_file import TxtFile

from .helpful import spec_name, parse_template


class parseconfLogic:
    """
    Класс для работы с файлом конфигурации
    """

    @classmethod
    def parseconf(cls, path_conf: str) -> dict[str, Union[dict, bool]]:
        res_export: list[Union[tuple[str, bool], tuple[str, str]]] = cls._parse_module(path_conf)
        return cls._list_path_to_dict_path(res_export)

    @staticmethod
    def _list_path_to_dict_path(list_path: list[Union[tuple[str, bool], tuple[str, str]]]):
        """Преобразовываем список путей в словарь путей"""
        response: dict[str, Union[dict, bool]] = {}
        for _p in list_path:
            _path = _p[0].lstrip("/").split("/")
            _key, _val = _path.pop(-1), _p[1]
            _target_dict = response
            for _component in _path:
                _target_dict = _target_dict.setdefault(_component, {})
            # Проверяем точно на `False` так как шаблон может иметь пустую строку
            if _val is not False:
                # Если хеш сумма данных в файле и готовых данных, различны, то перезаписываем данные в файле.
                if TxtFile(_p[0], type_file=None).writeIfDontEqHash(_val, hash_sha256=BaseHash.text(_val)):
                    _target_dict[_key] = True
                    logger.success(_p[0], flag="WRITE_TEMPLATE")
                # Если хеш суммы равны, то не перезаписываем файл
                else:
                    _target_dict[_key] = False
                    logger.info(_p[0], flag="NOT_WRITE_TEMPLATE_EQ_HASH")
            else:
                _target_dict[_key] = False

        return response

    @classmethod
    def _parse_module(cls, path_conf: str) -> list[Union[tuple[str, bool], tuple[str, str]]]:
        #: Читаем модуль
        module = read_file_by_module(path_conf)
        res_export: list[Union[bool, tuple[str, str]]] = []
        # Получить переменные из файла конфигурации, которые находятся в специальной переменной
        for _var in module.__dict__[spec_name.EXPORT_PATH.name]:
            # Получаем результат обработки экспорта
            res_export.append(cls._parse_export(*_var, _path_conf=path_conf))
        return res_export

    @classmethod
    def _parse_export(
            cls,
            file_name: str,
            path_out: str,
            template: str,
            kwargs: dict[str, str],
            is_rewrite: bool, *,
            _path_conf: str = "",
    ) -> Union[tuple[str, bool], tuple[str, str]]:
        """
        Обработать экспорт

        :param file_name: Имя файла который будет создам
        :param path_out: Путь куда поместить этот файл
        :param template: Шаблон
        :param kwargs: Словарь для заменой значений в шаблона
        :param is_rewrite: Нужно ли перезаписывать данные в файле, по умолчанию не нужно.
        :param _path_conf: Путь где расположен файл конфигураций
        :return: ПолныйПутьКФайлу:ГотовыйШаблон/Fasle
        """
        _file_path: str = path.join(path_out, file_name)

        #: Проверить необходимость перезаписи файла.
        #: Если файл существует и его не нужно перезаписывать то выходим
        if path.exists(absolute_path_dir(_file_path) / _file_path) and is_rewrite is False:
            return (_file_path, False)

        #: Создаем шаблон
        template: str = parse_template(template, kwargs)
        logger.info(_file_path, flag="CREATE_TEMPLATE")
        return (_file_path, template)
