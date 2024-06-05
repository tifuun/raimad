import raimad as rai

class RectWireError(Exception):
    pass

class RectWireTooManyArgumentsError(RectWireError):
    pass

class RectWireNotEnoughArgumentsError(RectWireError):
    pass

class RectWireIncorrectArgumentsError(RectWireError):
    pass

class RectWire(rai.Compo):
    """
    RectWire

    A rectangle defined by two points and a thickness.
    """
    browser_tags = ["builtin", "polygon"]

    class Options:
        p1 = rai.Option('First point', browser_default=(0, 0))
        p2 = rai.Option('Second point', browser_default=(10, 10))
        width = rai.Option('Thickness', browser_default=2)

    def _make(self, /, p1, p2=None, width=None, *, angle=None, length=None):
        passed = (
            (p2 is not None) << 2 |
            (angle is not None) << 1 |
            (length is not None) << 0
            )

        if passed == 0b000:
            raise RectWireNotEnoughArgumentsError(
                "You must specify either an endpoint or angle and bearing "
                "in order to construct a RectWire."
                )

        if passed == 0b001:
            raise RectWireNotEnoughArgumentsError(
                "You passed a length, but not an angle. "
                "You must specify angle."
                )

        if passed == 0b010:
            raise RectWireNotEnoughArgumentsError(
                "You passed an angle, but not a length. "
                "You must specify length."
                )

        if passed == 0b011:
            p2 = p1 + rai.polar(angle, length)

        if passed == 0b100:
            angle = rai.angle_between(p1, p2)

        if passed >= 0b101:
            raise RectWireIncorrectArgumentsError(
                "Pass either a startpoint and endpoint "
                "or startpoint, length, and angle."
                )

        step = rai.polar(
            arg=angle + rai.quartercircle,
            mod=width / 2)

        self.geoms.update({
            'root': [
                [
                    p1 + step,
                    p1 - step,
                    p2 - step,
                    p2 + step,
                    ]
                ]
            })

