import pycif as pc

class RectWire(pc.Compo):
    """
    RectWire

    A rectangle defined by two points and a thickness.
    """
    browser_tags = ["builtin", "polygon"]

    class Options:
        p1 = pc.Option('First point', browser_default=(0, 0))
        p2 = pc.Option('Second point', browser_default=(10, 10))
        thickness = pc.Option('Thickness', browser_default=2)

    def _make(self, p1, p2, thickness):
        bearing = pc.angle_between(p1, p2)
        step = pc.polar(
            arg=bearing + pc.quartercircle,
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

