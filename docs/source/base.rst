Системные требования
====================

* Разработка и тестирование проводилось под управлением OS Ubuntu, Debian, Mac OS. Production-использование — Ubuntu, Debian, RHEL, FreeBSD. Приложение не использует каких-либо специфичных для той или иной операционной системы особенностей языка, поэтому, скорее всего, всё будет работать и на остальных системах, для которых существуют требуемые версии Python
* Интерпретатор Python ``2.7+``, ``3.4``, ``3.5``, ``3.6``. На других интерпретаторах работоспособность не проверялась.
* ``Django 1.7+``, включая поддержку ``Django 2.x`` (доступно только для ``Python 3.4+``)
* Библиотека `python-requests <https://docs.python-requests.org/en/master/>`_

Установка
=========

Установка текущей стабильной версии django-ulogin производится из `PyPI <https://pypi.python.org>`_ с помощью утилиты ``pip``:

.. code:: bash

    $ pip install django-ulogin

Для установки dev-верии из репозитория нужно добавить к командной строке ключ ``-e``:

.. code:: bash

    $ pip install -e git+github.com/marazmiki/django-ulogin.git#egg=django-ulogin

Если нужно установить какую-то конкретную ревизию, просто укажите её в URL репозитория:

.. code:: bash

    $ pip install -e git+github.com/marazmiki/django-ulogin.git@{rev}#egg=django-ulogin

Все внешние зависимости будут утановлены автоматически
