from dataclasses import dataclass
from typing import Iterable

import pycif as pc
from pycif.draw import TransmissionLine as tl

@dataclass
class StraightSpec:
    start: pc.Point
    angle: float
    length: float

def construct_straights(path):
    specs = []
    for conn, after in pc.iter.duplets(path):
        if not isinstance(after, tl.StraightTo):
            continue

        specs.append(StraightSpec(
            start=conn.to,
            angle=pc.angle_between(conn.to, after.to),
            length=pc.distance_between(conn.to, after.to)
            ))

    return path, specs

def make_straight_component(spec: StraightSpec, Compo: pc.typing.ComponentClass):
    return (
        Compo(options=dict(length=spec.length))
        .marks.tl_enter.to(spec.start)
        .marks.tl_enter.rotate(spec.angle)
        )

def make_straight_components(
        specs: Iterable[StraightSpec],
        Compo: pc.typing.ComponentClass,
        ):
    return [
        make_straight_component(spec, Compo)
        for spec in specs
        ]

