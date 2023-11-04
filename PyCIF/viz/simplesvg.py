"""
Basic utility for drawing SVG files.
"""
from io import StringIO
from dataclasses import dataclass
from typing import Self, List
from copy import copy

import PyCIF as pc

class SVG:
    @dataclass
    class Circle:
        cx: float
        cy: float
        r: float
        name: str | None = None

        def write(self, stream):
            self.cy = self.cy

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

        def move(self, x, y):
            self.cx += x
            self.cy += y
            return self

    @dataclass
    class Line:
        x1: float
        y1: float
        x2: float
        y2: float
        color: str
        dasharray: List[float] | bool

        def write(self, stream):
            self.y1 = self.y1
            self.y2 = self.y2

            stream.write(
                '<line '
                f'x1="{self.x1}" '
                f'y1="{self.y1}" '
                f'x2="{self.x2}" '
                f'y2="{self.y2}" '
                f'stroke="{self.color}" '
                'stroke-width="1" '
                )
            if self.dasharray:
                if self.dasharray is True:
                    self.dasharray = [5, 4]

                stream.write(
                    f'stroke-dasharray="{",".join(map(str, self.dasharray))}" '
                    )
            stream.write(
                '/>\n'
                )

        def move(self, x, y):
            self.x1 += x
            self.x2 += x
            self.y1 += y
            self.y2 += y
            return self

    @dataclass
    class Rect:
        x: float
        y: float
        w: float
        h: float

        def write(self, stream):
            self.y = self.y

            stream.write(
                '<rect '
                f'x="{self.x}" '
                f'y="{self.y}" '
                f'width="{self.w}" '
                f'height="{self.h}" '
                'stroke="#333" '
                'stroke-width="1" '
                'fill="none" '
                '/>\n'
                )

        def move(self, x, y):
            self.x += x
            self.y += y
            return self

    def __init__(self, stream=None):
        self.stream = stream or StringIO()

        self.points = []
        self.shapes = []

        self.bbox = pc.BBox()

    def circle(self, cx, cy, r=2, name=None):
        self.bbox.add_point((cx, cy))
        self.shapes.append(self.Circle(cx, cy, r, name))

    def line(self, x1, y1, x2, y2, color='#00f', dasharray=[]):
        self.bbox.add_point((x1, y1))
        self.bbox.add_point((x2, y2))
        self.shapes.append(self.Line(x1, y1, x2, y2, color, dasharray))

    def rect(self, x, y, w, h):
        self.bbox.add_point((x, y))
        self.bbox.add_point((x + w, y + h))
        self.shapes.append(self.Rect(x, y, w, h))

    def done(self):
        bbox = self.bbox

        self.stream.write(
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{bbox.width}" '
            f'height="{bbox.height}" '
            f'viewBox="{bbox.left} {bbox.bottom} {bbox.width} {bbox.height}"'
            '>\n'
            )

        for shape in self.shapes:
            shape.write(self.stream)

        self.stream.write('</svg>\n')

    def make_frame(self, pad_x=10, pad_y=10):
        self.rect(
            self.bbox.left - pad_x,
            self.bbox.bottom - pad_y,
            self.bbox.width + pad_x * 2,
            self.bbox.height + pad_y * 2,
            )

    def collage_E(self, other: Self, pad_x=10, pad_y=10):
        for shape in other.shapes:
            self.shapes.append(
                copy(shape).move(
                    self.bbox.width + pad_x,
                    0
                    )
                )
        self.bbox.add_xyarray((
            (
                self.bbox.right + other.bbox.right + pad_x,
                self.bbox.top + other.bbox.top + pad_y,
                ),
            (
                self.bbox.right + other.bbox.right + pad_x * 2,
                self.bbox.bottom + other.bbox.bottom - pad_y,
                ),
            ))

