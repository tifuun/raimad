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
        return self.proxy

    def rotate(self, angle: float):
        self.proxy.transform.rotate(
            angle,
            self[0],
            self[1]
            )
        return self.proxy

    def move(self, x, y):
        """
        `move`ing a boundpoint is functionally identical to `move`ing
        the proxy itself, so there is no reason to call this explicitly.
        However, this function is still defined, so that you can use
        `move` in a chain of actions on a boundpoint
        """
        self.proxy.transform.move(x, y)
        return self.proxy

    # TODO the rest of the functions

