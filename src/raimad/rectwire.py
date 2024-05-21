import raimad as rai

class RectWire(rai.Compo):
    """
    RectWire

    A rectangle defined by two points and a thickness.
    """
    browser_tags = ["builtin", "polygon"]

    class Options:
        p1 = rai.Option('First point', browser_default=(0, 0))
        p2 = rai.Option('Second point', browser_default=(10, 10))
        thickness = rai.Option('Thickness', browser_default=2)

    def _make(self, p1, p2, thickness):
        bearing = rai.angle_between(p1, p2)
        step = rai.polar(
            arg=bearing + rai.quartercircle,
            mod=thickness / 2)

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

