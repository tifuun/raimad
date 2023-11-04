from dataclasses import dataclass
from typing import Iterable

import PyCIF as pc
from PyCIF.draw import TransmissionLine as tl

log = pc.get_logger(__name__)

@dataclass
class BendSpec:
    angle_start: float
    angle_end: float
    radius: float
    orientation: pc.Orientation
    point_enter: pc.Point
    point_exit: pc.Point
    point_center: pc.Point

def construct_bends(path, radius, striped=False):
    newpath = []
    bendspecs = []

    newpath.append(path[0])

    if len(path) < 3:
        newpath.append(path[1])
        return newpath, []

    default_radius = radius

    for before, conn, after in pc.iter.triplets(path):

        radius = conn.radius or (radius if striped else default_radius)

        bendspec = construct_bend(
            before.to, conn.to, after.to, radius)

        if bendspec is None:
            newpath.append(conn)
            continue

        newpath.append(
            tl.StraightTo(
                bendspec.point_enter
                )
            )
        newpath.append(
            tl.JumpTo(
                bendspec.point_exit
                )
            )
        bendspecs.append(bendspec)

    newpath.append(after)
    return newpath, bendspecs

def construct_bend(before, point, after, radius):
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

    match pc.classify_turn(before, point, after):
        case pc.TurnDirection.Straight:
            # Straight turn
            # TODO print warning here?
            log.debug("Straight.")
            return None

        case pc.TurnDirection.Left:
            # Left turn
            log.debug("Left.")

            angle_turn_center = (
                angle_outgoing + angle_incoming + pc.semicircle
                ) / 2

            orientation = pc.Orientation.Counterclockwise

            angle_turn_start = angle_incoming - pc.quartercircle
            angle_turn_end = angle_outgoing - pc.quartercircle

        case pc.TurnDirection.Right:
            # Right turn
            log.debug("Right.")

            angle_turn_center = (
                angle_outgoing + angle_incoming - pc.semicircle
                ) / 2

            orientation = pc.Orientation.Clockwise

            angle_turn_start = angle_incoming - 3 * pc.quartercircle
            angle_turn_end = angle_outgoing - 3 * pc.quartercircle

        case _:
            assert False

    offset_turn_center = radius / pc.sin(corner_angle / 2)

    point_turn_center = (
        point +
        pc.Point(arg=angle_turn_center, mag=offset_turn_center)
        )

    point_enter = (
        point_turn_center +
        pc.Point(arg=angle_turn_start, mag=radius)
        )

    point_exit = (
        point_turn_center +
        pc.Point(arg=angle_turn_end, mag=radius)
        )

    return BendSpec(
        angle_start=angle_turn_start,
        angle_end=angle_turn_end,
        radius=radius,
        orientation=orientation,
        point_enter=point_enter,
        point_exit=point_exit,
        point_center=point_turn_center,
        )

def make_bend_component(spec: BendSpec, Compo: pc.typing.ComponentClass):
    return Compo(options=dict(
        angle_start=spec.angle_start,
        angle_end=spec.angle_end,
        orientation=spec.orientation,
        bend_radius=spec.radius,
        )).marks.center.to(spec.point_center)

def make_bend_components(
        specs: Iterable[BendSpec],
        Compo: pc.typing.ComponentClass
        ):
    return [
        make_bend_component(spec, Compo)
        for spec in specs
        ]


