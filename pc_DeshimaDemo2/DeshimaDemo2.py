from PyClewinSDC.Component import Component, make_layers
from PyClewinSDC.Transform import Transform
from PyClewinSDC.Polygon import Polygon

from pc_Fundamental.Mesh import Mesh
from pc_DeshimaPort.Filter import Filter


class DeshimaDemo2(Component):
    layerspecs = make_layers(
        Component,
        mesh=("Mesh for absorbing radiation", ),
        gnd=("NbTiN Ground", ),
        opt=("Optically exposed NbTiN", ),
        diel=("Dielectric", ),
        eb=("Electrobeam-deposited NbTiN", ),
        )

    def make(self):
        self._make_mesh()

        line = Polygon.rect_wh(0, 700, 2000, 2)
        self.add_subpolygon(line, 'eb')

        self._make_filters(line)

    def _make_filters(self, line):

        trans = Transform()
        trans.move(500, 500)

        for filter_index in range(10):
            filt = Filter(
                {
                    'l_res': 70 + 20 * filter_index,
                    'meander_coup_spacing': 10,
                    'line_coup_spacing': 10,
                },
                transform=trans
                )
            filt.make()
            filt.marks.line.aligny(line.bot_mid)
            self.add_subcomponent(
                filt,
                {
                    'gnd': 'gnd',
                    'opt': 'opt',
                    'diel': 'diel',
                    'eb': 'eb',
                    },
                )

            trans.movex(200)
            if (filter_index == 5):
                trans.rot(90)


    def _make_mesh(self):
        mesh = Mesh(
            {
                'width': 2000,
                'height': 2000,
                'void_width': 100,
                'void_height': 100,
                'line_width': 10,
                'line_height': 10,
                },
            )
        mesh.make()
        self.add_subcomponent(mesh, 'mesh')

            
