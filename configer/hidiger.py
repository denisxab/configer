"""."""
from re import sub, finditer
from typing import NamedTuple


class TypeHidden(NamedTuple):
    """
    Тип для возвращаемого значения `sub_data_from_variables`



    :var sub_text: Скрытый текст
    :arg res_find_var: Список имен переменных у которых было скрыты значения
    """
    sub_text: str
    res_find_var: list[str]


class HiddenVar:
    """
    Скрыть данные значений из файла с конфигурациями
    """

    def __new__(cls, text_conf, prefix="_hide_", repl="___", ) \
            -> TypeHidden:
        """

        :param text_conf:
        :param prefix:
        :param repl:
        """
        return cls.sub_data_from_variables(
            text_conf,
            cls.sub_staff(text_conf),
            prefix=prefix,
            repl=repl,
        )

    @staticmethod
    def sub_staff(text: str, repl: str = '_') -> str:
        """
        Удаляем из исходного кода `Python`
        1. Кавычки
        2. Подсказки типов
        3. Скобки

        НО при этом длинна текста сохраниться, потому что мы заменяем значение на `repl`
        """
        # Вырезаем одинарные и двойные кавычки
        template_rep_quotation_mark = """['"]{1}[\w\d\s_.,/'#$:=\[\]\(\)\{\}]+['"]{1}"""
        # Вырезать трое двойных кавычек
        template_rep_quotation_mark_three = """['"]{3}[\w\d\s_.,/'"#$:=\[\]\(\)\{\}]+['"]{3}"""
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

    @staticmethod
    def sub_data_from_variables(source_text: str, text: str, prefix="_hide_", repl="___") \
            -> TypeHidden:
        """
        Ищем и удаления значений у переменных имеющий префикс `prefix=`

        @param source_text: Исходный текст.
        @param text: Рекомендую обработать текс в функции `sub_quotation_mark`
        шаблон ожидает, то что в тексте не будет данных в кавычках и скобках, а также
        подсказок типов.
        @param repl: На что заменить.
        @param prefix: Какой префикс должен стоять в начале переменной,
        чтобы скрыть её данные.
        @return:
        """

        res_find_var: list[str] = []
        # Удалить значения у переменных
        template_search: str = """([ \t]*%s[\w\d_]+)[ \t]*=([ \t][\w_\d]+)\n{1}""" % (prefix,)
        # Отступ с учетом удаления символов.
        count_cup_symbol: int = 0
        """
        Ищем все совпадения, вернем итератор в котором будет диапазон расположения
        в нем расположен текст который нужно удалить(скрыть).
        """
        len_repl: int = len(repl)
        for x in finditer(template_search, text):
            # Добавляем найденную переменную в результат
            rfv = x.regs[1]
            res_find_var.append(
                # Берем имя переменной с учетом удаленных символов
                source_text[rfv[0] - count_cup_symbol:rfv[1] - count_cup_symbol]
            )
            # Удаляем значение переменной
            r = x.regs[2]
            # Берем все до, берем все после, и создаем новый текст.
            source_text = "{0}{1}{2}".format(
                source_text[0:r[0] - count_cup_symbol],
                repl,
                # !: len(source_text) нужен самостоятельно высчитать длину,
                # !: а не взять `-1`, иначе мы потеряем символы в конце
                source_text[r[1] - count_cup_symbol:len(source_text)])
            # Конец минус начало, и минус доп символы замены.
            count_cup_symbol += (r[1] - r[0]) - len_repl

        return TypeHidden(sub_text=source_text, res_find_var=res_find_var)
