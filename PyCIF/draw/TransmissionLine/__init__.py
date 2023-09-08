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
from .resolvers.bends import make_bend_component
from .resolvers.bends import make_bend_components

from .resolvers.bridges import BridgeSpec
from .resolvers.bridges import construct_bridges
from .resolvers.bridges import make_bridge_component
from .resolvers.bridges import make_bridge_components

from .resolvers.straights import make_straight_components

from .viz import render_path_as_svg
from .viz import render_paths_as_svg
from .viz import format_path

from .TransmissionLine import TransmissionLine

import PyCIF as pc
BendOpts = pc.Dict(
    bend_radius=pc.Option.Geometric(
        10,
        'Bend Radius',
        ),
    angle_start=pc.Option.Geometric(
        pc.degrees(10),
        'Angle at the start of the turn',
        ),
    angle_end=pc.Option.Geometric(
        pc.degrees(50),
        'Angle at the end of the turn',
        ),
    orientation=pc.Option.Geometric(
        pc.Orientation.Counterclockwise,
        'Clockwise or counterclockwise?',
        ),
    )

StraightOpts = pc.Dict(
    length=pc.Option.Geometric(
        4,
        'Straight segment length (dimension parallel to line)',
        ),
    )

BridgeOpts = pc.Dict(
    length=pc.Option.Geometric(
        4,
        'Bridge length (dimension perpendicular to line)',
        ),
    width=pc.Option.Geometric(
        2,
        'Bridge width (dimension parallel with line)',
        ),
    )

TLOpts = pc.Dict(
    bend_radius=pc.Option.Geometric(
        10,
        'Bend Radius',
        ),
    rigid=pc.Option.Geometric(
        False,
        'Make only right angle turns?',
        ),
    bridging=pc.Option.Geometric(
        False,
        'Enable Bridging?',
        ),
    bridge_base_spacing=pc.Option.Geometric(
        20,
        'Base spacing interval between bridges',
        ),
    bridge_spacing_scramble=pc.Option.Geometric(
        1,
        'Maximum deviation from base bridge spacing '
        '(to prevent standing waves)',
        ),
    waypoints=pc.Option.Geometric(
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
    )


