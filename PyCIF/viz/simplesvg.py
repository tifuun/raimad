"""
Basic utility for drawing SVG files.
"""
from io import StringIO
from dataclasses import dataclass

import PyCIF as pc

class SVG:
    @dataclass
    class Circle:
        cx: float
        cy: float
        r: float
        name: str | None = None

        def write(self, stream, canvas_size):
            self.cy = canvas_size[1] - self.cy

            stream.write(
                '\t<circle class="mark" '
                f'cx="{self.cx}" '
                f'cy="{self.cy}" '
                f'r="{self.r}" '
                '>\n',
                )
            if self.name:
                stream.write(
                    f'\t\t<title>{self.name}</title>\n',
                    )
            stream.write('\t</circle>\n')

    @dataclass
    class Line:
        x1: float
        y1: float
        x2: float
        y2: float

        def write(self, stream, canvas_size):
            self.y1 = canvas_size[1] - self.y1
            self.y2 = canvas_size[1] - self.y2

            stream.write(
                '<line '
                f'x1="{self.x1}" '
                f'y1="{self.y1}" '
                f'x2="{self.x2}" '
                f'y2="{self.y2}" '
                'stroke="#00f" '
                'stroke-width="1" '
                '/>\n'
                )

    def __init__(self, canvas_size=None, stream=None):
        self.canvas_size = canvas_size
        self.stream = stream or StringIO()

        self.points = []
        self.shapes = []

        self.offset_x = 0
        self.offset_y = 0

    def circle(self, cx, cy, r=2, name=None):
        cx += self.offset_x
        cy += self.offset_y
        self.points.append((cx, cy))
        self.shapes.append(self.Circle(cx, cy, r, name))

    def line(self, x1, y1, x2, y2):
        x1 += self.offset_x
        x2 += self.offset_x
        y1 += self.offset_y
        y2 += self.offset_y
        self.points.extend(((x1, y1), (x2, y2)))
        self.shapes.append(self.Line(x1, y1, x2, y2))

    def autofit(self):
        x1, y1, x2, y2 = pc.bounding_box_cartesian(self.points)
        return x1 + x2, y1 + y2
        # TODO more jank here
        #return pc.bounding_box_size(
        #    pc.bounding_box_cartesian(
        #        self.points
        #        )
        #    )
    
    def collage_E(self):
        if self.canvas_size is not None:
            raise NotImplementedError(
                "Collage only works with automatic canvas size"
                )

        x1, y1, x2, y2 = pc.bounding_box_cartesian(self.points)
        self.offset_x = x1 + x2

    def done(self):
        canvas_size = self.canvas_size or self.autofit()

        self.stream.write(
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{canvas_size[0]}" '
            f'height="{canvas_size[1]}">\n'
            )

        for shape in self.shapes:
            shape.write(self.stream, canvas_size)

        self.stream.write('</svg>\n')

