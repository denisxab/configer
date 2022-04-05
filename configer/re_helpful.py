from re import sub

#: Спец символы для вставки значения по ключу
from typing import Final

SPLIT_REGX_START: Final[str] = "\$\$\("
#: Спец символы для вставки значения по ключу
SPLIT_REGX_END: Final[str] = "\)\$\$"


class RePython:
    """
    Работа с кодом ``Python``

    """

    @staticmethod
    def sub_staff(text: str, repl: str = '_') -> str:
        """
        Удаляем из исходного кода `Python`:

        - Кавычки
        - Подсказки типов
        - Скобки

        .. note::
            Но при этом длинна текста сохраниться,
            потому что мы заменяем значение на `repl`

        :param text: Текст
        :param repl: На что заменить
        :return: Текст без скобок и ковы чек и подсказок типа
        """

        #: Что должно быть в кавычках
        templ_ = "\w\d\s_.,/'@\+\-#$:=\[\]\(\)\{\}<>"
        # Вырезаем одинарные и двойные кавычки
        template_rep_quotation_mark = """["']{1}[\w\W][^\n]+["']{1}"""
        # Вырезать тройные кавычки
        template_rep_quotation_mark_three = """['"]{3}[%s]+['"]{3}""" % (templ_,)
        res = sub(f"{template_rep_quotation_mark}|{template_rep_quotation_mark_three}",
                  lambda m: f"{repl}" * len(m.group()),
                  text)
        # Удалить подсказки типов
        template_rep_type_hints: str = """(?![\w\d_\t ]):[ \t]*[\w\d_]+\[*[\w\d, ]*\]*"""
        res2 = sub(template_rep_type_hints,
                   lambda m: f"{repl}" * len(m.group()), res)
        # Вырезаем данные в скобках ()[]{}, даже если они вложенные
        template_rep_brackets = """[\[\(\{]{1}[\w\d\s_.,/'#$:\[\]\(\)\{\}]+[\]\})]{1}"""
        res3 = sub(f"{template_rep_brackets}",
                   lambda m: f"{repl}" * len(m.group()),
                   res2)
        return res3
