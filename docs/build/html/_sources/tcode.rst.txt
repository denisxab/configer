Генерация кода
--------------

1 Файл с командами (``configer tcode print``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Иметь файл в котором будут храниться сборник команд, он будет состоять из блоков исходного кода, эти блоки могут быть
написаны на различных языках программирования, в этих блоках будут доступна возможность использовать шаблоны ``$$(Ключ)$$``
, данные для шаблона будут доступны во всех языках программирования внутри команды.

Для того чтобы указать какие переменные нужно рассматривать в качестве команд, их нужно поместить в переменную
``EXPORT_COMMAND``, переменная с конфигурациями должна соответствовать правилам, это должен быть картеж со следующим порядком
значений: :class:`logic_helpful.spec_name`, эти значения подставится в :meth:`logic_tcode.tcodeLogic.__new__`

Для того удобно создавать экспорты команды, используйте :meth:`useconf.export_code`

**Пример такого сборника команд**

:configer/test/in/public/tcode/print_conf.py:

.. literalinclude:: ../../configer/test/in/public/tcode/print_conf.py


По команде

.. code-block:: bash

    configer tcode print "sum" -l "py"


Мы получим вывод в консоль

:configer/test/out/public/tcode/print_tests.py:

.. literalinclude:: ../../configer/test/out/public/tcode/print_tests.py


2 Авто создание тестов (``TEST``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

    Данная возможность "пока" поддерживаться только для языка ``Python``

Для создания тестов есть специальный ключ ``TEST``, это поваляет вставить тесты в любое место шаблона.
Для создание ключа ``TEST`` рекомендую вызвать функцию :meth:`useconf.autotests`.

.. seealso::

    Если вам не нужны тесты то указывайте ключ ``$$(TEST)$$`` в шаблоне

3 Вставка шаблона в файл (``configer tcode infile``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Если нам нужно вставить этот блок кода в файл, то нужно в этом файле написать ``$$(ИмяКоманды:ЯзыкПрограммирования)$$``, в
это место вставиться готовый блок.


.. seealso::

    Рекомендую использовать эти шаблоны в отдельных модулях, в качестве подключаемых библиотек.
    Не нужно бездумно дублировать код в основной программе, мы же боремся с дублированием, а не преходим на его сторону.

.. seealso::

    ``configer tcode infile`` - это одноразовая команда, для того чтобы обновить блок кода
    используйте ``configer tcode upfile``

**Пример файла в который нужно вставить блок**

Путь к файлу ``/home/user/castom_lib.py``

:configer/test/in/public/tcode/infile.py:

.. literalinclude:: ../../configer/test/in/public/tcode/infile.py

По команде

.. code-block:: bash

    configer tcode infile /home/user/castom_lib.py


В итоге файл должен содержать

:configer/test/out/public/tcode/infile.py:

.. literalinclude:: ../../configer/test/out/public/tcode/infile.py


4 Авто обновление в файлах (``configer tcode upfile``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Допустим с течением времени мы изменили исходный код в файле с командами, и теперь нам нужно обновить код в сторонних
файлах. Информацию о том что блок кода различается мы получим из хеша.

Допустим мы изменили код в команде

:configer/test/in/public/tcode/upfile_conf.py:

.. literalinclude:: ../../configer/test/in/public/tcode/upfile_conf.py


Прошлый файл

:configer/test/out/public/tcode/infile.py:

.. literalinclude:: ../../configer/test/out/public/tcode/infile.py


Теперь, чтобы проверить и обновить файл(или рекурсивно всю папку)
выполним команду. В данном случае проверим все файлы имение расширение ``[.py, .md]``


.. code-block:: bash


    configer tcode upfile /home/user/ -t "py, md"


В итоге файл ``/home/user/castom_lib.py`` будет иметь следующие содержание

:configer/test/out/public/tcode/upfile.py:

.. literalinclude:: ../../configer/test/out/public/tcode/upfile.py

