import os.path
from doctest import testmod
from types import ModuleType
from typing import Optional
from unittest import TestCase

from logsmal import loglevel
from mg_file.file.helpful import BaseHash


def проверить_подлинность_файла(infile: str, hash_sum: str):
    return BaseHash.check_hash_sum(BaseHash.file(infile), hash_sum)


def проверить_подлиность_текст(text: str, hash_sum: str):
    return BaseHash.check_hash_sum(BaseHash.text(text), hash_sum)


class ТестовыйФайл:
    """
    Вернуть файл если хеш сумма верна
    """

    def __init__(self, path: str, hash_sum: Optional[str]):
        """
        Проверить подлинность файла

        :param path:
        :param hash_sum:
        """
        if hash_sum is not None:
            проверить_подлинность_файла(path, hash_sum)
        self.path = path
        self.full_path = os.path.abspath(self.path)

    def прочесть(self):
        with open(self.full_path, "r", encoding='utf-8') as _f:
            return _f.read()

    def обновить(self, text: str):
        with open(self.full_path, "w", encoding='utf-8') as _f:
            return _f.write(text)


class ПрочитанныйТестовыйФайл(ТестовыйФайл):
    """
    Вернуть данные из фала если хеш сумма верна
    """

    def __init__(self, path: str, hash_sum: Optional[str]):
        """
        Проверить подлинность файла

        :param path:
        :param hash_sum:
        """
        super().__init__(path, hash_sum)
        self.__текст = None

    @property
    def текст(self):
        # Записать данные в переменную из файла, только при первом обращении.
        if self.__текст is None:
            return self.прочесть()
        return self.__текст


class ОткатываемыйФайл(ПрочитанныйТестовыйФайл):
    """
    Файл с возможностью отката данных, на момент создания класса.
    Или удалить файл, если он не был создан, на момент создания класса.


    with ОткатываемыйФайл():
        ...
    """

    def __init__(self, path: str, hash_sum: Optional[str]):
        super().__init__(path, hash_sum)
        self.существование = os.path.exists(self.full_path)
        # Если файл не существовал, то удаляем его при откате
        if not self.существование:
            self.прошлые_данные_из_файла = ''
        else:
            self.прошлые_данные_из_файла: str = self.текст

    def откатить(self):
        if self.существование:
            with open(self.full_path, 'w', encoding='utf-8') as _f:
                _f.write(self.прошлые_данные_из_файла)
        else:
            os.remove(self.full_path)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.откатить()


class TestDoc(TestCase):
    """
    Протестировать документацию у модулей

    .. code-block::python

        import logic_helpful
        from configer.test.helpful_test import TestDoc

        # Док тесты
        TestDoc.list_mod = (
            logic_helpful,
        )
    """
    #: Список модулей
    list_mod: tuple[ModuleType] = (
        # МОДУЛИ
    )

    def setUp(self):
        # Отключаем логирование ``logsmal``
        loglevel.__call__ = lambda *args, **kwargs: None

    def test_docs_from_module(self):
        for _m in TestDoc.list_mod:
            # Выполняем док тесты
            self.assertEqual(testmod(_m).failed, 0)
