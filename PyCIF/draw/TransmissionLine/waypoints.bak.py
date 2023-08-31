"""
Waypoints -- specify what points a transmissionline can visit.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Sequence

import numpy as np

import PyCIF as pc

@dataclass
class Waypoint:
    """
    Specifies point and whether or not to place a segment until the
    next point
    """
    point: np.ndarray  # FIXME point type
    do_segment: bool

@dataclass
class WayMarkable:
    markable: pc.Markable
    do_segment: bool

ShorthandWaypoint = (
    Waypoint
    | pc.Markable
    | pc.WayMarkable
    | np.ndarray
    )
# FIXME point type

Waypoints = Sequence[Waypoint]
ShorthandWaypoints = Sequence[ShorthandWaypoints]


class SegmentStyle(Enum):
    NONE = 0
    STRAIGHT = 1
    RIGHTANGLE = 2



# Shorthand Waypoints:
# 1. Starts and ends with waypoints or components
# 2. In between there may be components or WayComponents
# 3. In between there may be SegmentStyles

# Canonical Waypoints:
# 1. Consists entirely of WayPoint's

def canonicalize(
        wpoint: ShorthandWaypoint,
        next_wpoint: ShorthandWaypoint | None,
        do_segment: bool,
        ):

    if isinstance(wpoint, Waypoint):
        return [wpoint, next_wpoint]

    elif isinstance(wpoint, np.ndarray):  # FIXME point type
        if next_wpoint is None:
            return [
                Waypoint(
                    wpoint,
                    do_segment,
                    ),
                next_wpoint
                ]

        elif isinstance(next_wpoint, SegmentStyle):
            if next_wpoint is SegmentStyle.NONE:
                return [
                    Waypoint(
                        wpoint,
                        False,
                        )
                    ]

            elif next_wpoint is SegmentStyle.STRAIGHT:
                return [
                    Waypoint(
                        wpoint,
                        True,
                        )
                    ]

            else:
                # TODO right angle routing
                pass

    elif isinstance(wpoint, pc.Markable):
        return [
            Waypoint(
                wpoint.get_mark('tl_enter'),
                do_segment,
                ),
            *canonicalize(
                wpoint.get_mark('tl_exit'),
                next_wpoint
                )
            ]

    elif isinstance(wpoint, WayMarkable):
        return canonicalize(
            wpoint.markable,
            next_wpoint
            )



    return [
        Waypoint(
            self.markable.get_mark('tl_enter'),
            slef.do_segment_between,
            ),
        Waypoint(
            self.markable.get_mark('tl_exit'),
            slef.do_segment_after,
            ),
        ]


def canonicalize_markables(wpoints: ShorthandWaypoints, do_segment: bool):
    """
    """
    new_wpoints = []

    for wpoint in wpoints:
        if isinstance(wpoint, pc.Markable):
            new_wpoints.append(Waypoint(
                wpoint.get_mark('tl_enter'),
                do_segment
                ))

            new_wpoints.append(Waypoint(
                wpoint.get_mark('tl_exit'),
                do_segment
                ))

            # FIXME have or have not segment?

        elif isinstance(wpoint, WayMarkable):
            new_wpoints.append(Waypoint(
                wpoint.markable.get_mark('tl_enter'),
                wpoint.do_segment
                ))

            new_wpoints.append(Waypoint(
                wpoint.markable.get_mark('tl_exit'),
                wpoint.do_segment
                ))

