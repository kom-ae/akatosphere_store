import pytest

from http import HTTPStatus
from django.urls import reverse
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def test_user():
    user = User.objects.create(
        username='testuser',
        # email='test@example.com'
    )
    user.password = make_password('пароль')
    user.save()
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    return client.force_authenticate(user=user)


@pytest.fixture
def authenticated_api_client(api_client):
    url = reverse('api:jwt-create')
    response = api_client.post(
        reverse,
        {'username': 'testuser', 'password': 'пароль'},
        format='json'
    )
    token = response.data['access']
    return api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


class TestClient:

    def test_client(self, api_client, db):
        url = reverse('api:categories-list')
        response = api_client.get(url)
        print(response)
        assert True

    def test_get_cart(authenticated_api_client):
        url = reverse('api:cart-view')
        response = authenticated_api_client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert response.data['count'] == 0
