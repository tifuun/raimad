from functools import partial, reduce
from collections import defaultdict
import raimad as rai
from raimad.types import Vec2S, PolyS, PolysS, GeomsS
from typing import Callable, TypeVar, TypeAlias, Iterable, Any, Sequence

def hash_vec2(vec2: Vec2S) -> int:
    return hash(vec2)

#def canon_micron(vec2: Vec2S) -> tuple[int, int]:
def canon_micron(vec2: Vec2S) -> Vec2S:
    return (
        round(vec2[0] * 100),
        round(vec2[1] * 100),
        )

def tf_vec2_in_poly(
        fn: Callable[[Vec2S], Vec2S],
        poly: PolyS,
        ) -> PolyS:
    return list(map(fn, poly))

def hash_poly(poly: PolyS) -> int:
    return hash(tuple(poly))

def canon_rot(poly: PolyS) -> PolyS:
    return min(
        (rai.cycled(poly, count) for count in range(len(poly))),
        key=hash_poly
        )

def canon_rot_or(poly: PolyS) -> PolyS:
    return min(
        (
            rai.cycled(rpoly, count)
            for rpoly in (poly, rai.reversed(poly))
            for count in range(len(poly))
            ),
        key=hash_poly
        )

def canon_or(poly: PolyS) -> PolyS:
    return min(
        (poly, rai.reversed_pin(poly)),
        key=hash_poly
        )

CanoniserVec2: TypeAlias = Callable[[Vec2S], Vec2S] | None
CanoniserPoly: TypeAlias = Callable[[PolyS], PolyS] | None
CanoniserPolys: TypeAlias = Callable[[PolysS], PolysS] | None
CanoniserGeoms: TypeAlias = Callable[[GeomsS], GeomsS] | None

def poly_equal(
        polys: Iterable[PolyS],
        canon_poly: CanoniserPoly = None,
        canon_vec2: CanoniserVec2 = None,
        ) -> bool:

    if canon_vec2 is not None:
        polys = tuple(tf_vec2_in_poly(canon_vec2, poly) for poly in polys)

    if canon_poly is not None:
        polys = tuple(canon_poly(poly) for poly in polys)

    return len(set(map(hash_poly, polys))) == 1

def canon_order(polys: PolysS) -> PolysS:
    return list(sorted(polys, key=hash_poly))

def hash_polys(polys: PolysS) -> int:
    return hash(tuple(map(tuple, polys)))

def tf_vec2_in_polys(fn: Callable[[Vec2S], Vec2S], polys: PolysS) -> PolysS:
    return [
        [fn(vec2) for vec2 in poly]
        for poly in polys
        ]

def tf_poly_in_polys(fn: Callable[[PolyS], PolyS], polys: PolysS) -> PolysS:
    return list(map(fn, polys))

def polys_equal(
        polyss: Iterable[PolysS],
        canon_polys: CanoniserPolys = None,
        canon_poly: CanoniserPoly = None,
        canon_vec2: CanoniserVec2 = None,
        ) -> bool:

    if canon_vec2 is not None:
        polyss = tuple(tf_vec2_in_polys(canon_vec2, polys) for polys in polyss)

    if canon_poly is not None:
        polyss = tuple(tf_poly_in_polys(canon_poly, polys) for polys in polyss)

    if canon_polys is not None:
        polyss = tuple(canon_polys(polys) for polys in polyss)

    return len(set(map(hash_polys, polyss))) == 1

def hash_geoms(geoms: GeomsS) -> int:
    hashable = tuple((layer, tuple(map(tuple, polys))) for layer, polys in geoms.items())
    #print(f"{geoms = }")
    #print(f"{hashable = }")
    #print(f"{hash(hashable) = }")
    return hash(hashable)

def tf_vec2_in_geoms(fn: Callable[[Vec2S], Vec2S], geoms: GeomsS) -> GeomsS:
    return {
            layer: [
                [fn(vec2) for vec2 in poly]
                for poly in polys
                ]
            for layer, polys in geoms.items()
        }

def tf_poly_in_geoms(fn: Callable[[PolyS], PolyS], geoms: GeomsS) -> GeomsS:
    return {
            layer: [
                fn(poly)
                for poly in polys
                ]
            for layer, polys in geoms.items()
        }

def tf_polys_in_geoms(fn: Callable[[PolysS], PolysS], geoms: GeomsS) -> GeomsS:
    return {
            layer: fn(polys)
            for layer, polys in geoms.items()
        }

def canon_layer_order(geoms: GeomsS) -> GeomsS:
    # TODO what to do about duplicate layer names,,?
    # or wait thats not even possible because dict..??
    return dict(sorted(tuple(geoms.items()), key=lambda pair: pair[0]))

def geoms_equal(
        geomss: Iterable[GeomsS],
        canon_geoms: CanoniserGeoms = None,  # TODO
        canon_polys: CanoniserPolys = None,
        canon_poly: CanoniserPoly = None,
        canon_vec2: CanoniserVec2 = None,
        ) -> bool:

    if canon_vec2 is not None:
        geomss = tuple(tf_vec2_in_geoms(canon_vec2, geoms) for geoms in geomss)

    if canon_poly is not None:
        geomss = tuple(tf_poly_in_geoms(canon_poly, geoms) for geoms in geomss)

    if canon_polys is not None:
        geomss = tuple(tf_polys_in_geoms(canon_polys, geoms) for geoms in geomss)

    if canon_geoms is not None:
        geomss = tuple(canon_geoms(geoms) for geoms in geomss)

    return len(set(map(hash_geoms, geomss))) == 1

