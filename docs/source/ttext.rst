Шаблонный текст
---------------

1 Файл с шаблонами (``configer ttext``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Для того чтобы указать какие переменные нужно рассматривать в качестве команд, их нужно поместить в переменную
``EXPORT_TEMPLATE``, переменная с конфигурациями должна соответствовать правилам, это должен быть картеж со следующим порядком
значений: :class:`logic_helpful.spec_name`, эти значения подставится в :meth:`logic_ttext.ttextLogic.parse_export`

У вас есть следующие возможности:

- Одинаковые ключевые имена имеют одинаковые значения.
- Возможность переопределять значение ключей. Ключи которые не переопределены становится значениями по умолчанию.
- Одни и те же ключевые имена могу по разному оформляться. Эту логику пользователь может как угодно реализовывать через функции. Для того чтобы обработать ключевое имя через функции нужно написать в шаблоне ``$$(ИмяКлюча|ИмяФункции)$$``, и передать последним значением словарь ``{"ИмяФункции": СсылкаНаФункцию}``. Ссылка на функцию должна быть типа ``typing.Callable[[str, dict[str, str], str], str]``.

:configer/test/in/public/ttext/conf.py:
.. literalinclude:: ../../configer/test/in/public/ttext/conf.py

Выполним команду

.. code-block:: bash

    configer ttext "pytest"               \
    -k "name=sum"                         \
    -k "doc=Тестирование суммирования"    \
    -k "args=a, b, c"



В итоге получим

:configer/test/out/public/ttext/template.py:
.. literalinclude:: ../../configer/test/out/public/ttext/template.py