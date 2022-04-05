from useconf import export_code

EXPORT_COMMAND = {
    "sum": export_code(
        template_lange={
            "py": """
def $$(fun_name)$$(a: float, b: float) -> int:
    '''$$(doc)$$'''
    return int(a + b)
"""[1:],
        },
        # Ключи для шаблонов, которые доступные во всех языках
        kwargs={
            "fun_name": "sum_two_float",  # ! Изменен
            "doc": "Сложение двух чисел"
        }
    )
}
