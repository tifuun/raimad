from PyClewinSDC.Component import Component

from pc_Fundamental.Mesh import ArbitraryMesh


class MeshDeshima2(ArbitraryMesh):
    def __init__(self, width, height):
        super().__init__(
            width,
            height,
            100,
            100,
            3,
            3,
            )

class DeshimaDemo(Component):
    def __init__(self):
        super().__init__()

        self.add_layer('front', 'SiN_front', '0500cf00', '0500cf00')  # L0
        self.add_layer('gnd', 'NbTiN_GND', '0f00bbff', '0f00bbff')  # L1
        self.add_layer('back', 'SiN_back', '0f00cbff', '0f00cbff')  # L2
        self.add_layer('al', 'Aluminum', '0fff0000', '0fff0000')  # L3
        self.add_layer('si', 'aSilicon', '05000000', '05000000')  # L4
        self.add_layer('line_opt', 'NbTiN_lineOPT', '050000ff', '050000ff')  # L5
        self.add_layer('line_eb', 'NbTiN_lineEB', '0f0000ff', '0f0000ff')  # L6
        self.add_layer('backside', 'Ta backside', '0fc0c0c0', '0fc0c0c0')  # L7
        self.add_layer('text', 'text', '05000000', '05000000')  # L8
        self.add_layer('dummy_opt', 'dummy_NbTiN_lineOPT', '05fefefe', '05fefefe')  # L8
        self.add_layer('dummy_gnd', 'dummy_NbTiN_GND', '05fefefe', '05fefefe')  # L9
        self.add_layer('poly', 'Polymide', '0ff0f000', '0ff0f000')  # L10


    def make(self):
        self.make_mesh()
        self.make_squares()

    def make_mesh(self):
        mesh = MeshDeshima2(1000, 1000)
        mesh.make()
        self.add_subcomponent(mesh, 'backside')

    def make_squares(self):
        ctx = self.new_context()
        ctx.rotate(10)
        ctx.translate(500, 500)
        ctx.scale(0.9)
        ctx.rotate(-10)
        mesh = MeshDeshima2(1000, 1000)
        mesh.make()
        ctx.add_subcomponent(mesh, 'poly')
        pass


