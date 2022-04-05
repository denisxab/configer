from useconf import export_path

project_name = "configer"

EXPORT_PATH = (
    export_path(
        # Этот файл создастся только если он не существует
        namefile="README.md",
        path="../",
        template="""
## Что это
Программа: $$(project_name)$$
## Установка
## Использование
    """[1:],
        kwargs={
            "project_name": project_name
        }
    ),
    export_path(
        # Этот файл будет постоянно перезаписываться
        # (перезапись произойдет если данные изменились)
        namefile="gitignore",
        path="../",
        template="""
/venv
/.ide
/$$(project_name)$$/log
    """,
        kwargs={
            "project_name": project_name
        },
        isrewrite=True
    )
)
