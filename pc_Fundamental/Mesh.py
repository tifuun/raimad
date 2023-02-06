from PyCIF.Component import Component, make_opts, make_layers
from PyCIF.Polygon import Polygon
from PyCIF.OptCategory import OptCategory, Geometric


class Mesh(Component):
    """
    Mesh
    Grid of lines that forms a mesh.
    Long description here.
    Something that can be used to absorb leaking radiation.
    Lorem Ipsum Dolor Sit Amet.
    """
    optspecs = make_opts(
        Component,
        width=(100, "Total width of the Mesh", Geometric),
        height=(100, "Total height of the Mesh", Geometric),
        void_width=(10, "Width of the blank cells", Geometric),
        void_height=(10, "Height of the blank cells", Geometric),
        line_width=(1, "Horizontal thickness of the mesh lines", Geometric),
        line_height=(1, "Vertical thickness of the mesh lines", Geometric),
        )

    layerspecs = make_layers(
        Component,
        main=("I-Shape", ),
        )

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

