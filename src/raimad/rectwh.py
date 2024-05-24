import raimad as rai

class RectWH(rai.Compo):
    """
    RectWH

    A rectangle defined by width and height.
    """
    browser_tags = ["builtin", "polygon"]

    class Options:
        width = rai.Option('Width of rectangle', browser_default=15)
        height = rai.Option('Height of rectangle', browser_default=10)

    def _make(self, width: int, height: int):
        self.width = width
        self.height = height

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

