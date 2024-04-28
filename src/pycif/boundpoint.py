import numpy as np

# see
# https://numpy.org/doc/stable/user/basics.subclassing.html
class BoundPoint(np.ndarray):

    def __new__(cls, input_array, proxy):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj.proxy = proxy
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None:
            return
        self.proxy = getattr(obj, 'proxy', None)

    def to(self, point):
        self.proxy.transform.move(
            point[0] - self[0],
            point[1] - self[1],
            )
        return self

    def rotate(self, angle: float):
        self.proxy.transform.rotate(
            angle,
            self[0],
            self[1]
            )

