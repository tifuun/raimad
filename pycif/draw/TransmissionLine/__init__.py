from .Connection import Connection
from .Connection import StartAt
from .Connection import JumpTo
from .Connection import StraightTo
from .Connection import ElbowTo
from .Connection import MeanderTo

from .resolvers.elbows import resolve_elbows
from .resolvers.elbows import resolve_elbow

from .resolvers.reducers import reduce_straights

from .resolvers.bends import BendSpec
from .resolvers.bends import construct_bends
from .resolvers.bends import construct_bend
from .resolvers.bends import make_bend_compo
from .resolvers.bends import make_bend_compos

from .resolvers.bridges import BridgeSpec
from .resolvers.bridges import construct_bridges
from .resolvers.bridges import make_bridge_compo
from .resolvers.bridges import make_bridge_compos

from .resolvers.straights import StraightSpec
from .resolvers.straights import make_straight_compos
from .resolvers.straights import make_straight_compo
from .resolvers.straights import construct_straights

from .viz import render_path_as_svg
from .viz import render_paths_as_svg
from .viz import format_path

from .TransmissionLine import TransmissionLine

import pycif as pc

# TODO TODO FIXME TODO move the below out FIXME FIXME TODO

class BendOpts(pc.Compo.Options):
    bend_radius = pc.Option.Geometric(
        10,
        'Bend Radius',
        )

    angle_start = pc.Option.Geometric(
        pc.degrees(10),
        'Angle at the start of the turn',
        )

    angle_end = pc.Option.Geometric(
        pc.degrees(50),
        'Angle at the end of the turn',
        )

    orientation = pc.Option.Geometric(
        pc.Orientation.Counterclockwise,
        'Clockwise or counterclockwise?',
        )

class StraightOpts(pc.Compo.Options):
    length = pc.Option.Geometric(
        4,
        'Straight segment length (dimension parallel with line)',
        )

class BridgeOpts(pc.Compo.Options):
    length = pc.Option.Geometric(
        4,
        'Bridge length (dimension parallel with line)',
        )

class TLOpts(pc.Compo.Options):
    bend_radius = pc.Option.Geometric(
        10,
        'Bend Radius',
        )

    rigid = pc.Option.Geometric(
        False,
        'Make only right angle turns?',
        )

    bridging = pc.Option.Geometric(
        False,
        'Enable Bridging?',
        )

    bridge_base_spacing = pc.Option.Geometric(
        20,
        'Base spacing interval between bridges',
        )

    bridge_spacing_scramble = pc.Option.Geometric(
        1,
        'Maximum deviation from base bridge spacing '
        '(to prevent standing waves)',
        )

    waypoints = pc.Option.Geometric(
        [
            [0, 0],
            [150, 0],
            [150, 50],
            [150, 100],
            [120, 100],
            [100, 100],
            [100, 50],
            [50, 50],
            [50, 100],
            [0, 80],
            [-50, 60],
            [-100, 100],
            [0, 140],
            [-70, 140],
            ],
        "numpy array containing points that the line should pass through",
        )

