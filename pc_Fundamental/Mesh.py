from PyClewinSDC.Component import Component
from PyClewinSDC.Polygon import Polygon
from PyClewinSDC.Dotdict import Dotdict


class Mesh(Component):
    default_opts = Dotdict(
        Component.default_opts,
        width=100,
        height=100,
        void_width=10,
        void_height=10,
        line_width=10,
        line_height=10,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_layer('main')

    @property
    def cell_width(self):
        return self.opts.void_width + self.opts.line_width

    @property
    def cell_height(self):
        return self.opts.void_height + self.opts.line_height

    def make(self):
        for col in range(self.opts.width // self.cell_width):
            self.add_subpolygon(
                Polygon.rect_2point(
                    col * self.cell_width,
                    0,
                    col * self.cell_width + self.opts.line_width,
                    self.opts.height,
                    ),
                )

        for row in range(self.opts.height // self.cell_height):
            self.add_subpolygon(
                Polygon.rect_2point(
                    0,
                    row * self.cell_height,
                    self.opts.width,
                    row * self.cell_height + self.opts.line_height,
                    ),
                )

