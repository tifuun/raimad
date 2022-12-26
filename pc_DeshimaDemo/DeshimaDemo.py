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

        self.add_layer('backside')
        self.add_layer('main')

    def make(self):
        self.make_mesh()

    def make_mesh(self):
        mesh = MeshDeshima2(1000, 1000)
        mesh.make()
        self.add_subcomponent(mesh, 'backside')


#layers['SiN_front'] = ('0500cf00', '0500cf00') # L0
#layers['NbTiN_GND'] =  ('0f00bbff', '0f00bbff') # L1
#layers['SiN_back'] = ('0f00cbff', '0f00cbff') # L2
#layers['Aluminum'] = ('0fff0000', '0fff0000') # L3
#layers['aSilicon'] = ('05000000', '05000000') # L4
#layers['NbTiN_lineOPT'] = ('050000ff', '050000ff') # L5
#layers['NbTiN_lineEB'] = ('0f0000ff', '0f0000ff') # L6
#layers['Ta backside'] = ('0fc0c0c0', '0fc0c0c0') # L7
#layers['text'] = ('05000000', '05000000') # L8
#layers['dummy_NbTiN_lineOPT'] = ('05fefefe', '05fefefe') # L9 for readout
#layers['dummy_NbTiN_GND'] = ('05fefefe', '05fefefe') # L10 for readout
#layers['Polyimide'] = ('0ff0f000', '0ff0f000') # L11
