import math

class PieceOfPi:
    def __init__(self, halves=2):
        self.halves = halves

    def __mul__(self, other):
        return type(self)(halves=self.halves * other)

    def __truediv__(self, other):
        return type(self)(halves=self.halves / other)

    def __add__(self, other):
        if not isinstance(other, type(self)):
            return self.as_float() + other
        return type(self)(halves=self.halves + other.halves)

    def __sub__(self, other):
        if not isinstance(other, type(self)):
            return self.as_float() - other
        return type(self)(halves=self.halves - other.halves)

    def __rmul__(self, other):
        return type(self)(halves=other * self.halves)

    def __rtruediv__(self, other):
        return type(self)(halves=other / self.halves)

    def __radd__(self, other):
        if not isinstance(other, type(self)):
            return other + self.as_float()
        return type(self)(halves=other.halves + self.halves)

    def __rsub__(self, other):
        if not isinstance(other, type(self)):
            return other - self.as_float()
        return type(self)(halves=other.halves - self.halves)

    def as_float(self):
        return math.pi * self.halves / 2

def sin(num):
    if isinstance(num, PieceOfPi):
        if num.halves % 4 == 0:
            return 0
        elif num.halves % 4 == 1:
            return 1
        elif num.halves % 4 == 2:
            return 0
        elif num.halves % 4 == 3:
            return -1

        num = num.as_float()

    return math.sin(num)


def cos(num):
    if isinstance(num, PieceOfPi):
        if num.halves % 4 == 0:
            return 1
        elif num.halves % 4 == 1:
            return 0
        elif num.halves % 4 == 2:
            return -1
        elif num.halves % 4 == 3:
            return 0

        num = num.as_float()

    return math.cos(num)

