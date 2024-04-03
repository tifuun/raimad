import numpy as np
import pycif as pc

class Circle(pc.Compo):
    """
    Circle

    A polygon that approximates a circle,
    defined by the radius and number of points.
    """
    browser_tags = ["builtin", "polygon"]

    class Options:
        radius = pc.Option('Circle radius', browser_default=15)
        num_points = pc.Option('Number of points')

    def _make(self, radius: float, num_points: int = 200):

        self.geoms.update({
            'root': [
                np.array([
                    pc.polar(angle, radius)
                    for angle
                    in np.linspace(0, 2 * np.pi, num_points)
                    ])
                ]
            })

        self.marks.center = (0, 0)

