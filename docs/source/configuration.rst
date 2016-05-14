Конфигурация проекта
====================

Для подключения к проекту откройте ``settings.py`` и добавьте в кортеж ``INSTALLED_APPS`` приложение ``django_ulogin``

.. code:: python

    INSTALLED_APPS += (
        'django_ulogin', 
    )

Для работы django-ulogin необходим подключенный контекст-процессор ``django.core.context_processors.request``. Обратите внимание, что по умолчанию в файле ``settings.py`` параметр ``TEMPLATE_CONTEXT_PROCESSORS`` отсутствует. Добавьте следующие строки в ``settings``, если их там нет:

.. code:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.request',
        'django.contrib.messages.context_processors.messages',
    )

Добавьте схему URL-адресов к списку ``urlpatterns`` Вашего проекта (``urls.py``):

.. code:: python

    urlpatterns += patterns('',
        url(r'^ulogin/', include('django_ulogin.urls')),
    )

Затем следует синхронизировать базу данных

.. code:: bash

    $ ./manage.py syncdb

