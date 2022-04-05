from useconf import export_path

name_proj = "mg_crp"
version = "0.0.1"
author = "Denis Kustov <denis-kustov@rambler.ru>"
_hide_login= 'denisxab'


readthedocs_conf = export_path(
    namefile="conf.py",
    path="./docs/source/",
    template="""
# Файл конфигурации для конструктора документации Sphinx.
#
# Этот файл содержит только выбор наиболее распространенных опций. Для получения полного
# список см. в документации:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# Если расширения (или модули для документирования с помощью autodoc) находятся в другом каталоге,
# добавьте эти каталоги в sys.path здесь. Если каталог является относительным по отношению к
# корня документации, используйте os.path.abspath, чтобы сделать его абсолютным, как показано здесь.

import os
import sys
from pathlib import Path

def absolute_path_dir(_file: str, back: int = 1) -> Path:

    #Получить абсолютный путь к своей директории
    #:param _file: Путь
    #:param back: Сколько отступить назад

    res = Path(_file).resolve()
    for _ in range(back):
        res = res.parent
    return res


sys.path.insert(0, os.path.abspath('.'))

# Путь к проекту ./../..
sys.path.insert(0, str(absolute_path_dir(__file__, 3)))
print(sys.path)
# -- Project information -----------------------------------------------------

project = '$$(name_proj)$$'
copyright = '$$(author)$$'
author = '$$(author)$$'

# Полная версия, включая теги alpha/beta/rc
release = '$$(version)$$'

# -- General configuration ---------------------------------------------------

# Добавьте сюда имена любых модулей расширения Sphinx в виде строк. Это могут быть
# расширениями, поставляемыми с Sphinx (с именем 'sphinx.ext.*') или вашими собственными
# расширения.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    "m2r2",
]
source_suffix = [".rst", ".md"]

# Добавьте сюда все пути, содержащие шаблоны, относительно этой директории.
templates_path = ['_templates']

# Язык для содержимого, автогенерируемого Sphinx. Обратитесь к документации
# для списка поддерживаемых языков.
# Этот параметр также используется, если вы выполняете перевод содержимого через каталоги gettext.
# Обычно для таких случаев вы задаете "language" из командной строки.
language = 'ru'

# Список шаблонов, относительно исходного каталога, которые соответствуют файлам и
# каталогов, которые следует игнорировать при поиске исходных файлов.
# Этот шаблон также влияет на html_static_path и html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# Тема, используемая для страниц HTML и HTML-справки.  См. документацию для
# список встроенных тем.
html_theme = 'sphinx_rtd_theme'

# Добавьте сюда все пути, содержащие пользовательские статические файлы (например, таблицы стилей),
# относительно этого каталога. Они копируются после встроенных статических файлов,
# поэтому файл с именем "default.css" будет перезаписывать встроенный "default.css".
html_static_path = ['_static']
"""[1:],
    kwargs={
        "name_proj": name_proj,
        "author": author,
        "version": version,
    }, isrewrite=True
)

readthedocs_yaml = export_path(
    namefile=".readthedocs.yaml",
    path="./",
    template="""
# .readthedocs.yaml
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the version of Python and other tools you might need
build:
	os: ubuntu-20.04
	tools:
		python: '3.10'
		# You can also specify other tool versions:
		# nodejs: "16"
		# rust: "1.55"
		# golang: "1.17"

sphinx:
	# Путь к конфигурациям +++++
	configuration: docs/source/conf.py

# Optionally declare the Python requirements required to build your docs
python:
	install:
		# Путь к зависимостям +++++
		- requirements: docs/requirements.txt
# If using Sphinx, optionally build your docs in additional formats such as PDF
# formats:
#    - pdf
"""[1:], kwargs={}, isrewrite=True
)

pyproject_toml = export_path(
    namefile="pyproject.toml",
    path="./",
    template="""
[tool.poetry]
name = "$$(name_proj)$$"
version = "$$(version)$$"
description = "Создание файлов конфигураци"
repository = "https://github.com/$$(git_login)$$/$$(name_proj)$$.git"
documentation = "https://$$(name_proj)$$.readthedocs.io/ru/latest/index.html"
authors = ["$$(auth)$$"]
readme = "README.md"
exclude = [
    "$$(name_proj)$$/.idea",
    "$$(name_proj)$$/venv",
    "$$(name_proj)$$/venvs",
    "$$(name_proj)$$/.git",
    "$$(name_proj)$$/.gitignore",
    "$$(name_proj)$$/test",
    "$$(name_proj)$$/Makefile"
]

[tool.poetry.dependencies]
python = "^3.10"


[tool.poetry.dev-dependencies]
pytest = "^7.0.0"
Nuitka = "^0.6.19"
Sphinx = "^4.4.0"
sphinx-autobuild = "^2021.3.14"
sphinx-rtd-theme = "^1.0.0"
m2r2 = "^0.3.2"


[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

"""[1:],
    kwargs={
        "name_proj": name_proj,
        "version": version,
        "auth": author,
        "git_login": _hide_login,
    }
)

index_rst = export_path(
    namefile="index.rst",
    path="./docs/source/",
    template="""
Навигация
=========

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. toctree::
   :maxdepth: 2
   :caption: Оглавление:

   use_guide
   api

"""[1:], kwargs={}
)

use_guide_rst = export_path("use_guide.rst", "./docs/source/", """
Быстрый старт
=============

.. mdinclude:: ../../README.md

"""[1:], {})

api_rst = export_path(namefile="api.rst", path="./docs/source/", template="""
Описание APi
------------

.. automodule:: main
    :members:
    :undoc-members:
    :special-members: __init__
    :inherited-members:

"""[1:], kwargs={})

makefile = export_path("Makefile", "./", """
name_bin_file = "$$(name_proj)$$.bin"
proj_name = "$$(name_proj)$$"

# Генерировать документацию
auto_doc:
	sphinx-autobuild -b html ./docs/source ./docs/build/html

# Создать файл зависимостей для Read The Docs
req_doc:
	poetry export -f requirements.txt --output ./docs/requirements.txt --dev --without-hashes;

# Скомпилировать проект
compile:
	python -m nuitka --follow-imports $(proj_name)/main.py -o $(name_bin_file)

debug:
	python -m nuitka --follow-imports $(proj_name)/main.py -o $(name_bin_file) --remove-output

init:
	pip install poetry && poetry install && mkdir docs && sphinx-quickstart -p "$$(name_proj)$$" -a "$$(auth)$$" -v "$$(version)$$" -l "ru"  -r "$$(version)$$" --sep

"""[1:], {
    "name_proj": name_proj,
    "auth": author,
    "version": version,
}, isrewrite=True)

gitignore = export_path(".gitignore", "./", """
/.idea
/venvs
/venv
/__pycache__
/dist
/__pycache__/
/$$(name_proj)$$/__pycache__/
$$(name_proj)$$.bin
/main.build
"""[1:], {
    "name_proj": name_proj,
})

main_proj = export_path(f"main.py", f"./{name_proj}", """

if __name__ == "__main__":
    print("$$(name_proj)$$")
""", {
    "name_proj": name_proj
})

readme_md = export_path("README.md", "./", """""", {})

EXPORT_PATH = (
    pyproject_toml,
    readthedocs_yaml,
    readthedocs_conf,
    makefile,
    gitignore,
    index_rst,
    use_guide_rst,
    api_rst,
    main_proj,
    readme_md,
)
