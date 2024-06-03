import raimad as rai

class RectLW(rai.Compo):
    """
    RectLW

    A rectangle defined by length (horizontal) and width (vertical).
    """
    browser_tags = ["builtin", "polygon"]

    class Options:
        length = rai.Option('Length of rectangle', browser_default=15)
        width = rai.Option('Width of rectangle', browser_default=10)

    def _make(self, length: float, width: float):
        self.length = length
        self.width = width

        self.geoms.update({
            'root': [
                [
                    [- length / 2, - width / 2],
                    [+ length / 2, - width / 2],
                    [+ length / 2, + width / 2],
                    [- length / 2, + width / 2],
                    ]
                ]
            })

