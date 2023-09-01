from typing import Any, ClassVar, List
from dataclasses import dataclass
from copy import copy
import logging
from random import Random

import numpy as np

import PyCIF as pc

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# Get a random number generator with a known seed,
# so that bridge spacing is deterministic.
# This is better than using `random.seed`, since it won't
# set the seed for anyone else who might be using the `random`
# module.
bridge_rng = Random(42)

ConnectionTarget = pc.typing.Point | pc.Markable

class Connection:
    """
    Abstract base for connection type
    """
    to: ConnectionTarget

    def __init__(self, to):
        if type(self) is Connection:
            raise Exception("Cannot create abstract Connection")
        self.to = to

class StartAt(Connection):
    """
    Start at point or markable
    """
    def __repr__(self):
        return f"Start at    {self.to}"

class JumpTo(Connection):
    """
    Indicates no connection to next point
    """
    def __repr__(self):
        return f"Jump to     {self.to}"

class StraightTo(Connection):
    """
    Direction connection between points with one straight line segment
    """
    def __repr__(self):
        return f"Straight to {self.to}"

class ElbowTo(Connection):
    """
    Elbow connection (90 degree) between two points
    """
    def __repr__(self):
        return f"Elbow to    {self.to}"

class MeanderTo(Connection):
    """
    Meander between two points
    """
    def __repr__(self):
        return f"Meander to  {self.to}"

    def __init__(*args, **kwargs):
        raise NotImplementedError

@dataclass
class GoThru:
    """
    Wrap components in this to specify how they should be traversed
    `how` is the connection type. Passing a raw component is equivalent to
    passing a component wrapped in a JumpTo GoThrough
    """
    markable: pc.Markable
    how: Connection

    def __repr__(self):
        if self.how is JumpTo:
            return f'Jump through {self.markable}'
        if self.how is StraightTo:
            return f'Straight through {self.markable}'
        if self.how is ElbowTo:
            return f'Elbow through {self.markable}'
        if self.how is MeanderTo:
            return f'Meander through {self.markable}'
        return repr(self.how)
        # TODO this is jank

def JumpThru(markable):
    return GoThru(markable, JumpTo)

def StraightThru(markable):
    return GoThru(markable, StraightTo)

def ElbowThru(markable):
    return GoThru(markable, ElbowTo)

def MeanderThru(markable):
    return GoThru(markable, MeanderTo)

def log_path(path, message):
    if log.level > logging.DEBUG:
        return

    logging.debug("----- %s -----", message)
    for i, conn in enumerate(path):
        logging.debug("%4.f: %s", i, conn)
    logging.debug("")

def resolve_path(
        path,
        bend_compo: pc.typing.ComponentClass,
        bend_radius: float,
        bridge_compo: pc.typing.ComponentClass,
        bridge_spacing: float,
        bridge_scramble: float,
        straight_compo: pc.typing.ComponentClass,
        ):
    assert [1 for waypoint in path if isinstance(waypoint, StartAt)] == [1]

    path = copy(path)
    log_path(path, "Stage 0")

    bends = []
    bridges = []
    straights = []

    # Step 1: resolve starting point
    path[0] = resolve_startat(path[0])
    log_path(path, "Stage 1: Resolve startat")

    # Step 2: resolve components
    path = resolve_components(path)
    log_path(path, "Stage 2: Resolve components")

    # Step 3: resolve elbows
    path = resolve_elbows(path)
    log_path(path, "Stage 3: Resolve elbows")

    # Step 4: construct bends
    path, bends = construct_bends(
        path,
        bend_component=bend_compo,
        bend_radius=bend_radius
        )
    log_path(path, "Stage 4: Construct bends")

    # Step 5: resolve bends
    path = resolve_components(path)
    log_path(path, "Stage 5: Resolve bends")

    # Step 6: construct bridges
    bridge_builder = BridgeBuilder(
        bridge_compo=bridge_compo,
        base_spacing=bridge_spacing,
        spacing_scramble=bridge_scramble,
        )

    bridge_builder.build(path)

    bridges = bridge_builder.bridges_
    path = bridge_builder.newpath_
    log_path(path, "Stage 6: Construct bridges")

    # Step 7: resolve bridges
    path = resolve_components(path)
    log_path(path, "Stage 7: Resolve bridges")

    # Step 8: purge duplicates
    path = purge_duplicates(path)
    log_path(path, "Stage 8: Purge duplicates")

    # TODO better handling of this.
    # some system for component attributes.
    # what if a bridge design wants to support both?

    # TODO this is actually broken,
    # since it ignores JumpThrough rules
    if getattr(straight_compo, 'tl_dont_go_thru', False):
        straights_points = bridge_builder.straights_points_
    else:
        straights_points = [
            path[0].to,
            *[
                point for bend in bends for point in
                (bend.get_mark('tl_enter'), bend.get_mark('tl_exit'))
                ],
            path[-1].to,
            ]
        # TODO this is a mess

    # Step 9: construct straights
    straights = construct_straights(
        straights_points,
        straight_component=straight_compo
        )

    #path = newpath

    return path, bends, bridges, straights

def resolve_components(path):
    """
    Replace all components in path with raw points
    """
    newpath = path[0:1]
    for prev_conn, conn in pc.iter.duplets(path):
        if isinstance(conn.to, GoThru | pc.Component):
            newpath.extend(resolve_thru(conn))

        else:
            newpath.append(conn)

    return newpath

def resolve_startat(startat):
    """
    Resolve a StartAt that wraps a markable to a startat that
    wraps a raw point
    """
    if isinstance(startat.to, pc.Markable):
        return StartAt(startat.to.get_mark('tl_exit'))
    else:
        return startat

def resolve_elbows(path):
    newpath = path[0:1]
    for prev_conn, conn in pc.iter.duplets(path):
        if isinstance(conn, ElbowTo):
            newpath.extend(
                resolve_elbow(
                    prev_conn.to,
                    conn,
                    ),
                )
        else:
            newpath.append(conn)

    return newpath

def resolve_elbow(_from: pc.typing.Point, elbow: ElbowTo):
    """
    Convert single ElbowTo into three instances of StraightTo
    Expects POINTS!
    """
    if _from[0] == elbow.to[0] or _from[1] == elbow.to[1]:
        return [
            StraightTo(elbow.to)
            ]

    mid = pc.midpoint(_from, elbow.to)
    p1 = pc.Point(mid[0], _from[1])
    p2 = pc.Point(mid[0], elbow.to[1])
    return [
        StraightTo(p1),
        StraightTo(p2),
        StraightTo(elbow.to),
        ]

def resolve_meander(meander: MeanderTo):
    raise NotImplementedError

def resolve_thru(connection):
    """
    Given a connection to a GoThrough, return
    two new connections
    """
    if isinstance(connection.to, pc.Component):
        connection = copy(connection)
        connection.to = JumpThru(connection.to)

    connection1 = copy(connection)
    connection1.to = connection.to.markable.get_mark('tl_enter')
    connection2 = connection.to.how(connection.to.markable.get_mark('tl_exit'))

    return [connection1, connection2]

def construct_bends(path, bend_component, bend_radius):
    """
    Given path, component, and bend radius,
    create bends.
    """
    if __debug__:
        validate_construct_bends(path)

    newpath = path[0:1]
    bends = []

    for before, point, after in pc.iter.triplets(path):
        bend = construct_bend(
            bend_component,
            bend_radius,
            before.to,
            point.to,
            after.to
            )

        if bend:
            bends.append(bend)
            newpath.append(
                StraightTo(
                    JumpThru(
                        bend
                        )
                    )
                )

        else:
            # no turn here, just a straight line
            newpath.append(point)

        # The below TODO was copy-pasted from CPW.py,
        # not sure if its still relevant

        # TODO somehow freeze polygons/components
        # when they are added as subpolygons/subcomponents
        # so that they can't be used later on?
        #
        # Or, rather, can't be transformed/modified.
        #yield bend


    newpath.append(path[-1])

    return newpath, bends

def validate_path_structure(path, allowed_conns=Connection):
    """
    Validates the structure of a path:
    1. Must start with a StartAt connection
    2. All subsequent connections must be instances of anything in
        `allowed_conns`, but not StartAt.
    Throws exceptions if path is not correctly structured.
    """
    if not isinstance(path[0], StartAt):
        raise Exception(
            f"Path must start with StartAt, not {(path[0])} "
            f"(found {path[0]})."
            )

    for i, conn in enumerate(path[1:]):
        if isinstance(conn, StartAt):
            raise Exception(
                f"StartAt connection must be only at index 0, not {i} "
                f"(found {conn})."
                )

        if not isinstance(conn, allowed_conns):
            raise Exception(
                f"Found disallowed connection type {conn} at index {i} "
                f"(Only {allowed_conns} are allowed."
                )

def validate_path_targets(path, allowed_targets=ConnectionTarget):
    """
    """
    for i, conn in enumerate(path):
        if not isinstance(conn.to, allowed_targets):
            raise Exception(
                f"Found connection {conn} "
                f"with disallowed target at index {i}. "
                f"All targets must be of type {allowed_targets}."
                )

def validate_construct_bends(path):
    """
    Validates that a `path` is suitable to be passed into
    `construct_bends`, namely:
    1. Consists purely of StraightTo and JumpTo connections,
        except the first element, which must be a StartAt
    2. All connections point to Points, not markables
    """
    validate_path_structure(path, StraightTo | JumpTo)
    validate_path_targets(path, pc.typing.Point)
    

def construct_bend(bend_component, bend_radius, before, point, after):
    """
    Given component, bend radius, point of bend,
    and the points before and after,
    return created bend component
    """
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

    if abs(turn % pc.fullcircle) < 0.01:  # TODO standardize epsilon value
        # Straight turn
        log.debug("Straight.")
        return None

    if pc.pi * 1 > turn > 0:
        # Left turn
        log.debug("Left.")

        angle_turn_center = (
            angle_outgoing + angle_incoming + pc.semicircle
            ) / 2

        orientation = pc.Orientation.Counterclockwise

        angle_turn_start = angle_incoming - pc.quartercircle
        angle_turn_end = angle_outgoing - pc.quartercircle

    # TODO direction detection is still wonlky?
    elif turn < 0 or turn >= pc.pi:
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
        pc.point_polar(angle_turn_center, offset_turn_center)
        )

    bend = bend_component(opts=dict(
        angle_start=angle_turn_start,
        angle_end=angle_turn_end,
        #center=point_turn_center,
        orientation=orientation,
        ))

    bend.align_mark_to_point('center', point_turn_center)

    return bend

class BridgeBuilder:
    def __init__(
            self,
            bridge_compo: pc.typing.ComponentClass,
            base_spacing: float,
            spacing_scramble: float
            ):

        self.path = None
        self.bridge_compo = bridge_compo
        self.base_spacing = base_spacing
        self.spacing_scramble = spacing_scramble

        self.newpath_ = None
        self.bridges_ = None
        self.straights_points_ = None

    def build(self, path):

        self.path = path
        self.newpath_ = []
        self.bridges_ = []
        self.straights_points_ = []

        self.newpath_.append(self.path[0])
        #self.straights_points_.append(self.path[0].to)

        with LegBuilder(self) as leg_builder:
            for leg_start, leg_end in pc.iter.duplets(self.path):
                self.straights_points_.append(leg_start.to)
                leg_builder.build(leg_start, leg_end)

        self.newpath_.append(self.path[-1])
        self.straights_points_.append(self.path[-1].to)


class LegBuilder:
    def __init__(
            self,
            bridge_builder: BridgeBuilder,
            ):
        self.bridge_builder = bridge_builder

    def build(
            self,
            leg_start: Connection,
            leg_end: Connection,
            ):
        """
        Construct bridges for one "leg"
        (i.e. straight space between two bends).
        """
        self.leg_start = leg_start
        self.leg_end = leg_end

        if not isinstance(leg_end, StraightTo):
            # At this step, the only connection types should be
            # StraightTo (between bends)
            # and
            # JumpTo (across bends)
            self.bridge_builder.newpath_.append(leg_start)
            return

        leg_distance = pc.distance_between(leg_start.to, leg_end.to)

        if leg_distance < self.bridge_builder.base_spacing:
            self.bridge_builder.newpath_.append(leg_start)
            return

        self.leg_angle = pc.angle_between(leg_start.to, leg_end.to)

        # put a bridge at the start
        self._build_bridge(leg_start.to, reverse=False)

        # Put the remaining bridges_ along the leg
        bridge_positions = np.arange(
            0,
            leg_distance,
            self.bridge_builder.base_spacing,
            )[1:-1]

        for i, distance in enumerate(bridge_positions):
            bridge_coords = self._find_bridge_coords(distance)

            self._build_bridge(bridge_coords, reverse=False)

        # put a bridge at the end
        self._build_bridge(leg_end.to, reverse=True)

    def _find_bridge_coords(
            self,
            distance: float,
            ):

        scramble_distance = (
            bridge_rng.uniform(-1, 1) * self.bridge_builder.spacing_scramble
            )

        bridge_coords = (
            + self.leg_start.to
            + pc.point_polar(
                self.leg_angle,
                distance + scramble_distance
                )
            )

        return bridge_coords

    def _build_bridge(
            self,
            point: pc.typing.Point,
            reverse: bool = False,
            ):
        """
        Given a startpoint and rotation (leg angle), add a bridge
        """
        if reverse:
            # TODO get rid of magic strings!
            mark_name = 'tl_exit'
        else:
            mark_name = 'tl_enter'
            angle = pc.semicircle - self.leg_angle

        bridge = self.bridge_builder.bridge_compo()
        bridge.align_mark_to_point(mark_name, point)
        bridge.rotate_around_mark(mark_name, self.leg_angle)

        self.bridge_builder.bridges_.append(bridge)
        self.bridge_builder.newpath_.append(
            StraightTo(JumpThru(bridge))
            )

        self.bridge_builder.straights_points_.append(
            bridge.get_mark('tl_enter')
            )
        self.bridge_builder.straights_points_.append(
            bridge.get_mark('tl_exit')
            )


    # TODO does this do what I think it does??

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.bridge_builder = None

    def __del__(self):
        self.bridge_builder = None

def validate_construct_bridges(path):
    validate_path_structure(path, StraightTo | JumpTo)
    validate_path_targets(path, pc.typing.Point)

def purge_duplicates(
        path
        ):

    newpath = path[0:1]

    for point in path[1:]:
        if pc.distance_between(point.to, newpath[-1].to) > 0.01:
            newpath.append(point)

    # TODO step to purge repeated JumpTos?

    return newpath

def construct_straights(
        points,
        straight_component: pc.typing.ComponentClass,
        ):

    straights = []

    for point, next_point in pc.iter.couples(points):

        angle, length = pc.to_polar(point, next_point)

        # TODO logically, the next three lines should be broken out
        # into a separate function (same as with construct_bend
        # or construct_bridge)
        straight = straight_component(opts=pc.Dict(
            length=length,
            ))

        straight.align_mark_to_point('tl_enter', point)
        straight.rotate_around_mark('tl_enter', angle)

        straights.append(straight)

    return straights

def get_path_bounds(path):
    """
    Return [x1, y1, x2, y2] bounding box of path
    """
    return pc.BBox([
        conn.to for conn in path
        if isinstance(conn.to, np.ndarray)
        ])

def _render_path_as_svg(svg, path):
    for conn, next_conn in pc.iter.duplets(path):
        if isinstance(conn.to, np.ndarray):
            svg.circle(*conn.to, name=repr(conn))
            if isinstance(next_conn.to, np.ndarray):
                svg.line(*conn.to, *next_conn.to)
    svg.circle(*next_conn.to)

def render_path_as_svg(path, stream=None):
    """
    Render path as svg, return stream
    """
    svg = pc.viz.SVG(stream=stream)
    _render_path_as_svg(svg, path)
    svg.done()

    return stream or svg.stream

def render_paths_as_svg(paths, stream=None):
    svg = pc.viz.SVG(stream=stream)
    for path in paths:
        _render_path_as_svg(svg, path)
        svg.collage_E()
    svg.done()


    return stream or svg.stream

