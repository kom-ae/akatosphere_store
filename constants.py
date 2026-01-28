# Максимальная длина названия
MAX_LENGTH_NAME: int = 128

# Количество слов в строке для представления объекта.
COUNT_WORD_IN_VIEW_OBJECT: int = 5

# Пагинация. Количество элементов на страницу.
PAGINATION_PAGE_SIZE = 5

# Количество цифр в цене товара
DECIMAL_MAX_DIGITS = 10
# Количество цифр в цене товара после запятой
DECIMAL_PLACES = 2

# -----------Настройки IMAGEKIT-----------

# Формат миниатюр ('JPEG', 'PNG', ...)
IMAGEKIT_FORMAT: str = 'JPEG'
# Дополнительные опции
IMAGEKIT_OPTIONS: dict[str, int] = {'quality': 90}
# Размер маленькой картинки
SIZE_SMALL_IMAGE: tuple[int, int] = (50, 50)
# Размер средней картинки
SIZE_MEDIUM_IMAGE: tuple[int, int] = (150, 150)
# Размер большой картинки
SIZE_BIG_IMAGE: tuple[int, int] = (250, 250)
# Каталог хранения кэша изображений
IMAGEKIT_CACHEFILE_DIR = 'CACHE'
