import pycif as pc

class RectWH(pc.Compo):
    """
    RectWH

    A rectangle defined by width and height.
    """
    browser_tags = ["builtin", "polygon"]

    class Options:
        width = pc.Option('Width of rectangle', browser_default=15)
        height = pc.Option('Height of rectangle', browser_default=10)

    def _make(self, width: int, height: int):
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

