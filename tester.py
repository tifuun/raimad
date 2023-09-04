#from PyCIF.SampleComponent import SampleComponent
#from PyCIF.exporters.cif import export as export_cif
#
#compo = SampleComponent()
#compo.make()
#
#with open('./test.cif', 'w') as f:
#    export_cif(f, compo)
#

#from pc_DeshimaPort.CPW import CPW
#from PyCIF.exporters.cif import export as export_cif
#
#compo = CPW()
#compo.make()
#
#with open('./test.cif', 'w') as f:
#    export_cif(f, compo)

###############

# import numpy as np
# from PyCIF.draw.angles import Angle, Turn, Bearing
# 
# print(Angle.Degrees(10))
# print(Angle.Radians(np.pi))
# print(Angle.Radians(np.pi))
# 
# print(Turn.Degrees(180))
# print(Turn.Degrees(-180))
# print(Turn.Degrees(-90))
# print(Turn.Degrees(90))
# print(Turn.Degrees(0))
# print(Bearing.Degrees(370))
# print(Turn.Left)
# print(Turn.Left())
# 
# #print(Angle(radians=np.pi, degrees=10))
# #print(Angle(10))

##################

#import PyCIF as pc
#from pc_DeshimaPort.CPW import CPW, CPWMKIDCoupler, CPWLayers
#from PyCIF.exporters.cif import export as export_cif
#
#class Test(pc.Component):
#    Layers = CPWLayers
#
#    def _make(self, opts):
#
#        coup1, compo = self._make_demo_cpw()
#        self.add_subcomponent(coup1)
#        self.add_subcomponent(compo)
#
#        coup1, compo = self._make_demo_cpw(pc.Dict(
#            enable_bridges=False,
#            ))
#        coup1.move(y=-20)
#        compo.move(y=-20)
#        self.add_subcomponent(coup1)
#        self.add_subcomponent(compo)
#
#        coup1, compo = self._make_demo_cpw(pc.Dict(
#            enable_bridges=True,
#            break_bridges=True,
#            ))
#        coup1.move(y=-40)
#        compo.move(y=-40)
#        self.add_subcomponent(coup1)
#        self.add_subcomponent(compo)
#
#    def _make_demo_cpw(self, cpwopts={}):
#        lineopts = pc.Dict(
#            signal_width=1,
#            ground_width=1,
#            gap_width=1,
#            )
#
#        coup1 = CPWMKIDCoupler(opts=pc.Dict(
#            lineopts
#            )).align_mark_to_point(
#                'cpw_center',
#                pc.Point(100, 50)
#            )
#
#        compo = CPW(opts=pc.Dict(
#            lineopts,
#            cpwopts,
#            waypoints=[
#                    pc.Point(0, 0),
#                    pc.Point(50, 50),
#                    coup1,
#                    pc.Point(150, 50),
#                ]
#            ))
#
#        return coup1, compo
#
#
#with open('./test.cif', 'w') as f:
#    export_cif(f, Test())


####################
####################

#import PyCIF as pc
#from PyCIF import path
#from pc_DeshimaPort.CPW import CPWBend, CPWBridge, CPWLayers, CPWStraight
#from pprint import pprint
#
#from PyCIF.exporters.cif import export as export_cif
#
#class MyComponent(pc.Component):
#    Layers = pc.Dict(
#        root=pc.Layer()
#        )
#
#    Options = pc.Dict(
#        radius=pc.Option.Geometric(2)
#        )
#
#    def _make(self, opts):
#        self.add_subpolygon(
#            pc.Circle(opts.radius)
#            )
#        self._add_mark('tl_enter',
#            pc.Point(
#                arg=pc.degrees(180),
#                mag=opts.radius,
#                ),
#            )
#        self._add_mark('tl_exit',
#            pc.Point(
#                arg=pc.degrees(0),
#                mag=opts.radius,
#                ),
#            )
#
#compo1 = MyComponent(opts=pc.Dict(radius=10)).move(-40, -40)
#compo2 = MyComponent(opts=pc.Dict(radius=5)).move(100, 100)
#compo3 = MyComponent(opts=pc.Dict(radius=10)).move(200, 140)
#
#path0 = [
#    path.StartAt(compo1),
#    path.StraightTo(pc.Point(30, 40)),
#    path.ElbowTo(compo2),
#    path.ElbowTo(path.StraightThru(compo3)),
#    path.StraightTo(pc.Point(250, 140)),
#    path.StraightTo(pc.Point(300, 50)),
#    path.StraightTo(pc.Point(100, 50)),
#    ]
#
#path0, bends, bridges, straights = path.resolve_path(
#    path0,
#    bend_compo=pc.Partial(
#        CPWBend,
#        pc.Dict(
#            radius=10,
#            ),
#        ),
#    bend_radius=10,
#    bridge_compo=pc.Partial(
#        CPWBridge,
#        pc.Dict(
#            length=10,
#            insl_length=7
#            ),
#        ),
#    bridge_spacing=30,
#    bridge_scramble=10,
#    straight_compo=pc.Partial(
#        CPWStraight,
#        pc.Dict(
#            ),
#        ),
#    )


#from copy import copy
#
#print('\n'*20)
#pprint('-'*20 + 'step 0')
#pprint(path0)
#
#pprint('-'*20 + 'step 1')
#path1, *_ = path.resolve_path(copy(path0), steps=1)
#pprint(path1)
#
#pprint('-'*20 + 'step 2')
#path2, *_ = path.resolve_path(copy(path1), steps=2)
#pprint(path2)
#
#pprint('-'*20 + 'step 3')
#path3, *_ = path.resolve_path(copy(path2), steps=3)
#pprint(path3)
#
#pprint('-'*20 + 'step 4')
#path4, bends, _, _ = path.resolve_path(
#    copy(path3),
#    steps=4,
#    bend_compo=pc.Partial(
#        CPWBend,
#        pc.Dict(
#            radius=10,
#            ),
#        ),
#    bend_radius=10
#    )
#pprint(path4)
#
#pprint('-'*20 + 'step 5')
#path5, *_ = path.resolve_path(copy(path4), steps=5)
#pprint(path5)
#
#pprint('-'*20 + 'step 6')
#path6, _, bridges, _ = path.resolve_path(
#    copy(path5),
#    steps=6,
#    bridge_compo=pc.Partial(
#        CPWBridge,
#        pc.Dict(
#            ),
#        ),
#    bridge_spacing=30,
#    bridge_scramble=10,
#    )
#pprint(path6)
#
#pprint('-'*20 + 'step 7')
#path7, *_ = path.resolve_path(copy(path6), steps=7)
#pprint(path7)
#
#pprint('-'*20 + 'step 8')
#path8, _, _, _ = path.resolve_path(copy(path7), steps=8)
#pprint(path8)
#
#pprint('-'*20 + 'step 9')
#path9, _, _, straights = path.resolve_path(
#    copy(path8),
#    steps=9,
#    straight_compo=pc.Partial(
#        CPWStraight,
#        pc.Dict(
#            ),
#        ),
#    )
#pprint(path9)
#
#pprint('-'*20)
#
#svg = path.render_paths_as_svg([path2, path5, path7, path8]).getvalue()
#with open('./test0.svg', 'w') as f:
#    f.write(svg)
#
#
#
#class TestCompo(pc.Component):
#    Layers = CPWLayers
#
#    def _make(self, o):
#
#        self.add_subcomponent(compo1, 'conductor')
#        self.add_subcomponent(compo2, 'conductor')
#        self.add_subcomponent(compo3, 'conductor')
#        for bend in bends:
#            self.add_subcomponent(bend)
#
#        for bridge in bridges:
#            self.add_subcomponent(bridge)
#
#        for straight in straights:
#            self.add_subcomponent(straight)
#
#compo = TestCompo()
#
#with open('./test.cif', 'w') as f:
#    export_cif(f, compo)


################################
################################

#import PyCIF as pc
#from pc_DeshimaDemo import DeshimaDemo
#from PyCIF.exporters.cif import export as export_cif
#
#compo = DeshimaDemo()
#
#with open('./test.cif', 'w') as f:
#    export_cif(f, compo)
#

#################################
#################################



import PyCIF as pc
from pc_DeshimaPort.CPW import CPWBend, CPWBridge, CPWLayers, CPWStraight

from PyCIF.exporters.cif import export as export_cif

class MyComponent(pc.Component):
    Layers = pc.Dict(
        root=pc.Layer()
        )

    Options = pc.Dict(
        radius=pc.Option.Geometric(2)
        )

    def _make(self, opts):
        self.add_subpolygon(
            pc.Circle(opts.radius)
            )
        self._add_mark('tl_enter',
            pc.Point(
                arg=pc.degrees(180),
                mag=opts.radius,
                ),
            )
        self._add_mark('tl_exit',
            pc.Point(
                arg=pc.degrees(0),
                mag=opts.radius,
                ),
            )

compo1 = MyComponent(opts=pc.Dict(radius=10)).move(-40, -40)
compo2 = MyComponent(opts=pc.Dict(radius=5)).move(100, 100)
compo3 = MyComponent(opts=pc.Dict(radius=10)).move(200, 140)


bend_compo = pc.Partial(
    CPWBend,
    pc.Dict(
        radius=10,
        ),
    )

bridge_compo=pc.Partial(
    CPWBridge,
    pc.Dict(
        length=10,
        insl_length=7
        ),
    )

straight_compo=pc.Partial(
    CPWStraight,
    pc.Dict(
        ),
    )

path0 = [
    pc.path.StartAt(pc.Point(0, 40)),
    pc.path.ElbowTo(pc.Point(50, 80)),
    pc.path.StraightTo(pc.Point(100, 40)),
    pc.path.StraightTo(pc.Point(150, 00)),
    pc.path.ElbowTo(pc.Point(200, 40)),
    ]


path1 = pc.path.resolve_startat(path0)
path2 = pc.path.resolve_elbows(path1)
path3 = pc.path.reduce_straights(path2)
path4 = pc.path.construct_bends_2(path3, bend_radius=10)
path5 = pc.path.construct_bridges_2(path4, 20, 3, 5)

#path0, bends, bridges, straights = pc.path.resolve_path(
#    path0,
#    bend_compo=bend_compo,
#    bend_radius=10,
#    beidge_compo=bridge_compo,
#    bridge_spacing=30,
#    bridge_scramble=10,
#    straight_compo=straight_compo,
#    )

svg = pc.path.render_paths_as_svg([path1, path2, path3, path4, path5]).getvalue()

with open('./test0.svg', 'w') as f:
    f.write(svg)

