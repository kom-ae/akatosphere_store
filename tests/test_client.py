from http import HTTPStatus

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestCart:
    """Протестируй корзину."""

    def test_unauthorized_access(self, api_client):
        """Без токена доступ запрещён."""
        url = reverse('api:cart-view')
        response = api_client.get(url)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @pytest.mark.usefixtures('test_user')
    def test_authorized_access(self, authenticated_api_client):
        """Запрос данных с валидным токеном к пустой корзине."""
        url = reverse('api:cart-view')
        response = authenticated_api_client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert len(response.data['cart']) == 0

    @pytest.mark.usefixtures('test_user')
    def test_add_cart(self, authenticated_api_client):
        """Добавление товара в корзину."""
        url = reverse('api:cart-list')
        data = {
            'product': 2,
            'count': 22
        }
        response = authenticated_api_client.post(url, data, format='json')
        assert response.status_code == HTTPStatus.CREATED
        assert response.data['product']['id'] == 2

    @pytest.mark.usefixtures('test_user')
    def test_authorized_access_cart(self, authenticated_api_client, cart_add):
        """Запрос данных с валидным токеном к корзине с одним товаром."""
        url = reverse('api:cart-view')
        response = authenticated_api_client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert len(response.data['cart']) == 1


class TestCatalog:
    """Протестируй каталог."""

    def test_unauthorized_access_categories(self, api_client):
        """Доступ к категориям неавторизованным пользователем."""
        url = reverse('api:categories-list')
        response = api_client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert response.data['count'] == 5

    def test_unauthorized_access_products(self, api_client):
        """Доступ к продуктам неавторизованным пользователем."""
        url = reverse('api:products-list')
        response = api_client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert response.data['count'] == 30
