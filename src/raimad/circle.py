"""circle.py: home to Circle builtin component."""

from math import pi
import raimad as rai

class Circle(rai.Compo):
    """A polygon that approximates a circle."""

    browser_tags = ["builtin", "polygon"]

    class Options:
        radius = rai.Option('Circle radius', browser_default=15)
        num_points = rai.Option('Number of points')

    def _make(self, radius: float, num_points: int = 200) -> None:

        self.geoms.update({
            'root': [
                [
                    rai.polar(angle / num_points * 2 * pi, radius)
                    for angle
                    in range(0, num_points)
                    ]
                ]
            })

        self.marks.center = (0, 0)

