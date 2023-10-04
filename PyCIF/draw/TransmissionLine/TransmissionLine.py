"""
"""
from typing import Sequence
import logging

import PyCIF as pc

log = pc.get_logger(__name__)

class TransmissionLine:
    bends_: Sequence[pc.Component]
    bridges_: Sequence[pc.Component]
    straights_: Sequence[pc.Component]

    bend_radius: float  # at start of connection
    bridge_spacing: float
    bridge_scramble: float
    bridge_width: float
    bridges: bool

    def __init__(
            self,
            path,
            bend_radius: float,  # at start of connection
            bridge_spacing: float,
            bridge_scramble: float,
            bridge_width: float,
            bridges: bool = True,
            ):
        self.bend_radius = bend_radius
        self.bridge_spacing = bridge_spacing
        self.bridge_scramble = bridge_scramble
        self.bridge_width = bridge_width
        self.bridges = bridges

        log.debug('====== Original path ======')
        log.debug(pc.tl.format_path(path))

        path1 = pc.tl.resolve_elbows(path)
        log.debug('====== Step 1: resolve elbows ======')
        log.debug(pc.tl.format_path(path1))

        path2 = pc.tl.reduce_straights(path1)
        log.debug('====== Step 2: reduce straights ======')
        log.debug(pc.tl.format_path(path2))

        path3, self._bendspecs = pc.tl.construct_bends(
            path2,
            radius=self.bend_radius,
            )
        log.debug('====== Step 3: construct bends ======')
        log.debug(pc.tl.format_path(path3))

        path4, self._bridgespecs = pc.tl.construct_bridges(
            path3,
            spacing=self.bridge_spacing,
            scramble=self.bridge_scramble,
            bridge_width=self.bridge_width,
            )
        log.debug('====== Step 4: construct bridges ======')
        log.debug(pc.tl.format_path(path4))

        self._resolved_path = path4
        # TODO type for path

    def make_bends(self, bend_compo: pc.typing.ComponentClass):
        self.bends_ = pc.tl.make_bend_components(
            self._bendspecs,
            bend_compo
            )
        return self.bends_

    def make_bridges(self, bridge_compo: pc.typing.ComponentClass):
        self.bridges_ = pc.tl.make_bridge_components(
            self._bridgespecs,
            bridge_compo
            )
        return self.bridges_

    def make_straights(self, straight_compo: pc.typing.ComponentClass):
        self.straights_ = pc.tl.make_straight_components(
            self._resolved_path,
            straight_compo
            )
        return self.straights_

