from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema, extend_schema_view)

"""Схема для добавления продукта в корзину"""
create_cart_product = extend_schema(
    summary='В корзину.',
    description='Добавить продукт в корзину.',
    responses={
            200: {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'product': {
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'slug': {'type': 'string'},
                            'category': {'type': 'string'},
                            'subcategory': {'type': 'string'},
                            'price': {'type': 'string'},
                            'images': {
                                'type': 'array',
                                'items': {'type': 'string'}
                            },
                        },
                    },
                    'count': {'type': 'integer'}
                }
            },
        400: OpenApiResponse(description='Error: Bad Request.')
    },
    examples=[
        OpenApiExample(
            name='Cart product add',
            summary='Добавить продукт в корзину',
            value={'product': 2, 'count': 3},
            request_only=True,
            status_codes=['201']
        )
    ]
)
