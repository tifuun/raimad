from PyCIF.draw.Component import Component, make_opts, Shadow, make_layers
from PyCIF.draw.Polygon import Polygon
from PyCIF.draw.polygons.Rect import Rect
from PyCIF.draw.polygons.Arc import Arc
from PyCIF.draw.OptCategory import Geometric
from PyCIF.draw.Transform import Transform


class SampleComponent(Component):
    """
    Sample component used for testing/debugging/development
    """
    optspecs = make_opts(
        Component,
        )

    layerspecs = make_layers(
        Component,
        l1=('l1', ),
        l2=('l2', ),
        )

    def make(self, opts=None):
        if opts is None:
            opts = self.opts

        trans = Transform()
        for x in range(0, 10):
            self.add_subpolygon(
                Rect(20, 10).apply_transform(trans),
                'l1',
                )

            arc = Arc(10, 20, 360 / 10 * x + 10)
            arc.move(x * 30, 10)
            arc.center.rot(x * 5)
            self.add_subpolygon(arc, 'l2')

            trans.move(30, 0)
            trans.rot(5, 10, 5)

