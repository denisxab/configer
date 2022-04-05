def export(
        file_name: str,
        path_out: str,
        template: str,
        kwargs: dict[str, str],
        is_rewrite: bool = True,
): return file_name, path_out, template, kwargs, is_rewrite


port = 8080
project_name = "dq232dc3f34f32q4fwe3"

readme_md = export("README.md", "../", """
## Что это
Программа: $$(project_name)$$
## Установка
## Использование
"""[1:], {
    "project_name": project_name
}, is_rewrite=False)

EXPORT_PATH = [
    readme_md
]
