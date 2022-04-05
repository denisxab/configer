from useconf import export_code, autotests

math = {
    "sum": export_code(
        template_lange={
            "py": """
def $$(fun_name)$$(a: int, b: int) -> int:
    '''
    $$(doc)$$
    $$(TEST)$$
    '''
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
        kwargs={
            "fun_name": "sum_two_number",
            "doc": "Сложение двух чисел",
            "TEST": autotests(
                {
                    "in": "sum_two_number(1, 2)",
                    "out": "3"
                },
                {
                    "in": "sum_two_number(3, 3)",
                    "out": "6"
                },
                {
                    "in": "sum_two_number(-10, -10)",
                    "out": "-20"
                },
            )
        }
    )
}

EXPORT_COMMAND = {
    **math
}
