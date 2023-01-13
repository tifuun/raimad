from PyClewinSDC.Component import Component, make_layers
from PyClewinSDC.Polygon import Polygon
from PyClewinSDC.Transform import Transform
from PyClewinSDC.Dotdict import Dotdict

from pc_Fundamental.Mesh import Mesh
from pc_DeshimaPort.Filter import Filter
from pc_LeakyAntenna.LeakyAntennaExample import LeakyAntennaExample


class DeshimaDemo(Component):
    layerspecs = make_layers(
        Component,
        front=('SiN_front', ),  # L0
        gnd=('NbTiN_GND', ),  # L1
        back=('SiN_back', ),  # L2
        al=('Aluminum', ),  # L3
        asi=('aSilicon', ),  # L4
        line_opt=('NbTiN_lineOPT', ),  # L5
        line_eb=('NbTiN_lineEB', ),  # L6
        backside=('Ta backside', ),  # L7
        text=('text', ),  # L8
        dummy_opt=('dummy_NbTiN_lineOPT', ),  # L9
        dummy_gnd=('dummy_NbTiN_GND', ),  # L10
        poly=('Polymide', ),  # L11
        permi=('Perminex', ),  # L12
        al_eb=('AluminumEB', ),  # L13
        line_eb_coarse=('NbTiN_lineEB_coarse', ),  # L14
        )
    #layerspecs = make_layers(
    #    Component,
    #    front=('SiN_front', '0500cf00', '0500cf00'),  # L0
    #    gnd=('NbTiN_GND', '0f00bbff', '0f00bbff'),  # L1
    #    back=('SiN_back', '0f00cbff', '0f00cbff'),  # L2
    #    al=('Aluminum', '0fff0000', '0fff0000'),  # L3
    #    asi=('aSilicon', '05000000', '05000000'),  # L4
    #    line_opt=('NbTiN_lineOPT', '050000ff', '050000ff'),  # L5
    #    line_eb=('NbTiN_lineEB', '0f0000ff', '0f0000ff'),  # L6
    #    backside=('Ta backside', '0fc0c0c0', '0fc0c0c0'),  # L7
    #    text=('text', '05000000', '05000000'),  # L8
    #    dummy_opt=('dummy_NbTiN_lineOPT', '05fefefe', '05fefefe'),  # L9
    #    dummy_gnd=('dummy_NbTiN_GND', '05fefefe', '05fefefe'),  # L10
    #    poly=('Polymide', '0ff0f000', '0ff0f000'),  # L11
    #    permi=('Perminex', '0f0000ff', '0f0000ff'),  # L12
    #    al_eb=('AluminumEB', '0ff0f00f', '0ff0f00f'),  # L13
    #    line_eb_coarse=('NbTiN_lineEB_coarse', '0fff00ff', '0fff00ff'),  # L14
    #    )

    def make(self):
        self._make_mesh()
        #self._make_antenna()

        line = Polygon.rect_wh(-500, 0, 1000, 2)
        self.add_subpolygon(line, 'line_eb')

        self._make_filters(line)

    def _make_mesh(self):
        mesh = Mesh(
            Dotdict(
                width=1000,
                height=1000,
                void_width=100,
                void_height=100,
                ),
            )
        mesh.make()
        mesh.move(-500, -500)
        self.add_subcomponent(mesh, 'backside')

    def _make_antenna(self):
        antenna = LeakyAntennaExample()
        antenna.make()
        self.add_subcomponent(
            antenna,
            {'eb': 'line_eb_coarse'}
            )

    def _make_filters(self, line):
        trans = Transform()

        for filter_index in range(0, 10):
            filt = Filter(
                Dotdict(
                    l_res=filter_index * 10 + 70,
                    ),
                transform=trans,
                )
            filt.make()
            filt.marks.line.aligny(line.bot_mid)
            self.add_subcomponent(
                filt,
                {
                    'gnd': 'gnd',
                    'opt': 'line_opt',
                    'diel': 'asi',
                    'eb': 'line_eb',
                    },
                )

            trans.movex(200)




