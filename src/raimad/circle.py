import numpy as np
import raimad as rai

class Circle(rai.Compo):
    """
    Circle

    A polygon that approximates a circle,
    defined by the radius and number of points.
    """
    browser_tags = ["builtin", "polygon"]

    class Options:
        radius = rai.Option('Circle radius', browser_default=15)
        num_points = rai.Option('Number of points')

    def _make(self, radius: float, num_points: int = 200):

        self.geoms.update({
            'root': [
                np.array([
                    rai.polar(angle, radius)
                    for angle
                    in np.linspace(0, 2 * np.pi, num_points)
                    ])
                ]
            })

        self.marks.center = (0, 0)

