# Использование

```bash
./configer.bin $ПутьКонфигурациям$.py
```

## Консольные команды

## Создание файла конфигураций

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
2022-02-09 22:26:06.425 | INFO     | __main__:parse_conf:24 - [VAR] env
2022-02-09 22:26:06.425 | INFO     | main:__init__:27 - [TEMPLATE] __env.env
2022-02-09 22:26:06.426 | INFO     | main:parse_template:40 - [FIND] ['secret_key', 'project_name', 'project_name', 'port']
2022-02-09 22:26:06.426 | INFO     | main:writeFile:55 - [FILE_WRITE] ./test/__env.env
```
