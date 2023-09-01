"""
TransmissionLine -- component for building arbitrary tranmission lines.
TransmissionLine allows for constructing transmission lines
out of separate building blocks. Namely, a TransmissionLine
takes in bend, bridge, and connecting segment components,
and builds a full transmission linme out of them, given
a set of points that it must pass through.
"""

__author__ = "MaybE_Tree"
__credits__ = [
    ]

import logging
from random import Random
from typing import Sequence

import numpy as np

import PyCIF as pc

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

WaypointsType = Sequence[Sequence | pc.Markable]
# TODO proper point type, this is not obvious


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

def waypoints_to_points(waypoints: WaypointsType):
    points = []

    for index, waypoint in enumerate(waypoints):
        if isinstance(waypoint, pc.Markable):
            if index != 0:
                points.append(waypoint.get_mark('tl_enter'))
            if index != len(waypoints) - 1:
                points.append(waypoint.get_mark('tl_exit'))

        else:
            # TODO proper point type, this is not obvious
            points.append(pc.Point(*waypoint))

    return points

def make_rigid(points):
    """
    Given a 2D numpy array containing points for a transmission line,
    add points such that the line only make 90 degree turns.
    """
    pass


def make_straights(straight_component, straight_points):
    straights = []

    for start_point, end_point in pc.iter.couples(straight_points):

        length = pc.distance_between(start_point, end_point)
        angle = pc.angle_between(start_point, end_point)

        straight = straight_component(opts=dict(
            length=length,
            ))

        straight.align_mark_to_point('tl_enter', start_point)
        straight.rotate_around_mark('tl_enter', angle)

        straights.append(straight)

    return straights

def make_straight_points(leg_points, all_bridges):
    straight_points = []

    for leg_bridges, (leg_start, leg_end) in zip(
            all_bridges,
            pc.iter.couples(leg_points),
            ):
        straight_points.append(leg_start)

        for bridge in leg_bridges:
            straight_points.append(
                bridge.get_mark('tl_enter'),
                )
            straight_points.append(
                bridge.get_mark('tl_exit'),
                )

        straight_points.append(leg_end)

    return straight_points

def make_bridges(
        bridge_component,
        leg_points,
        base_spacing,
        spacing_scramble,
        ):
    """
    Given leg points (see self._make_leg_points),
    make bridges.
    """
    all_bridges = []

    # Get a random number generator with a known seed,
    # so that bridge spacing is deterministic.
    # This is better than using `random.seed`, since it won't
    # set the seed for anyone else who might be using the `random`
    # module.
    rng = Random(42)

    for leg_start, leg_end in pc.iter.couples(leg_points):
        leg_angle = pc.angle_between(leg_start, leg_end)
        leg_distance = pc.distance_between(leg_start, leg_end)

        current_point = leg_start

        leg_bridges = []

        for _ in np.arange(leg_distance / (base_spacing) - 1):
            step = (
                base_spacing +
                rng.uniform(-1, 1) * spacing_scramble
                )
            bridge = make_bridge(
                bridge_component,
                current_point,
                leg_angle,
                )

            leg_bridges.append(bridge)

            current_point = current_point + pc.Point_polar(leg_angle, step)

        # Add one last bridge at the end of the leg
        # (right by the turn)
        leg_bridges.append(
            make_bridge_end(
                bridge_component,
                leg_end,
                leg_angle,
                )
            )

        all_bridges.append(leg_bridges)

    return all_bridges

def make_bridge(bridge_component, startpoint, angle):
    """
    Given a startpoint and rotation (leg angle), add a bridge
    """
    bridge = bridge_component()
    bridge.align_mark_to_point('tl_enter', startpoint)
    bridge.rotate_around_mark('tl_enter', angle)
    return bridge

def make_bridge_end(bridge_component, endpoint, angle):
    """
    Given an endpoint and rotation (leg angle), add a bridge
    """
    bridge = bridge_component()
    bridge.align_mark_to_point('tl_exit', endpoint)
    bridge.rotate_around_mark('tl_exit', angle)
    return bridge

def make_leg_points(points, bends):
    """
    Generate a list of points, where every two points
    show the start and end of a leg.
    [
        first leg start point,
        first leg end point,
        second leg start point,
        second leg end point,
        .......
    ]
    """
    leg_points = []

    # The start of the first leg is the start of the
    # transmission line
    leg_points.append(points[0])

    # Next, we loop through the bends and add their points
    for bend in bends:
        leg_points.append(bend.get_mark('tl_enter'))
        leg_points.append(bend.get_mark('tl_exit'))

    # Finally, the end of the last leg is the
    # end of the transmission line.
    leg_points.append(points[-1])

    return leg_points

def make_bends(bend_radius, bend_component, points):
    bends = []
    for before, point, after in pc.iter.triplets(points):
        bend = make_bend(bend_radius, bend_component, before, point, after)
        if not bend:
            continue

        # TODO somehow freeze polygons/components
        # when they are added as subpolygons/subcomponents
        # so that they can't be used later on?
        #
        # Or, rather, can't be transformed/modified.
        #yield bend
        bends.append(bend)

    return bends

def make_bend(bend_radius, bend_component, before, point, after):
    angle_incoming = pc.angle_between(before, point) % pc.fullcircle
    angle_outgoing = pc.angle_between(point, after) % pc.fullcircle

    log.debug(
        "New turn, in: %.3f, out: %.3f",
        angle_incoming / pc.pi,
        angle_outgoing / pc.pi,
        )

    turn = angle_outgoing - angle_incoming

    # corner_angle is the inner angle made by the incoming and
    # outgoing straight measures. We calculate it by taking the
    # supplement of the turn angle
    corner_angle = pc.semicircle - abs(turn)

    if abs(turn) < 0.01:  # TODO standardize epsilon value
        # Straight turn
        log.debug("Straight.")
        return None

    if turn > 0:
        # Left turn
        log.debug("Left.")

        angle_turn_center = (
            angle_outgoing + angle_incoming + pc.semicircle
            ) / 2

        orientation = pc.Orientation.Counterclockwise

        angle_turn_start = angle_incoming - pc.quartercircle
        angle_turn_end = angle_outgoing - pc.quartercircle

    elif turn < 0:
        # Right turn
        log.debug("Right.")

        angle_turn_center = (
            angle_outgoing + angle_incoming - pc.semicircle
            ) / 2

        orientation = pc.Orientation.Clockwise

        angle_turn_start = angle_incoming - 3 * pc.quartercircle
        angle_turn_end = angle_outgoing - 3 * pc.quartercircle

    else:
        assert False, f'Invalid turn `{turn}` ocurred in TransmissionLine'

    offset_turn_center = bend_radius / pc.sin(corner_angle / 2)

    point_turn_center = (
        point +
        pc.Point_polar(angle_turn_center, offset_turn_center)
        )

    bend = bend_component(opts=dict(
        angle_start=angle_turn_start,
        angle_end=angle_turn_end,
        #center=point_turn_center,
        orientation=orientation,
        ))

    bend.align_mark_to_point('center', point_turn_center)

    return bend



# ==============
#from pc_DeshimaPort import waypoints as wp
#
#def add_bridges(wpoints: wp.Waypoints, bend_radius, bend_component):
#    new_wpoints = []
#
#    new_wpoints.append(wpoints[0])
#
#    for before, point, after in pc.iter.triplets(wpoints):
#        bend = make_bend(
#                bend_radius,
#                bend_component,
#                before.point,
#                point.point,
#                after.point,
#                )
#
#        if bend:
#            new_wpoints.append(bend)
#        else:
#            new_wpoints.append(point)
#
#    new_wpoints.append(wpoints[-1])
#
#    return new_wpoints


