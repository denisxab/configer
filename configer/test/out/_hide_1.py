def export(
        file_name: str,
        path_out: str,
        template: str,
        kwargs: dict[str, str],
        is_rewrite: bool = True,
): return file_name, path_out, template, kwargs, is_rewrite


port = 8080
_hide_any_name: str =___

env = export("__env.env", "/test/in/", """
## Django
# Ключ для расшифровки сессии
DJANGO_SECRET_KEY="$$(secret_key)$$"
# Имя проекта
NAME_PROJ="$$(project_name)$$"
# Режим работы (true/false)
DEBUG=true

### Docker
# Путь к рабочей директории
WORK_DIR="/usr/src/$$(project_name)$$"
# Путь к переемным окружениям
PATH_ENV="./__env.env"
NGINX_PORT=$$(port)$$

"""[1:], {
    "secret_key": "dq232dc3f34f32q4fwe3",
    "project_name": "МойПроект",
    "port": port,
})

EXPORT_PATH = [env]
