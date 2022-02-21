## Что это

Программа для создания файлов конфигурации. Часто встречается нужда держать конфигурационные файлы в порядке, и
консистенции, распределять общие данные по разным типам файлам, у некоторых типов файлов нет возможности читать
переменные окружения, или приходиться подстраиваться под каждый формат по отдельности. Для того чтобы не подстраиваться
под каждый формат файла, можно использовать всю мощь `python` и держать все конфигурации в одном файле.

[Документация](https://configer.readthedocs.io/ru/latest/index.html)

## Установка

1) Скачать `configer.bin` из репозитория
2) Добавить `alias` в консоль

  ```bash
  alias -g configer="$ПутьГдеРасположенСonfiger$.bin"
  ```

3) Проверим правильность указания пути

  ```bash
  configer --help
  ```

## Использование

### Консольные команды

- Скомпилировать конфигурационные файлы

  ```bash
  configer parseconf $ПутьКонфигурациям$.py
  ```

- Сделать копию и скрыть данные

  ```bash
  configer hideconf $ПутьКонфигурациям$.py
  ```

### Создание файла конфигураций

Для того чтобы указать какие переменные нужно рассматривать в качестве конфигураций, их нужно поместить в переменную
`export_var`, переменная с конфигурациями должна соответствовать правилам, это должен быть картеж со следующим порядком
значений:

- Название файла (`str`)
- Путь куда поместить файл (`str`)
- Шаблон (`str`)
    - Значения которые нужно взять из словаря заключите в `$$(Ключ)$$`
- Словарь для замены слов (`dict[str,str]`)

> Эти значения подставится в `ConfFile(*args)`

```python
port = 8080

env = ("__env.env", "./test", """
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
NGINX_PORT=8811

"""[1:], {
    "secret_key": "dq232dc3f34f32q4fwe3",
    "project_name": "МойПроект",
    "port": port,
})
export_var = [
    env
]
```

Выполним команду

```bash
configer parseconf conf.py
```

В итоге мы получим файл, расположенный в `./test/__env.env`. Содержание

```text
## Django
# Ключ для расшифровки сессии
DJANGO_SECRET_KEY="dq232dc3f34f32q4fwe3"
# Имя проекта
NAME_PROJ="МойПроект"
# Режим работы (true/false)
DEBUG=true

### Docker
# Путь к рабочей директории
WORK_DIR="/usr/src/МойПроект"
# Путь к переемным окружениям
PATH_ENV="./__env.env"
NGINX_PORT=8080
```

Логи

```text
[INFO][TEMPLATE]:'__env.env'
[INFO][FIND]:['secret_key', 'project_name', 'project_name', 'port']
[INFO][FILE_WRITE]:'/home/denis/PycharmProjects/configer/configer/test/data_set/__env.env'
[INFO][VAR_CREATE]:'__env.env'
```

## Сделать копию и скрыть данные

Почти всегда нам нужно иметь в проекте секретные(приватные) данные, которые не должны стать публичными. У нас есть
возможность создавать копию конфигурации со скрытыми данными.

Для того чтобы указать переменную у которой нужно скрыть значения, напишите в начел её имени `_hide_`

---

Пример, нам нужно скрыть данные `url` для подключения к БД, ключ для шифрования сессии, данные для входа в админ панель,
ну или любые другие данные. Для того чтобы сделать копию этой конфигурации, например, для того чтобы сохранить всю
логики, но при этом скрыть выше указанные данные, мы указываем в начале имени `_hide_`, в итоге мы получим
файл `conf_pub.py` который можно спокойно хранить в открытом доступе, например в `GitHab`.

```python
_hide_SQL_URL: str = "postgresql+asyncpg://postgres:root@localhost/fast"
_hide_SESSION_SECRET_KEY = "qQWEdqwdwqefASDQF4qw4h3ofv3vw3oervwg532gg5"
_hide_ADMIN_PANEL: tuple[str, str, str] = ("user", "password", "emal")

host = "0.0.0.0"
port = 8080

env = ("__env.env", "./test", """
SQL_URL = $$(sql_url)$$
SESSION_SECRET_KEY = $$(session_secret_kry)$$
ADMIN_PANEL = $$(admin_panel)$$
"""[1:], {
    "sql_url": _hide_SQL_URL,
    "session_secret_kry": _hide_SESSION_SECRET_KEY,
    "port": port,
})
export_var = [
    env
]
```

Выполним команду

```bash
configer hideconf conf.py
```

В итоге мы получим копию, расположенный в `./conf_pub.py`. Содержание

```python
_hide_ADMIN_PANEL: tuple[str, str, str] = ___
_hide_SESSION_SECRET_KEY = ___
_hide_SQL_URL: str = ___

host = "0.0.0.0"
port = 8080

env = ("__env.env", "./test", """
SQL_URL = $$(sql_url)$$
SESSION_SECRET_KEY = $$(session_secret_kry)$$
ADMIN_PANEL = $$(admin_panel)$$
"""[1:], {
    "sql_url": _hide_SQL_URL,
    "session_secret_kry": _hide_SESSION_SECRET_KEY,
    "port": port,
})
export_var = [
    env
]
```

Логи

```text
[INFO][VAR_HIDE]:'_hide_ADMIN_PANEL: tuple[str, str, str]'
[INFO][VAR_HIDE]:'_hide_SESSION_SECRET_KEY'
[INFO][VAR_HIDE]:'_hide_SQL_URL: str '
```

## Реальный пример конфигурации

```python
# Режим работы 
DEBUG: bool = True
# Имя проекта
project_name: str = "frontend_template"
# Путь к скомпилированным статичным файлам 
path_public: str = f"/{project_name}/frontend_react/static/frontend_react/public/"
# Путь ко всем статическим файлам
path_static: str = f"/{project_name}/frontend_react/static/"


class Nginx:
    # Внешний и Внутренний порт для `nginx`. EXTERNAL_WEB_PORT != NGINX_PORT <!Изменить значеня на свои>
    PORT: int = 8080
    # Путь к рабочей директории
    WORK_DIR: str = f"/usr/src/{project_name}"
    # Внешний порт <!Изменить значения на свои>
    EXTERNAL_PORT: int = 8080


"""
Конфигурации
"""
env = ("__env.env", "./",
       """
       # (!) - обозначает что нельзя изменять имя ПО, так как его используют официальное образы.
       
       ## Django
       # Ключ для расшифровки сессии
       # DJANGO_SECRET_KEY="django-insecure-@jt^$2(a!%rl%hs8^y@hu^am^+6h^rg4pwo*kp8d@1!+!5gl=i"
       # Имя проекта
       NAME_PROJ="$$(project_name)$$"
       # Режим работы (true/false)
       DEBUG=$$(DEBUG)$$
       
       
       ### Docker
       # Путь к рабочей директории
       WORK_DIR="$$(WORK_DIR)$$"
       # Путь к переемным окружениям
       PATH_ENV="./__env.env"
       # Внешний порт <!Изменить значения на свои>
       EXTERNAL_WEB_PORT=$$(EXTERNAL_WEB_PORT)$$
       # Внешний и Внутренний порт для `nginx`. EXTERNAL_WEB_PORT != NGINX_PORT <!Изменить значеня на свои>
       NGINX_PORT=$$(NGINX_PORT)$$
       
       
       # ### Postgres
       # #  Имя БД (!) <!Изменить значения на свои>
       # POSTGRES_DB="postgres"
       # # Имя пользователя (!) <!Изменить значения на свои>
       # POSTGRES_USER="postgres"
       # # Пароль от пользователя (!) <!Изменить значения на свои>
       # POSTGRES_PASSWORD="postgres"
       # # Имя сервиса(контейнера)
       # POSTGRES_HOST="db"
       # # Порт подключения к БД. (По умолчанию 5432)
       # POSTGRES_PORT=5432
       # # Путь к зеркальной папке с БД
       # POSTGRES_VOLUMES="./db/pg_data"
       """[1:],
       {
           "WORK_DIR": Nginx.WORK_DIR,
           "project_name": project_name,
           "NGINX_PORT": Nginx.PORT,
           "EXTERNAL_WEB_PORT": Nginx.EXTERNAL_PORT,
           "DEBUG": "true" if DEBUG else "false"
       }
       )
npm = (
    "package.json", "./",
    """
    {
        "name": "$$(project_name)$$",
        "version": "1.0.0",
        "description": "...",
        "private": true,
        "scripts": {
            "/1": "Запустить автоматически перезагружаемый сервер [--mode development]",
            "dev": "webpack serve --config $$(webpack_path)$$",
            "/2": "Собрать проект `JS`. Для оптимизированной сборки измените `__env.env->DEBUG='false'` или [--mode production]",
            "build": "webpack --config $$(webpack_path)$$",
            "/3": "Получить данные о размере банглов",
            "status": "webpack --config $$(webpack_path)$$ --json >status.json && webpack-bundle-analyzer status.json"
        },
        "author": "...",
        "license": "ISC",
        "devDependencies": {
            "@types/react": "^16.8.24",
            "@types/react-dom": "^16.0.5",
            "@types/webpack": "4.1.4",
            "clean-webpack-plugin": "^4.0.0",
            "copy-webpack-plugin": "^10.2.0",
            "css-loader": "^6.5.1",
            "file-loader": "^6.2.0",
            "html-webpack-plugin": "^5.5.0",
            "loader": "^2.1.1",
            "mini-css-extract-plugin": "^2.4.5",
            "optimize-css-assets-webpack-plugin": "^6.0.1",
            "sass": "^1.45.0",
            "sass-loader": "^12.4.0",
            "style-loader": "^3.3.1",
            "terser-webpack-plugin": "^5.3.0",
            "ts-loader": "^6.2.1",
            "typescript": "^3.9.10",
            "webpack": "^5.67.0",
            "webpack-bundle-analyzer": "^4.5.0",
            "webpack-cli": "^4.9.2",
            "webpack-dev-server": "^4.7.3"
        },
        "dependencies": {
            "bootstrap": "^5.1.3",
            "react-bootstrap": "^2.0.4",
            "dotenv": "^10.0.0",
            "react": "^16.12.0",
            "react-dom": "^16.12.0",
            "react-router-dom": "^6.2.1"
        }
    }
    """[1:],
    {
        "project_name": project_name,
        "webpack_path": f"{project_name}/webpack.config.js"
    }
)

gitignore = (
    ".gitignore", "./",
    """
    /node_modules
    $$(path_static)$$
    """[1:],
    {
        "path_static": path_public,
    }
)

nginx = (
    "default.conf", "./nginx",
    """
server {
    listen $$(NGINX_PORT)$$
    default_server;

    # Задаёт максимально допустимый размер тела запроса клиента.
    client_max_body_size 4G;

    location = /favicon.ico {
        access_log off; log_not_found off;
    }

    # Раздача `index.html`
    location / {
        root $$(root_path)$$;
    }

    # Раздача статических файлов
    # http://127.0.0.1:$$(NGINX_PORT)$$/static/frontend_react/public/index.html
    location /static/ {
        alias $$(static_path)$$;
    }

    # Раздача медиа файлов
    #location /media/ {
    #        root  $Work_dir/$Name_proj/media;
    #}
}
    """[1:],
    {
        "NGINX_PORT": Nginx.PORT, "WORK_DIR": Nginx.WORK_DIR, "NAME_PROJ": project_name,
        "static_path": f"{Nginx.WORK_DIR}{path_static}",
        "root_path": f"{Nginx.WORK_DIR}{path_public}",
    }
)

export_var = [env, npm, gitignore, nginx]
```