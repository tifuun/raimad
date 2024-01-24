"""
"""
from typing import Sequence
import logging

import pycif as pc

from .resolvers.bends import BendSpec
from .resolvers.straights import StraightSpec
from .resolvers.bridges import BridgeSpec

log = pc.get_logger(__name__)

class TransmissionLine:
    bends_: Sequence[pc.Compo]
    bridges_: Sequence[pc.Compo]
    straights_: Sequence[pc.Compo]

    bendspecs_: Sequence[BendSpec]
    bridgespecs_: Sequence[BridgeSpec]
    straightspecs_: Sequence[StraightSpec]

    bend_radius: float  # at start of connection
    bridge_spacing: float
    bridge_scramble: float
    bridge_length: float
    do_bridges: bool

    def __init__(
            self,
            path,
            bend_radius: float,  # at start of connection
            bridge_spacing: float,
            bridge_scramble: float,
            bridge_length: float,
            do_bridges: bool = True,
            ):
        self.bend_radius = bend_radius
        self.bridge_spacing = bridge_spacing
        self.bridge_scramble = bridge_scramble
        self.bridge_length = bridge_length
        self.do_bridges = do_bridges

        self.path = path

    def make_specs(self):
        log.debug('====== Original path ======')
        log.debug(pc.tl.format_path(self.path))

        path1 = pc.tl.resolve_elbows(self.path)
        log.debug('====== Step 1: resolve elbows ======')
        log.debug(pc.tl.format_path(path1))

        path2 = path1
        #path2 = pc.tl.reduce_straights(path1)
        #log.debug('====== Step 2: reduce straights ======')
        #log.debug(pc.tl.format_path(path2))

        path3, self.bendspecs_ = pc.tl.construct_bends(
            path2,
            radius=self.bend_radius,
            )
        log.debug('====== Step 3: construct bends ======')
        log.debug(pc.tl.format_path(path3))

        path4, self.bridgespecs_ = pc.tl.construct_bridges(
            path3,
            do_bridges=self.do_bridges,
            spacing=self.bridge_spacing,
            scramble=self.bridge_scramble,
            bridge_length=self.bridge_length,
            )
        log.debug('====== Step 4: construct bridges ======')
        log.debug(pc.tl.format_path(path4))

        _, self.straightspecs_ = pc.tl.construct_straights(path4)

        self._resolved_path = path4
        # TODO type for path

    def make_bends(self, bend_compo: pc.typing.CompoClass):
        self.bends_ = pc.tl.make_bend_compos(
            self.bendspecs_,
            bend_compo
            )
        return self.bends_

    def make_bridges(self, bridge_compo: pc.typing.CompoClass):
        self.bridges_ = pc.tl.make_bridge_compos(
            self.bridgespecs_,
            bridge_compo
            )
        return self.bridges_

    def make_straights(self, straight_compo: pc.typing.CompoClass):
        self.straights_ = pc.tl.make_straight_compos(
            self.straightspecs_,
            straight_compo
            )
        return self.straights_

