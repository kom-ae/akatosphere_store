import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse
from rest_framework.test import APIClient

from cart.models import Cart

User = get_user_model()


@pytest.fixture(autouse=True)
def load_fixtures(django_db_setup, django_db_blocker):
    """Автоматически загружает фикстуры перед тестами."""
    with django_db_blocker.unblock():
        call_command(
            'loaddata',
            'fixtures/full_no_image_db.json'
        )


@pytest.fixture
def password():
    return '12345'


@pytest.fixture
def test_user(password):
    """Создать тестового пользователя."""
    return User.objects.create_user(username='testuser', password=password)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, password):
    """Верни авторизованный api клиент."""
    url = reverse('api:jwt-create')
    response = api_client.post(
        url,
        {'username': 'testuser', 'password': password},
        format='json'
    )
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def data():
    return {
        'product_id': 2,
        'count': 22
    }


@pytest.fixture
def cart_add(test_user, data):
    Cart.objects.create(user=test_user, **data)
