Конфигурация проекта
====================

Для подключения к проекту откройте ``settings.py`` и добавьте в кортеж ``INSTALLED_APPS`` приложение ``django_ulogin``

.. code:: python

    INSTALLED_APPS += [
        'django_ulogin'
    ]

.. attention::

    Атрибут ``INSTALLED_APPS`` по умолчанию стал списком (``list``) начиная с Django версии ``1.9``. В более ранних версиях он является кортежем (``tuple``), поэтому, если Вы не изменяли тип, добавлять надо кортеж:

    .. code:: python

        INSTALLED_APPS += (
            'django_ulogin'
        )

Для работы ``django-ulogin`` необходим подключенный контекст-процессор ``django.template.context_processors.request``:

.. code:: python

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    # ...
                    'django.template.context_processors.request',
                ],
            },
        },
    ]


.. attention::

    В старых версих Django до версии 1.9 включительно, не было поддержки нескольких систем рендеринга шаблонов,
    а требуемый контекст-процессор располагался в ``django.core.context_processors.request``. Таким образом,
    подключение выглядит примерно следующим образом:


        TEMPLATE_CONTEXT_PROCESSORS = (
            # ...
            'django.core.context_processors.request',
        )

Добавьте схему URL-адресов к списку ``urlpatterns`` Вашего проекта (``urls.py``):

.. code:: python

    urlpatterns += [
        url(r'^ulogin/', include('django_ulogin.urls')),
    ]


Затем следует синхронизировать базу данных

.. code:: bash

    $ ./manage.py migrate
