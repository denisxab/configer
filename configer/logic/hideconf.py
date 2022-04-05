from re import finditer

from logsmal import logger
from mg_file import TxtFile
from mg_file.file.helpful import BaseHash

from re_helpful import RePython


class hideconfLogic:
    """
    Скрыть данные значений из файла с конфигурациями
    """

    @classmethod
    def hideconf(cls, path_conf: str, outfile: str):
        """
       :param path_conf: Путь к файлу конфигураций
       :param outfile: Путь для сохранения итогового файла
       """
        response_hide_conf: str = cls._parse_config(path_conf=path_conf)
        # Если хеш сумма данных в файле и готовых данных, различны, то перезаписываем данные в файле.
        if TxtFile(
                outfile,
                type_file='.py'
        ).writeIfDontEqHash(
            response_hide_conf,
            hash_sha256=BaseHash.text(response_hide_conf)
        ):
            logger.success(outfile, flag="FILE_HIDE_CREATE")
        # Если хеш суммы равны, то не перезаписываем файл
        else:
            logger.info(outfile, flag="NOT_WRITE_HIDE_EQ_HASH")

    @classmethod
    def _parse_config(cls, path_conf) -> str:
        """
        :param prefix: Что должно стоять в начале переменой, для того чтобы скрыть её значение
        :param repl: На что заменить значение если его нужно скрыть
        :return: Текст со скрытыми значениями
        :param path_conf:
        :return: Скрытые конфигурации
        """
        # Получаем исходный текст конфигурации
        text_conf: str = TxtFile(path_conf, type_file=".py").readFile()
        # Переменные которые необходимо скрыть, удаляем значения.
        # По умолчанию, для того чтобы пометить переменную, что её нужно скрыть
        # нужно написать в начале её `_hide_`.
        text_conf_rm_hide_var: str = cls._sub_data_from_variables(
            source_text=text_conf,
            text=RePython.sub_staff(text_conf)
        )
        return text_conf_rm_hide_var

    @staticmethod
    def _sub_data_from_variables(
            source_text: str,
            text: str,
            prefix: str = "_hide_",
            repl: str = "___"
    ) -> str:
        """
        Ищем и удаления значений у переменных имеющий префикс `prefix="_hide_"`

        :param source_text: Исходный текст.
        :param text: Рекомендую обработать текс в функции `sub_quotation_mark`
            шаблон ожидает, то что в тексте не будет данных в кавычках и скобках, а также
            подсказок типов.
        :param repl: На что заменить.
        :param prefix: Какой префикс должен стоять в начале переменной,
            чтобы скрыть её данные.
        :return: Текст у которого скрыты значения
        """

        список_скрытых_переменных: list[str] = []
        отступ_с_учетом_удаленных_символов: int = 0
        """
        Ищем все совпадения, вернем итератор в котором будет диапазон расположения
        в нем расположен текст который нужно удалить(скрыть).
        """
        текст_со_скрытыми_переменными = source_text
        len_repl: int = len(repl)
        for _elem in finditer("""([ \t]*%s[\w\d_]+)[ \t]*=([ \t][\w_\d]+)\n{1}""" % (prefix,), text):
            # Добавляем найденную переменную в результат
            rfv = _elem.regs[1]
            список_скрытых_переменных.append(
                # Берем имя переменной с учетом удаленных символов
                текст_со_скрытыми_переменными[
                rfv[0] - отступ_с_учетом_удаленных_символов:rfv[1] - отступ_с_учетом_удаленных_символов]
            )
            # Удаляем значение переменной
            r = _elem.regs[2]
            # Берем все до, берем все после, и создаем новый текст.
            текст_со_скрытыми_переменными = "{0}{1}{2}".format(
                текст_со_скрытыми_переменными[0:r[0] - отступ_с_учетом_удаленных_символов],
                repl,
                # !: len(текст_со_скрытыми_переменными) нужен самостоятельно высчитать длину,
                # !: а не взять `-1`, иначе мы потеряем символы в конце
                текст_со_скрытыми_переменными[
                r[1] - отступ_с_учетом_удаленных_символов:len(текст_со_скрытыми_переменными)])
            # Конец минус начало, и минус доп символы замены.
            отступ_с_учетом_удаленных_символов += (r[1] - r[0]) - len_repl

        logger.info(список_скрытых_переменных, flag="FIND_VAR_HIDE")
        return текст_со_скрытыми_переменными
