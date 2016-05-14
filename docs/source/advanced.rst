Для опытных пользователей
=========================


Тонкая настройка
----------------

По умолчанию ``django_ulogin`` требует от сервиса только одно обязательное поле - ``email``. Вы можете указать для проекта список как необходимых полей (определив в ``settings`` список ``ULOGIN_FIELDS``), так и опциональных (``ULOGIN_OPTIONAL``):

.. code:: python

    # Поля first_name и last_name обязательны
    ULOGIN_FIELDS = ['first_name', 'last_name']

    #  Необязательные поля: пол, URL аватара, дата рождения
    ULOGIN_OPTIONAL = ['sex', 'photo', 'bdate']

Список всех полей, которые сообщает ULOGIN:

* ``first_name``
* ``last_name``
* ``email``
* ``nickname``
* ``bdate`` *(дата рождения, передаётся в формате dd.mm.yyyy)*
* ``sex`` *(пол: 1 означает женский, 2 - мужской)*
* ``photo`` *(аватар, размер 100х100 пикселей)*
* ``photo_big``
* ``city``
* ``country``
* ``phone``

Внешний вид виджета определяется параметром ``ULOGIN_DISPLAY``. Доступно три варианта:

* ``small`` *(по умолчанию)*
* ``panel``
* ``button``

Список используемых провайдеров определяется директивой ``ULOGIN_PROVIDERS``. По умолчанию включены:

* ``vkontakte``
* ``facebook``
* ``twitter``
* ``google``
* ``livejournal``

Дополнительные провайдеры, которые будут показаны внутри выпадающего меню, определяются в директиве ``ULOGIN_HIDDEN``. По умолчанию:

* ``yandex``
* ``odnoklassniki``
* ``mailru``
* ``openid``

Если при входе нужно выполнить какую-то JavaScript-функцию, укажите её в виде строки в переменной ``ULOGIN_CALLBACK``.

Если необходимо создать функцию, создающую пользователя Django (это полезно при использовании нестандартной модели), можно
указать полный путь до неё в переменной ``ULOGIN_CREATE_USER_CALLBACK`` (см. ниже)


Схемы
-----

Как упоминалось выше, в некоторых случаях нужно разместить на одной странице несколько виджетов ulogin с различными настройками. В этом случае целесообразно создать нужное количество схем и настроить их.

Схемы определяются как словарь ``ULOGIN_SCHEMES``, ключи которого — названия схем, используемые в шаблонном теге ``{% ulogin_widget "scheme_name" %}``, а значения - словари с настройками.

Ключи этого словаря совпадают с названиями соответствующих «глобальных» настроек, но без префикса ``ULOGIN_``. Это означает, что в пределах настройки схемы ключ ``DISPLAY`` будет отвечать за вид панели виджета, как и его глобальный «коллега» ``ULOGIN_DISPLAY``

Кроме того, настройки схем наследуют глобальные настройки. Например, такая настройка:

.. code:: python

    ULOGIN_PROVIDERS = ['google', 'twitter']
    ULOGIN_HIDDEN = ['odnoklassniki', 'mailru']
    ULOGIN_DISPLAY = 'panel'

    ULOGIN_SCHEMES = {
        'default': {'HIDDEN': ['yandex']},
        'comments': {'DISPLAY': 'small'}
    }

означает, что по умолчанию включены провайдеры ``google`` и ``twitter``, ``odnoklassniki`` и ``mailru`` скрыты, а виджет выводится в раскладке ``panel``.

Однако при использовании схемы ``default`` скрытым провайдером окажется ``yandex``, а схема ``comments`` будет выведена в раскладке ``small``. Настройки, которые не переопределены, будут браться из глобальной области.


Если в проекте используются бэкенды аутентификации, отличные от стандартных, можно указать настройку ``ULOGIN_AUTHENTICATION_BACKEND``, которая будет использована для хранения в сессии информации о том, через какой бэкенд аутентифицировался пользователь.


Сигналы
--------

При аутентификации пользователя создаётся новый Django-пользователь, ``username`` которого заполняется uuid4-хешем. Однако при создании новой аутентификации срабатывает сигнал ``django_ulogin.signals.assign``, в котором передаётся объект ``request``, пользователь Django, аутентификация и флаг ``registered`` , показывающий, была ли создана запись.

Чтобы сделать имя поля дружественным пользователю, достаточно создать объект, подписанный на сигнал ``django_ulogin.signals.assign``:

.. code:: python

    from django_ulogin.models import ULoginUser
    from django_ulogin.signals import assign

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
            user.username = json['username']
            user.first_name = json['first_name']
            user.last_name = json['last_name']
            user.email = json['email']
            user.save()


    assign.connect(receiver=catch_ulogin_signal,
                   sender=ULoginUser,
                   dispatch_uid='customize.models')

Можно изучить тестовый проект, в котором реализована функция сохранения данных, полученных от uLogin:

* https://github.com/marazmiki/django-ulogin/tree/master/test_project
* https://github.com/marazmiki/django-ulogin/blob/master/test_project/customize/models.py#L58


Создание нестандартной модели пользователя
------------------------------------------

По умолчанию при аутентификации пользователя через социальные сети будет создаваться стандартный пользователь Django; в качестве имени будет использоваться обрезанный до 30 символов (ограничение длины поля ``username`` в стандартной модели пользователя) UUID4-хеш.

Однако если Вы используете собственную модель, отличную от ``django.contrib.auth.models.User``, в которой содержатся другие поля, то можете написать собственную функцию, которая создавала бы пользователя по Вашему сценарию.

Требования к этой функции:

* она должна принимать два аргумента: ``request`` и ``ulogin_response`` для передачи объекта ``HttpRequest`` и ``JSON``, полученного от uLogin соответственно;
* возвращать сохранённую модель пользователя

Пример:

.. code:: python

    from my_projects.models import MyUser

    def my_user_create(request, ulogin_response):
        return MyUser.objects.create_user(
            username='Vasya_' + uuid.uuid4().hex, 
            birthday=datetime.date.today()
        )


После этого в настройках проекта в переменной ``ULOGIN_CREATE_USER_CALLBACK`` указать полный путь этой функции:

.. code:: python

    ULOGIN_CREATE_USER_CALLBACK = "my_projects.utils.my_user_create"
