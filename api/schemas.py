from drf_spectacular.utils import (
                                   OpenApiExample,
                                   OpenApiResponse,
                                   extend_schema,
)

from api.serializers import CategorySerializer

resp_val = {
    204: OpenApiResponse(description='No Content'),
    400: OpenApiResponse(description='Error: Bad Request.'),
    401: OpenApiResponse(description='Error: Unauthorized.'),
    404: OpenApiResponse(description='Error: Not Found.'),
}


product = {
    'properties': {
        'id': {'type': 'integer'},
        'name': {'type': 'string'},
        'slug': {'type': 'string'},
        'category': {'type': 'string'},
        'subcategory': {'type': 'string'},
        'price': {'type': 'string'},
        'images': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'size': {'type': 'string'},
                    'url': {'type': 'string'},
                },
            },
        },
    },
}

"""Схема для добавления товара в корзину."""
create_cart_product = extend_schema(
    tags=['cart'],
    summary='В корзину.',
    description='Добавить товар в корзину.',
    responses={
            200: {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'product': product,
                    'count': {'type': 'integer'},
                    'total_price': {'type': 'integer'},
                },
            },
        400: resp_val[400],
        401: resp_val[401],
    },
    examples=[
        OpenApiExample(
            name='Cart product add',
            summary='Добавить товар в корзину',
            value={'product': 2, 'count': 3},
            request_only=True,
            status_codes=['201'],
        ),
    ],
)


"""Схема для обновления количества товара в корзине."""
update_count_cart_product = extend_schema(
    tags=['cart'],
    summary='Изменить количество.',
    description='Изменение количества товара в корзине.',
    responses={
        200: {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'product': product,
                    'count': {'type': 'integer'},
                    'total_price': {'type': 'integer'},
                },
        },
        400: resp_val[400],
        401: resp_val[401],
        404: resp_val[404],
    },
    examples=[
        OpenApiExample(
            name='Cart product edit count',
            summary='Изменить количество',
            value={'count': 5},
            request_only=True,
            status_codes=['200'],
        ),
    ],
)

"""Схема для удаления товара из корзины."""
delete_product_in_cart = extend_schema(
    tags=['cart'],
    summary='Удалить товар.',
    description='Удалить товар из корзины.',
    responses={
        204: resp_val[204],
        401: resp_val[401],
        404: resp_val[404],
    },
)

"""Схема для очистки корзины."""
clear_cart = extend_schema(
    tags=['cart'],
    summary='Очистить корзину.',
    description='Удалить все товары из корзины.',
    responses={
        204: resp_val[204],
        401: resp_val[401],
    },
)

"""Схема для просмотра корзины с итогами."""
view_cart = extend_schema(
    tags=['cart'],
    summary='Показать корзину.',
    description='Просмотр товаров в корзине с общими итогами.',
    responses={
        200: {
            'type': 'object',
            'properties': {
                'cart': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'product': product,
                            'count': {'type': 'integer'},
                            'total_price': {'type': 'integer'},
                        },

                    },

                },
                'total_in_cart': {
                    'type': 'object',
                    'properties': {
                        'total_quantity': {'type': 'integer'},
                        'total_amount': {'type': 'integer'},
                    },
                },
            },


        },
        401: resp_val[401],
    },
)
"""Схема для просмотра всех категорий."""
view_categories = extend_schema(
    tags=['categories'],
    summary='Показать все категории.',
    description='Просмотр всех категорий с подкатегориями каталога товаров.',
)

"""Схема для просмотра одной категории."""
retrieve_category = extend_schema(
    tags=['categories'],
    summary='Показать категорию.',
    description='Просмотр выбранной категории '
    'с подкатегориями каталога товаров.',
    responses={
        200: OpenApiResponse(CategorySerializer),
        404: resp_val[404],
    },
)

"""Схема для просмотра всех товаров."""
view_products = extend_schema(
    tags=['products'],
    summary='Показать все товары.',
    description='Просмотр всех товаров в каталоге.',
)

"""Схема для просмотра одного товара."""
retrieve_product = extend_schema(
    tags=['products'],
    summary='Показать товар.',
    description='Просмотр выбранного товара из каталога.',
    responses={
        200: {
            'type': 'object',
            **product,
        },
        404: resp_val[404],
    },
)
