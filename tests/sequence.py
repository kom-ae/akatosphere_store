from itertools import chain


def get_sequence(n):
    return ''.join(map(str, chain.from_iterable(
        [i] * i for i in range(1, n+1)))
        )


while True:
    n = int(input("Сколько элементов вывести? "))
    print(get_sequence(n))
