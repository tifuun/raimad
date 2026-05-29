from typing import Callable, Iterable, TypeVar, Self, Protocol, Any

O = TypeVar('O')
T = TypeVar('T')

def duplicate(
        lst: list[T],
        constructor: Callable[[list[T]], O] = list
        ) -> O:
    return constructor([*lst, *lst])

print(duplicate([1,2,3]))
print(duplicate([1,2,3], tuple))
print(duplicate([1,2,3], list))



