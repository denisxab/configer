"""
EXPORT_COMMAND = {
    "ИмяКоманды":(
        {
            "ЯзыкПрограммирования_1":"ШаблонныйТекст",
        },
        {
            "Ключ_1":"Значение",
        }
    )
}
"""

EXPORT_COMMAND = {
    "sum": (
        {
            "py": """
def $$(fun_name)$$(a: int, b: int) -> int:
    '''$$(doc)$$'''
    return a + b
"""[1:],
            "cpp": """
int $$(fun_name)$$ (int a, int b){
    /*$$(doc)$$*/
    return a+b;
}
"""[1:],
            "js": """
function $$(fun_name)$$ (a, b){
    /*$$(doc)$$*/
    return a+b;
}
 """[1:]
        },
        # Ключи для шаблонов, которые доступные во всех языках
        {
            "fun_name": "sum_two_number",
            "doc": "Сложение двух чисел"
        }
    )
}
