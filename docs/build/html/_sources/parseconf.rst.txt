Создание файлов конфигурации
----------------------------

Для того чтобы указать какие переменные нужно рассматривать в качестве конфигураций,
их нужно поместить в переменную
``EXPORT_PATH``, переменная с конфигурациями должна соответствовать правилам,
это должен быть картеж со следующим порядком
значений: :class:`logic_helpful.spec_name`,
эти значения подставится в :meth:`logic_parseconf.parseconfLogic.parseconf`

:configer/test/in/public/parseconf/conf.py:

.. literalinclude:: ../../configer/test/in/public/parseconf/conf.py


По команде

.. code-block:: bash

    configer parseconf ./conf.py


Создадутся файлы по указному пути ``./test/__env.env``, содержание этого файла

:configer/test/out/public/parseconf/__env.env:

.. literalinclude:: ../../configer/test/out/public/parseconf/__env.env

.. note::

    Перезаписывать файл если он уже существует

    Если нам нужно перезаписать файл когда он уже существует, то укажите последним значением ``isrewrite=True``

    :configer/test/in/public/parseconf/rewrite_conf.py:

    .. literalinclude:: ../../configer/test/in/public/parseconf/rewrite_conf.py

