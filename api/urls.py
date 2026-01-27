from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ProductViewSet, CategoryViewSet, CartViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('products', ProductViewSet, basename='products')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('cart', CartViewSet, basename='cart')


urlpatterns_v1 = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1))
]
