from useconf import export_path

port = 8080
secret_key = "sdfADSfsfsqdef43SD23"
project_name = "configer"

EXPORT_PATH = (
    export_path(
        namefile="__env.env",
        path="./",
        template="""
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
"""[1:],
        kwargs={
            "secret_key": secret_key,
            "project_name": project_name,
            "port": port,
        },
    ),
)
