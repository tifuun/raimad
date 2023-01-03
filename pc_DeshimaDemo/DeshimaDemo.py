from PyClewinSDC.Component import Component, make_layers
from PyClewinSDC.Transformable import Transformable

from pc_Fundamental.Mesh import Mesh
from pc_Fundamental.Antennas import LeakyDESHIMA


class DeshimaDemo(Component):
    layerspecs = make_layers(
        Component,
        ('front', 'SiN_front', '0500cf00', '0500cf00'),  # L0
        ('gnd', 'NbTiN_GND', '0f00bbff', '0f00bbff'),  # L1
        ('back', 'SiN_back', '0f00cbff', '0f00cbff'),  # L2
        ('al', 'Aluminum', '0fff0000', '0fff0000'),  # L3
        ('si', 'aSilicon', '05000000', '05000000'),  # L4
        ('line_opt', 'NbTiN_lineOPT', '050000ff', '050000ff'),  # L5
        ('line_eb', 'NbTiN_lineEB', '0f0000ff', '0f0000ff'),  # L6
        ('backside', 'Ta backside', '0fc0c0c0', '0fc0c0c0'),  # L7
        ('text', 'text', '05000000', '05000000'),  # L8
        ('dummy_opt', 'dummy_NbTiN_lineOPT', '05fefefe', '05fefefe'),  # L9
        ('dummy_gnd', 'dummy_NbTiN_GND', '05fefefe', '05fefefe'),  # L10
        ('poly', 'Polymide', '0ff0f000', '0ff0f000'),  # L11
        ('permi', 'Perminex', '0f0000ff', '0f0000ff'),  # L12
        ('al_eb', 'AluminumEB', '0ff0f00f', '0ff0f00f'),  # L13
        ('line_eb_coarse', 'NbTiN_lineEB_coarse', '0fff00ff', '0fff00ff'),  # L14
        )

    def make(self, opts=None):
        if opts is None:
            opts = self.opts

        self._make_mesh()
        self._make_squares()

        antenna = LeakyDESHIMA()
        antenna.make()
        self.add_subcomponent(
            antenna,
            {'eb': 'line_eb_coarse'}
            )

    def _make_mesh(self):
        mesh = Mesh(width=1000, height=1000, void_width=100, void_height=100)
        mesh.make()
        self.add_subcomponent(mesh, 'backside')

    def _make_squares(self):
        trans = Transformable()
        trans.rot(10)
        trans.move(500, 500)
        trans.scale(0.9)
        #trans.rot(-10)
        mesh = Mesh(width=1000, height=1000)
        mesh.make()
        self.add_subcomponent(mesh, 'poly', trans)


