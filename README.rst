django-ulogin
=============

Django-ulogin является приложением для социальной аутентификации пользователей с помощью интернет-сервиса `ULOGIN.RU <http://ulogin.ru>`_

Требования
-----------
- Python 2.6 и выше;
- Django Framework версии 1.3.1;
- requests версии 0.7.4 или выше;
- mock версии 0.8.0 (используется только для запуска тестов.

Лицензия
--------
Распространяется по лицензии MIT


Установка
----------

1. Установка пакета ``django-ulogin`` производится утилитой ``pip``.

    pip install django-ulogin

2. Откройте ``settings.py`` и добавьте в ``INSTALLED_APPS`` приложение ``django_ulogin``

    INSTALLED_APPS += ('django_ulogin', )

3. Для работы django-ulogin необходим подключенный контекст-процессор ``django.core.context_processors.request``. Обратите внимание, что по умолчанию в файле ``settings.py`` параметр ``TEMPLATE_CONTEXT_PROCESSORS`` отсутствует. Добавьте следующие строки в ``settings``, если их там нет:

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.request',
        'django.contrib.messages.context_processors.messages',
    )

4. Добавьте схему URL-адресов к списку ``urlpatterns`` Вашего проекта (``urls.py``):

    urlpatterns += patterns('',
        url(r'^ulogin/', include('django_ulogin.urls')),
    )

5. Выполните синхронизацию базы данных

    ./manage.py syncdb


Использование
-------------

Для использования приложения достаточно в любом месте шаблона вставить подключение шаблонной библиотеки ``ulogin_tags`` и вызов тега ``ulogin_widget``.

    {% load ulogin_tags %}
    {% ulogin_widget %}


На месте тега ``ulogin_widget`` при рендеринге появится код интеграции Вашего сайта c ULOGIN.

В случае необходимости можно разместить несколько виджетов на одной странице, причём настройки для каждого виджета могут быть индивидуальными (см. ниже). При использовании схемы, вызов виджета будет выглядеть следующим образом:

    {% load ulogin_tags %}
    {% ulogin_widget "scheme_name" %}


Тонкая настройка
----------------

По умолчанию ``django_ulogin`` требует от сервиса только одно обязательное поле - ``email``. Вы можете указать для проекта список как необходимых полей (определив в ``settings`` список ``ULOGIN_FIELDS``), так и опциональных (``ULOGIN_OPTIONAL``):

    # Поля first_name и last_name обязательны
    ULOGIN_FIELDS = ['first_name', 'last_name']

    #  Необязательные поля: пол, URL аватара, дата рождения
    ULOGIN_OPTIONAL = ['sex', 'photo', 'bdate'] 

Список всех полей, которые сообщает ULOGIN:

- first_name
- last_name
- email
- nickname
- bdate *(дата рождения, передаётся в формате dd.mm.yyyy)*
- sex *(пол: 1 означает женский, 2 - мужской)*        
- photo *(аватар, размер 100х100 пикселей)*    
- photo_big  
- city
- country
- phone Телефон

Настройка виджета производится при помощи схем, которые могут быть определены в словаре ``ULOGIN_SCHEMES``. Базовой схемой для всех виджетов является схема 'default'. Определение нескольких схем может быть полезно при использовании нескольких виджетов на одной странице.

Внешний вид виджета определяется параметром ``DISPLAY``. Доступно три варианта:

- panel
- small *(по умолчанию)*
- button

Список используемых провайдеров определяется директивой ``PROVIDERS``. По умолчанию включены:

- vkontakte
- facebook
- twitter
- google
- livejournal

Дополнительные провайдеры, которые будут показаны внутри выпадающего меню, определяются в директиве ``HIDDEN``. По умолчанию:

- yandex
- odnoklassniki
- mailru
- openid

Полный список поддерживаемых провайдеров можно уточнить на сайте http://ulogin.ru
Пример определения схем:

    ULOGIN_SCHEMES = {
        # базовая схема
        'default':{
            'DISPLAY'   : 'panel',
            'PROVIDERS' : ["vkontakte", "facebook", "twitter", "google"],
            'HIDDEN'    : ["yandex", "mailru"],
        },
        # дополнительная схема
        'comment':{
            'DISPLAY'   : 'small',
            'PROVIDERS' : ["vkontakte", "facebook", "twitter", "google", "yandex", "mailru"],
            'HIDDEN'    : [],
        }
    }

Если при входе нужно выполнить какую-то JavaScript-функцию, укажите её в виде строки в переменной ``ULOGIN_CALLBACK``.


Сигналы
-------

При аутентификации пользователя создаётся новый Django-пользователь, ``username`` которого заполняется uuid4-хешем. Однако при создании новой аутентификации срабатывает сигнал ``django_ulogin.signals.assign``, в котором передаётся объект ``request``, пользователь Django, аутентификация и флаг того, была ли создана запись.

Чтобы сделать имя поля дружественным пользователю, достаточно создать объект, подписанный на сигннал ``django_ulogin.signals.assign``:

    def catch_ulogin_signal(*args, **kwargs):
        """
        Обновляет модель пользователя: исправляет username, имя и фамилию на 
        полученные от провайдера.

        В реальной жизни следует иметь в виду, что username должен быть уникальным,
        а в социальной сети может быть много "тёзок" и, как следствие,
        возможно нарушение уникальности.

        """
        user=kwargs['user']
        json=kwargs['ulogin_data']

        if kwargs['registered']:
            user.username=json['username']
            user.first_name=json['first_name']
            user.last_name=json['last_name']
            user.email=json['email']
            user.save()

    from django_ulogin.models import ULoginUser

    assign.connect(receiver = catch_ulogin_signal,
                   sender   = ULoginUser,
                   dispatch_uid = 'customize.models')


Можно изучить тестовый проект, в котором реализована функция сохранения данных, полученных от ULogin:

- https://github.com/marazmiki/django-ulogin/tree/master/test_project
- https://github.com/marazmiki/django-ulogin/blob/master/test_project/customize/models.py#L47
