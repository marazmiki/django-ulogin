import pytest

PASSWORD = "17wa5ag00dday"


@pytest.fixture
def john(db, django_user_model):
    """
    Creates and returns "john" user
    """
    return django_user_model.objects.create_user(username="john",
                                                 password=PASSWORD,
                                                 email="john@example.com")


@pytest.fixture
def jane(db, django_user_model):
    """
    Creates and returns "jane" user
    """
    return django_user_model.objects.create_user(username="jane",
                                                 password=PASSWORD,
                                                 email="jane@example.com")


@pytest.fixture
def ulogin_postback_url():
    return ""


@pytest.fixture
def response():
    """
    Emulates JSON response from ulogin serivce for test purposes
    """
    return {
        "network": "vkontakte",
        "identity": "https://vk.com/id12345",
        "uid": "12345",
        "email": "demo@demo.de",
        "first_name": "John",
        "last_name": "Doe",
        "bdate": "01.01.1970",
        "sex": "2",
        "photo": "https://www.google.ru/images/srpr/logo3w.png",
        "photo_big": "https://www.google.ru/images/srpr/logo3w.png",
        "city": "Washington",
        "country": "United States",
    }


@pytest.fixture
def response_mocker(monkeypatch, response):
    """
    Mock the response
    """
    class Mocker:
        def apply(self, override=None):
            pass

        @property
        def response_data(self):
            return response

    return Mocker()
