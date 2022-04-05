from pathlib import Path
from typing import Optional, Literal, Protocol, Union, Final

from mg_file import read_file_by_module

# Путь для хранения локальных настроек конфигуратора
PATH_SETTINGS_CONFIGER: Final[str] = f'{str(Path(__file__).resolve().parent.parent)}/store_configer.json'


def importpy(path: str, self_path: str):
    """
    Импортировать модуль по его пути

    :Аналог:
    # Добавление путей для импорта
    from sys import path
    from pathlib import Path
    path.insert(0 , str(Path(__file__).resolve().parent))
    # Добавление кастомных импортов
    import ИмяМодуля
    """
    path = str(
        Path(
            Path(self_path).resolve().parent
        ).joinpath(path)
    )
    return read_file_by_module(path)


def export_path(namefile: str, path: str, template: str, kwargs: dict[str, str], isrewrite: bool = False) -> tuple:
    """
    Помощник для создания экспорта :doc:`parseconf <./parseconf>`

    .. code-block:: python

        EXPORT_PATH = (
            export_var(
                namefile="ИмяФайла", path="ПутьДляСохранения",
                template='''
        Пример вставки ключа $$(Ключ_1)$$
                '''[1:],
                # Ключи для замены
                kwargs={
                    "Ключ_1": "Значение",
                },
                #: Опционально !
                #: Перезаписать файл если он существует (по умолчанию нет)
                isrewrite=False
            ),
        )
    """
    return namefile, path, template, kwargs, isrewrite


class ttext_func(Protocol):
    """
    Оформление функции для ``ttext``
    """

    def __call__(
            self,
            text: str,
            kwargs: dict[str, str],
            template: str,
    ) -> str: ...


def export_template(
        template: str,
        kwargs: dict[str, Optional[str]],
        func: Optional[dict[str, ttext_func]] = None):
    """
    Помощник для создания экспорта :doc:`ttext <./ttext>`

    .. code-block:: python

        def Функция(text:str, kwargs:dict[str, str], template:str):
            return ""

        EXPORT_TEMPLATE = {
            "ИмяШаблона": export_template(
                template='''
        Вот пример вставки ключа, после обработки переданной функцией $$(Ключ_1|ИмяФункции_1)$$
                  ''',
                # Ключи для замены
                kwargs={
                    "Ключ_1": "Значение",
                },

                #: Опционально !
                #: Ключевые функции
                func={
                    "ИмяФункции_1": Функция,
                }
            ),
        }
    """
    return template, kwargs, func


def autotests(
        *args: dict[
            Union[Literal["in", "out"], str],
            str
        ]) -> tuple:
    """
    Функция для создания тестов

    :param args: Входные и выходные данные

    .. code-block:: python

        {
            "in":"входные",
            "out":"выходные"
        },

    .. note::
        Разрабатывается поддержка для многих языков



    """
    return args


def export_code(
        template_lange: dict[str, str],
        kwargs: dict[str, str]
) -> tuple:
    """
    Помощник для создания экспорта :doc:`tcode <./tcode>`

    :param template_lange: Язык программирования
    :param kwargs: Ключи для шаблонов, которые доступны во всех языках

    Для :doc:`tcode <./tcode>`

    .. code-block:: python

        EXPORT_COMMAND = {
            "ИмяКоманды": export_code(
                template_lange={
                    "ЯзыкПрограммирования_1": '''
        Пример вставки ключа $$(Ключ_1)$$
        Вставить где угодно готовый тест $$(TEST)$$
                                '''[1:],
                },
                #: Ключи для замены, доступны во всех языках
                kwargs={
                    "Ключ_1": "Значение",

                    #: Опционально !
                    #: Создание тестов ключевое слово ``TEST``
                    "TEST": autotests(
                        # Тест_1
                        {
                            "in": ...,
                            "out": ...,
                        },
                    )
                }
            )
        }
    """
    return template_lange, kwargs
