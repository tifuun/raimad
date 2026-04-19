from typing import Tuple, Protocol, Literal, SupportsFloat, TypeAlias, runtime_checkable

Num: TypeAlias = float | int | SupportsFloat

@runtime_checkable
class Vec2(Protocol):
    def __getitem__(self, i: Literal[0, 1]) -> Num: ...

def print_coords(vec2: Tuple[float, float]) -> None:
    print(vec2[0], vec2[1])

def print_coords2(vec2: Vec2) -> None:
    print(vec2[0], vec2[1])

mytup = (1, 2)
mylist = [1, 2]

print_coords(mytup)
# print_coords(mylist)  <-- wont work

print_coords2(mytup)
print_coords2(mylist)

