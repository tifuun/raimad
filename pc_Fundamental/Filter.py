import shapely as shp

from PyClewinSDC.Component import Component

class IFilter(Component):
    def __init__(self, x, y, beam_thickness, coupler_thickness):
        super().__init__()

        self.layers.main = []

        self.width = 10
        self.height = height
        self.width = width
        self.void_width = void_width
        self.void_height = void_height
        self.line_width = line_width
        self.line_height = line_height

    @property
    def cell_width(self):
        return self.void_width + self.line_width

    @property
    def cell_height(self):
        return self.void_height + self.line_height

    def make(self):
        for col in range(self.width // self.cell_width):
            self.layers.main.append(
                shp.box(
                    col * self.cell_width,
                    0,
                    col * self.cell_width + self.line_width,
                    self.height,
                    ),
                )

        for row in range(self.height // self.cell_height):
            self.layers.main.append(
                shp.box(
                    0,
                    row * self.cell_height,
                    self.width,
                    row * self.cell_height + self.line_height,
                    ),
                )


class Mesh850GHz(ArbitraryMesh):
    def __init__(self, width, height):
        super().__init__(
            width,
            height,
            50,
            50,
            3,
            3,
            )

