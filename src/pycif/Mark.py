import numpy as np

class Mark:
    def __init__(self, compo, point):
        self.point = np.array(point)
        self.compo = compo

    def __array__(self):
        return self.point

    def __class_getitem__(cls, key):
        return "It works"  # TODO

