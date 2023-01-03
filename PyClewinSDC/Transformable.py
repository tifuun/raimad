"""
Utility class for creating classes that encapsulate a Transform
"""

from PyClewinSDC.Transform import Transform


class Transformable(object):
    def __init__(self, transform=None):
        if transform is None:
            self.transform = Transform()
        else:
            self.transform = transform.copy()

    def apply_transform(self, transform):
        """
        Apply a Transform to this polygon
        """
        self.transform.apply_transform(transform)
        return self

    def move(self, x, y):
        """
        Move horizontally or vertically
        """
        self.transform.move(x, y)
        return self

    def movex(self, x):
        """
        Move horizontally
        """
        self.transform.movex(x)
        return self

    def movey(self, y):
        """
        Move vertically
        """
        self.transform.movey(y)
        return self

    def scale(self, x, y=None):
        """
        Apply scaling factor.
        Either pass one argument, or
        two separate arguments for horizontal and vertical factor
        """
        self.transform.scale(x, y)
        return self

    def rot(self, degrees):
        """
        Rotate by a fixed number of degrees
        """
        self.transform.rot(degrees)
        return self

    def hflip(self):
        """
        Horizontal flip
        """
        self.transform.hflip()
        return self

    def vflip(self):
        """
        Vertical flip
        """
        self.transform.vflip()
        return self

    def flip(self):
        """
        Vertical flip, then horizontal flip.
        """
        self.transform.flip()
        return self

