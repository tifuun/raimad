from PyClewinSDC.Component import Component
from PyClewinSDC.Polygon import Polygon
from PyClewinSDC.Dotdict import Dotdict


class Mesh(Component):
    """
    Mesh
    Grid of lines that forms a mesh.
    Long description here.
    Something that can be used to absorb leaking radiation.
    Lorem Ipsum Dolor Sit Amet.
    """
    default_opts = Dotdict(
        Component.default_opts,
        width=100,
        height=100,
        void_width=10,
        void_height=10,
        line_width=1,
        line_height=1,
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_layer('main')

    def make(self, opts=None):
        if opts is None:
            opts = self.opts

        cell_width = opts.void_width + opts.line_width
        cell_height = opts.void_height + opts.line_height

        for col in range(opts.width // cell_width):
            self.add_subpolygon(
                Polygon.rect_2point(
                    col * cell_width,
                    0,
                    col * cell_width + opts.line_width,
                    opts.height,
                    ),
                )

        for row in range(opts.height // cell_height):
            self.add_subpolygon(
                Polygon.rect_2point(
                    0,
                    row * cell_height,
                    opts.width,
                    row * cell_height + opts.line_height,
                    ),
                )

