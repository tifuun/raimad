"""rectwire.py: home to RectWire compo and relevant exceptions."""

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self


import raimad as rai
from raimad.types import Vec2, Num

class RectWire(rai.Compo):
    """A rectangle defined by two points and a thickness."""

    browser_tags = ["builtin", "polygon"]

    class Options:
        p1 = rai.Option('First point', browser_default=(0, 0))
        p2 = rai.Option('Second point', browser_default=(10, 10))
        width = rai.Option('Thickness', browser_default=2)

    def _make(
            self,
            p1: Vec2,
            p2: Vec2,
            width: Num,
            ) -> None:
        """
        Make RectWire betweent two points.

        Parameters
        ----------
        p1
            The first point
        p2
            The second point
        width
            Width of rectwire

        Returns
        -------
        Self
            The newly construct RectWire object
        """

        p1 = rai.vec2s(p1)
        p2 = rai.vec2s(p2)
        width = float(width)

        angle = rai.angle_between(p1, p2)

        step = rai.polar(
            arg=angle + rai.quartercircle,
            mod=width / 2
            )

        self.geoms.update({
            'root': [
                [
                    (p1[0] + step[0], p1[1] + step[1]),
                    (p1[0] - step[0], p1[1] - step[1]),
                    (p2[0] - step[0], p2[1] - step[1]),
                    (p2[0] + step[0], p2[1] + step[1]),
                    ]
                ]
            })

    @classmethod
    def from_points(
            cls,
            p1: Vec2,
            p2: Vec2,
            width: Num,
            ) -> Self:
        """
        Make RectWire betweent two points.

        Parameters
        ----------
        p1
            The first point
        p2
            The second point
        width
            Width of rectwire

        Returns
        -------
        Self
            The newly construct RectWire object
        """
        return cls(p1, p2, width)

    @classmethod
    def from_polar(
            cls,
            p1: Vec2,
            angle: Num,
            length: Num,
            width: Num,
            ) -> Self:
        """
        Make RectWire from polar coordinates.

        Parameters
        ----------
        p1
            Point where the RectWire starts
        angle
            Angle of rectwire
            in [numpy convention](coords-transforms.md)
        length
            Length of rectwire
        width
            Width of rectwire

        Returns
        -------
        Self
            The newly construct RectWire object
        """
        p1 = rai.vec2s(p1)
        p2 = rai.vec2s(p1)

        step = rai.polar(angle, length)
        p2 = (
            p1[0] + step[0],
            p1[1] + step[1],
            )
        return cls(p1, p2, width)

