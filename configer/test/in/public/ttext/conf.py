from re import sub, split, search

from logic_helpful import SPLIT_REGX_START, SPLIT_REGX_END
from useconf import export_template


def quotes_comma(text, kwargs, template):
    """
    Текста в кавычках через запятую

    >>> quotes_comma("a, b, c")
    '"a", "b", "c"'
    """
    return '"{0}"'.format('", "'.join(split(' *, *', text)))


def comma(text, kwargs, template):
    """
    Текста через запятую

    >>> comma("a,    b,  c")
    'a, b, c'
    """
    return sub('[\t ]+', ' ', text)


def tuple_srt(text, kwargs, template):
    """
    Вставки картежей по колличеству аргументов

    >>> tuple_srt("a, b, c")
    '(" ", " ", " ",)'
    """
    return '({0})'.format('" ",' * len(text.split(',')))


def tuple_int(text, kwargs, template):
    """
    Вставки картежей по колличеству аргументов

    >>> tuple_int("a, b, c")
    '(0, 0, 0,)'
    """
    return '({0})'.format('0, ' * len(text.split(',')))


def create_assert(text, kwargs, template):
    """
    Создание ассертов

    >>> create_assert("a, b, c")
    assert a == 0, ''\nassert b == 0, ''\nassert c == 0, ''\n
    """
    padding: str = search(f"(?P<padding>[\t ]*){SPLIT_REGX_START}[\w\d_]+\|create_assert{SPLIT_REGX_END}",
                          template).group('padding')
    return ''.join([f'assert {x} == 0, ""\n{padding}' for x in text.split(',')])


def params(text, kwargs, template):
    """
    Создание параметров

    >>> params("a, b, c")
    \n:params a:\n:params b:\n:params c:
    """
    padding: str = search(f"(?P<padding>[\t ]*){SPLIT_REGX_START}[\w\d_]+\|create_assert{SPLIT_REGX_END}",
                          template).group('padding')
    return ''.join([f'\n{padding}:params {x}:' for x in text.split(',')])


EXPORT_TEMPLATE = {
    "pytest": export_template(
        template='''
@pytest.mark.parametrize(
                ($$(args|quotes_comma)$$),
                [
                    $$(args|tuple_quotes)$$,
                ]
)
def test_$$(name)$$(self, $$(args|comma)$$):
    """
    $$(doc)$$

    $$(args|params)$$
    """

    $$(args|create_assert)$$
'''[1:],
        kwargs={
            "args": None,
            "name": None,
            'doc': None,
        },
        func={
            "quotes_comma": quotes_comma,
            "tuple_quotes": tuple_int,
            "comma": comma,
            'create_assert': create_assert,
            "params": params,
        }
    ),
}
