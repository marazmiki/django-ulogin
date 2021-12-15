Конфигурация проекта
====================

Для подключения к проекту откройте ``settings.py`` и добавьте в список ``INSTALLED_APPS`` приложение ``django_ulogin``

.. code:: python

    INSTALLED_APPS += [
        'django_ulogin'
    ]

.. attention::

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


Добавьте схему URL-адресов к списку ``urlpatterns`` Вашего проекта (``urls.py``):

.. code:: python

    urlpatterns += [
        url(r'^ulogin/', include('django_ulogin.urls')),
    ]


Затем следует синхронизировать базу данных

.. code:: bash

    $ ./manage.py migrate

Вроде всё, можно и запускаться.
