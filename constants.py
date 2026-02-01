# Максимальная длина названия
MAX_LENGTH_NAME: int = 128

# Максимальная длина slug поля
MAX_LENGTH_SLUG: int = MAX_LENGTH_NAME * 2 + 1

# Количество слов в строке для представления объекта.
COUNT_WORD_IN_VIEW_OBJECT: int = 5

# Пагинация. Количество элементов на страницу.
PAGINATION_PAGE_SIZE: int = 10

# Количество цифр в цене товара
DECIMAL_MAX_DIGITS: int = 10
# Количество цифр в цене товара после запятой
DECIMAL_PLACES: int = 2

# Срок жизни токена в минутах
ACCESS_TOKEN_LIFETIME: int = 20

# -----------Настройки IMAGEKIT-----------

# Формат миниатюр ('JPEG', 'PNG', ...)
IMAGEKIT_FORMAT: str = 'JPEG'
# Дополнительные опции
IMAGEKIT_OPTIONS: dict[str, int] = {'quality': 90}
# Размер маленькой картинки
SIZE_SMALL_IMAGE: tuple[int, int] = (50, 50)
# Размер средней картинки
SIZE_MEDIUM_IMAGE: tuple[int, int] = (300, 300)
# Размер большой картинки
SIZE_BIG_IMAGE: tuple[int, int] = (1000, 1000)
# Каталог хранения кэша изображений
IMAGEKIT_CACHEFILE_DIR: str = 'CACHE'
