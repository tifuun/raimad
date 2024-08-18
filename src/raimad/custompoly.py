"""custompoly.py: home to CustomPoly builtin component."""
import raimad as rai

from typing import Sequence

class CustomPolyException(Exception):
    """Error for when you incorrectly create a CustomPoly."""

class CustomPoly(rai.Compo):
    """
    A polygon that you can defined on-the fly.

    #TODO add example
    """

    browser_tags = ["builtin", "polygon"]

    class Options:
        points = rai.Option(
            "A list of points for the polygon",
            browser_default=[
                [0, 0],
                [10, 0],
                [10, 20],
                [20, -20],
                ]
            )

    def _make(
            self,
            points: Sequence[
                tuple[float, float]
                |
                tuple[str, tuple[float, float]]
                ]
            ) -> None:
        processed_points: 'list[rai.typing.Point]' = []
        for point in points:

            if isinstance(point[0], str):
                self.marks[point[0]] = point[1]
                processed_points.append(point[1])

            else:
                processed_points.append(point)

        self.geoms.update({'root': [processed_points]})

