import pycif as pc

class RectWire(pc.Compo):
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

