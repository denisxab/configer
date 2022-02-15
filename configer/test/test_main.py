from configer.configer import ConfFile


def test_parse_template():
    env = ConfFile("__env.env", "./test/", """
    # (!) - обозначает что нельзя изменять имя ПО, так как его используют официальное образы.

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
    # Внешний порт <!Изменить значения на свои>
    EXTERNAL_WEB_PORT=8081
    # Внешний и Внутренний порт для `nginx`. EXTERNAL_WEB_PORT != NGINX_PORT <!Изменить значеня на свои>
    NGINX_PORT=8080


    ### Postgres
    #  Имя БД (!) <!Изменить значения на свои>
    POSTGRES_DB="postgres"
    # Имя пользователя (!) <!Изменить значения на свои>
    POSTGRES_USER="postgres"
    # Пароль от пользователя (!) <!Изменить значения на свои>
    POSTGRES_PASSWORD="postgres"
    # Имя сервиса(контейнера)
    POSTGRES_HOST="db"
    # Порт подключения к БД. (По умолчанию 5432)
    POSTGRES_PORT=5432
    # Путь к зеркальной папке с БД
    POSTGRES_VOLUMES="./db/pg_data"
    """, {"secret_key":"dq232dc3f34f32q4fwe3", "project_name":"Тест"})

    assert env.template == '\n    # (!) - обозначает что нельзя изменять имя ПО, так как его используют официальное образы.\n\n    ## Django\n    # Ключ для расшифровки сессии\n    DJANGO_SECRET_KEY="dq232dc3f34f32q4fwe3"\n    # Имя проекта\n    NAME_PROJ="Тест"\n    # Режим работы (true/false)\n    DEBUG=true\n\n\n    ### Docker\n    # Путь к рабочей директории\n    WORK_DIR="/usr/src/Тест"\n    # Путь к переемным окружениям\n    PATH_ENV="./__env.env"\n    # Внешний порт <!Изменить значения на свои>\n    EXTERNAL_WEB_PORT=8081\n    # Внешний и Внутренний порт для `nginx`. EXTERNAL_WEB_PORT != NGINX_PORT <!Изменить значеня на свои>\n    NGINX_PORT=8080\n\n\n    ### Postgres\n    #  Имя БД (!) <!Изменить значения на свои>\n    POSTGRES_DB="postgres"\n    # Имя пользователя (!) <!Изменить значения на свои>\n    POSTGRES_USER="postgres"\n    # Пароль от пользователя (!) <!Изменить значения на свои>\n    POSTGRES_PASSWORD="postgres"\n    # Имя сервиса(контейнера)\n    POSTGRES_HOST="db"\n    # Порт подключения к БД. (По умолчанию 5432)\n    POSTGRES_PORT=5432\n    # Путь к зеркальной папке с БД\n    POSTGRES_VOLUMES="./db/pg_data"\n    '
