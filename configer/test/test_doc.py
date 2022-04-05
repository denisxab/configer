from doctest import testmod
from types import ModuleType
from unittest import TestCase, main

from logsmal import loglevel

import configer.logic_parseconf


class TestDoc(TestCase):
    """
    Протестировать документацию у модулей
    """
    #: Список модулей
    list_mod: tuple[ModuleType] = (
        configer.logic_parseconf,
    )

    def setUp(self):
        # Отключаем логирование ``logsmal``
        loglevel.__call__ = lambda *args, **kwargs: None

    def test_docs_from_module(self):
        """

        :param mod: Список модулей
        """
        for _m in TestDoc.list_mod:
            # Выполняем док тесты
            self.assertEqual(testmod(_m).failed, 0)


if __name__ == '__main__':
    main()
