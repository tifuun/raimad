"""rectwire.py: home to RectWire compo and relevant exceptions."""

import raimad as rai

class RectWireError(Exception):
    """Generic error when creating RectWire."""

class RectWireTooManyArgumentsError(RectWireError):
    """Too many arguments passed to RectWire."""

class RectWireNotEnoughArgumentsError(RectWireError):
    """Not enough arguments passed to RectWire."""

class RectWireIncorrectArgumentsError(RectWireError):
    """Incorrect combination of arguments passed to RectWire."""

class RectWire(rai.Compo):
    """A rectangle defined by two points and a thickness."""

    browser_tags = ["builtin", "polygon"]

    class Options:
        p1 = rai.Option('First point', browser_default=(0, 0))
        p2 = rai.Option('Second point', browser_default=(10, 10))
        width = rai.Option('Thickness', browser_default=2)

    def _make(
            self,
            /,
            p1: 'rai.typing.Point',
            p2: 'rai.typing.Point | None' = None,
            width: float = 0,
            *,
            angle: float | None = None,
            length: float | None = None
            ) -> None:

        p2, angle = self._interpret_args(p1, p2, angle, length)

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

    def _interpret_args(
            self,
            p1: 'rai.typing.Point',
            p2: 'rai.typing.Point | None',
            angle: float | None,
            length: float | None
            ) -> tuple['rai.typing.Point', float]:

        if p2 is None and angle is None and length is None:
            raise RectWireNotEnoughArgumentsError(
                "You must specify either an endpoint or angle and bearing "
                "in order to construct a RectWire."
                )

        if p2 is None and angle is None and length is not None:
            raise RectWireNotEnoughArgumentsError(
                "You passed a length, but not an angle. "
                "You must specify angle."
                )

        if p2 is None and angle is not None and length is None:
            raise RectWireNotEnoughArgumentsError(
                "You passed an angle, but not a length. "
                "You must specify length."
                )

        if p2 is None and angle is not None and length is not None:
            s = rai.polar(angle, length)
            p2 = (
                p1[0] + s[0],
                p1[1] + s[1],
                )
            return p2, angle

        if p2 is not None and angle is None and length is None:
            angle = rai.angle_between(p1, p2)
            return p2, angle

        if p2 is not None and angle is None and length is not None:
            raise RectWireIncorrectArgumentsError(
                "Pass either a startpoint and endpoint "
                "or startpoint, length, and angle."
                )

        if p2 is not None and angle is not None and length is None:
            raise RectWireIncorrectArgumentsError(
                "Pass either a startpoint and endpoint "
                "or startpoint, length, and angle."
                )

        if p2 is not None and angle is not None and length is not None:
            raise RectWireIncorrectArgumentsError(
                "Pass either a startpoint and endpoint "
                "or startpoint, length, and angle."
                )

        assert False

