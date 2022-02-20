port = 8080
_hide_any_name: str = "d1d1sxcdwc2qq32vwvdvw"


def ini(se: str):
    a = 10
    print(se)


_hide_env: tuple[str, str, dict] = ("__env.env", "/home/denis/PycharmProjects/configer/configer/test/data_set/", """
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

""", {
    "secret_key": "dq232dc3f34f32q4fwe3",
    "project_name": "МойПроект",
    "port": port,
})
tmp = "q12312"

export_var = [
    _hide_env
]

hide_var = [
    'any_name'
]
