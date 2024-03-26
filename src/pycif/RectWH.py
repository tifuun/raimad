import pycif as pc

class RectWH(pc.Compo):
    def _make(self, width, height):
        self.geoms.update({
            'root': [
                [
                    [- width / 2, - height / 2],
                    [+ width / 2, - height / 2],
                    [+ width / 2, + height / 2],
                    [- width / 2, + height / 2],
                    ]
                ]
            })

