"""
geom.py: Operations on geometric data.

By "geometric data" I mean `Vec2S`, `PolyS`, `PolysS`, and `GeomsS`
data types from `rai.types`.

"""

import raimad as rai
from raimad.types import Vec2S, PolyS, PolysS, GeomsS
from typing import Callable, TypeAlias, Iterable

def hash_vec2(vec2: Vec2S) -> int:
    """
    Hash a Vec2S.

    This method is mainly here for the other methods of `rai.geom` to use.
    It may or may not be a thin wrapper around Python's built-in `hash`.
    In many usecases, the builtin `hash` may be more clear than this method.
    """
    return hash(vec2)

#def canon_micron(vec2: Vec2S) -> tuple[int, int]:
def canon_micron(vec2: Vec2S) -> Vec2S:
    """
    Canonicalise Vec2S: snap to closest micron.

    This will multiply both coordinates by 100 and round to the nearest int,
    just like the CIF exporters do by default.

    Notes
    -----
    - Banker's rounding, normal rounding, floor, or ceil? I dont know! TODO!!

    See Also
    --------
    TODO link to explanation of geom canonicalisation, once that is written.

    Examples
    --------
    >>> rai.geom.canon_micron((10.00001, 30.00001))
    (1000, 3000)

    """
    return (
        round(vec2[0] * 100),
        round(vec2[1] * 100),
        )

def tf_vec2_in_poly(
        fn: Callable[[Vec2S], Vec2S],
        poly: PolyS,
        ) -> PolyS:
    """
    Transform each Vec2S in a PolyS.

    Applies `fn` to each Vec2S in `poly` and return a new PolyS
    with the result.

    """
    return list(map(fn, poly))

def hash_poly(poly: PolyS) -> int:
    """
    Hash a PolyS.

    This method is mainly here for the other methods of `rai.geom` to use.
    It may or may not be a thin wrapper around Python's built-in `hash`.
    In many usecases, the builtin `hash` may be more clear than this method.
    """
    return hash(tuple(poly))

def canon_rot(poly: PolyS) -> PolyS:
    """
    Canonicalise PolyS: by cycling.

    This will return a cycled version of `poly` (potentially unchanged)
    such that the value of `hash_poly(poly)` is minimized.
    This is useful for comparing polys when you don't care about
    which point comes first --
    for example, when you want to
    check that rotating a shape doesn't change its actual footprint.

    Notes
    -----
    - Is this stable across different instances of Python? I don't know!!

    See Also
    --------
    - TODO link the other canon methods
    - By "cycle" we mean `rai.cycle` TODO link.
    TODO link to explanation of geom canonicalisation, once that is written.

    """
    return min(
        (rai.cycled(poly, count) for count in range(len(poly))),
        key=hash_poly
        )

def canon_rot_or(poly: PolyS) -> PolyS:
    """
    Canonicalise PolyS: by cycling and orientation.

    This will return a (potentially) cycled and (potentially) reversed
    copy of `poly` such that the value of `hash_poly(poly)` is minimised.
    This is useful for comparing polys when you don't care about
    which point comes first --
    for example, when you want to
    check that rotating a shape doesn't change its actual footprint.

    As opposed to `canon_rot`, which can only cycle the poly,
    this method can also reverse it.
    Maybe useful for checking that mirroring a shape doesn't change its
    footprint.

    Notes
    -----
    - Is this stable across different instances of Python? I don't know!!

    See Also
    --------
    - TODO link the other canon methods
    - By "cycle" we mean `rai.cycle` TODO link.
    TODO link to explanation of geom canonicalisation, once that is written.

    """
    return min(
        (
            rai.cycled(rpoly, count)
            for rpoly in (poly, rai.reversed(poly))
            for count in range(len(poly))
            ),
        key=hash_poly
        )

def canon_or(poly: PolyS) -> PolyS:
    """
    Canonicalise PolyS: by orientation only.

    This will return a (potentially) reversed
    copy of `poly` such that the value of `hash_poly(poly)` is minimised.
    This method is not particularly useful, since
    I can't think of a single transformation that reverses the order
    of the points but keeps a particular point in its original index
    in a way that is intuitively predictable.

    The reverse operation used in this method is `rai.reversed_pin`.
    In other words, the point at index 0 of `poly` is guaranteed to be
    the same in the output as in the input.

    Notes
    -----
    - Is this stable across different instances of Python? I don't know!!

    See Also
    --------
    - TODO link the other canon methods
    - By "cycle" we mean `rai.cycle` TODO link.
    TODO link to explanation of geom canonicalisation, once that is written.

    """
    return min(
        (poly, rai.reversed_pin(poly)),
        key=hash_poly
        )

# TODO docstrings for typehints? Possible??
CanoniserVec2: TypeAlias = Callable[[Vec2S], Vec2S] | None
CanoniserPoly: TypeAlias = Callable[[PolyS], PolyS] | None
CanoniserPolys: TypeAlias = Callable[[PolysS], PolysS] | None
CanoniserGeoms: TypeAlias = Callable[[GeomsS], GeomsS] | None

def poly_equal(
        polys: Iterable[PolyS],
        canon_poly: CanoniserPoly = None,
        canon_vec2: CanoniserVec2 = None,
        ) -> bool:
    """
    Check whether a group of PolyS are equal under some canonicalization.

    This works by applying the given canonicalizations
    first to each point (Vec2), then to each PolyS itself,
    and then using
    the `hash_poly` function to
    whether they all produce the same hash.

    Parameters
    ----------
    polys
        The iterable of PolyS to compare with each other

    canon_poly
        Canonicalisation of each PolyS within each PolysS.
        This is applied LAST, AFTER canon_vec2
        `None` for noop.

    canon_vec2
        Canonicalisation of each Vec2S within each PolyS.
        This is applied FIRST.
        `None` for noop.

    Returns
    -------
    bool
        True if all PolyS are equal (produce the same hash).
        False otherwise.
    """

    if canon_vec2 is not None:
        polys = tuple(tf_vec2_in_poly(canon_vec2, poly) for poly in polys)

    if canon_poly is not None:
        polys = tuple(canon_poly(poly) for poly in polys)

    return len(set(map(hash_poly, polys))) == 1

def canon_order(polys: PolysS) -> PolysS:
    """
    Canonicalise PolysS: by order of polygons.

    This will return a copy of `polys`, sorted in ascending order.
    `hash_poly` is used as the key for the sorting operation.
    This is useful for comparing two PolysS when you don't care
    about the order of the PolysS within them.

    Notes
    -----
    - Is this stable across different instances of Python? I don't know!!

    See Also
    --------
    TODO link to explanation of geom canonicalisation, once that is written.

    """
    return list(sorted(polys, key=hash_poly))

def hash_polys(polys: PolysS) -> int:
    """
    Hash a PolysS.

    This method is mainly here for the other methods of `rai.geom` to use.
    It may or may not be a thin wrapper around Python's built-in `hash`.
    In many usecases, the builtin `hash` may be more clear than this method.
    """
    return hash(tuple(map(tuple, polys)))

def tf_vec2_in_polys(fn: Callable[[Vec2S], Vec2S], polys: PolysS) -> PolysS:
    """
    Transform each Vec2S in a PolysS.

    Applies `fn` to each Vec2S in `polys` and return a new PolysS
    with the result.

    """
    return [
        [fn(vec2) for vec2 in poly]
        for poly in polys
        ]

def tf_poly_in_polys(fn: Callable[[PolyS], PolyS], polys: PolysS) -> PolysS:
    """
    Transform each PolyS in a PolysS.

    Applies `fn` to each PolyS in `polys` and return a new PolysS
    with the result.

    """
    return list(map(fn, polys))

def polys_equal(
        polyss: Iterable[PolysS],
        canon_polys: CanoniserPolys = None,
        canon_poly: CanoniserPoly = None,
        canon_vec2: CanoniserVec2 = None,
        ) -> bool:
    """
    Check whether a group of PolysS are equal under some canonicalization.

    This works by applying the given canonicalizations
    to all the geometric primitives starting with
    the points (Vec2S), then hashing each PolysS
    with the `hash_polys` function and checking
    whether they all produce the same hash.

    Parameters
    ----------
    polyss
        The iterable of PolysS to compare with each other

    canon_polys
        Canonicalisation of each PolysS.
        This is applied LAST, AFTER canon_poly.
        `None` for noop.

    canon_poly
        Canonicalisation of each PolyS within each PolysS.
        This is applied AFTER canon_vec2.
        `None` for noop.

    canon_vec2
        Canonicalisation of each Vec2S within each PolyS.
        This is applied FIRST.
        `None` for noop.

    Returns
    -------
    bool
        True if all PolysS are equal (produce the same hash).
        False otherwise.
    """

    if canon_vec2 is not None:
        polyss = tuple(tf_vec2_in_polys(canon_vec2, polys) for polys in polyss)

    if canon_poly is not None:
        polyss = tuple(tf_poly_in_polys(canon_poly, polys) for polys in polyss)

    if canon_polys is not None:
        polyss = tuple(canon_polys(polys) for polys in polyss)

    return len(set(map(hash_polys, polyss))) == 1

def hash_geoms(geoms: GeomsS) -> int:
    """
    Hash a GeomsS.

    This method is mainly here for the other methods of `rai.geom` to use.
    It may or may not be a thin wrapper around Python's built-in `hash`.
    In many usecases, the builtin `hash` may be more clear than this method.
    """
    hashable = tuple(
        (layer, tuple(map(tuple, polys)))
        for layer, polys in geoms.items()
        )
    #print(f"{geoms = }")
    #print(f"{hashable = }")
    #print(f"{hash(hashable) = }")
    return hash(hashable)

def tf_vec2_in_geoms(fn: Callable[[Vec2S], Vec2S], geoms: GeomsS) -> GeomsS:
    """
    Transform each Vec2S in a GeomsS.

    Applies `fn` to each Vec2S in `geoms` and return a new GeomsS
    with the result.

    """
    return {
            layer: [
                [fn(vec2) for vec2 in poly]
                for poly in polys
                ]
            for layer, polys in geoms.items()
        }

def tf_poly_in_geoms(fn: Callable[[PolyS], PolyS], geoms: GeomsS) -> GeomsS:
    """
    Transform each PolyS in a GeomsS.

    Applies `fn` to each PolyS in `geoms` and return a new GeomsS
    with the result.

    """
    return {
            layer: [
                fn(poly)
                for poly in polys
                ]
            for layer, polys in geoms.items()
        }

def tf_polys_in_geoms(fn: Callable[[PolysS], PolysS], geoms: GeomsS) -> GeomsS:
    """
    Transform each PolysS in a GeomsS.

    Applies `fn` to each PolysS in `geoms` and return a new GeomsS
    with the result.

    """
    return {
            layer: fn(polys)
            for layer, polys in geoms.items()
        }

def canon_layer_order(geoms: GeomsS) -> GeomsS:
    """
    Canonicalise GeomsS: by layer order.

    Python dicts are ordered since Python 3.7.
    This will sort the entries of the GeomsS by key (layer name)
    using Python's built-in `sorted`.
    Useful for checking that two GeomsS are the same.

    See Also
    --------
    TODO link to explanation of geom canonicalisation, once that is written.

    """
    # TODO what to do about duplicate layer names,,?
    # or wait thats not even possible because dict..??
    return dict(sorted(tuple(geoms.items()), key=lambda pair: pair[0]))

def canon_no_layer_names(geoms: GeomsS) -> GeomsS:
    """
    Canonicalise GeomsS: by layer content, ignoring names.

    This will canonicalize a GeomsS by sorting them by their content
    (using `hash_polys` as key),
    and replacing all layer names with `L{integer starting with 0}`.
    Useful for checking that two GeomsS have the same geometric content
    regardless of layer names.

    See Also
    --------
    TODO link to explanation of geom canonicalisation, once that is written.

    """
    # TODO what to do about duplicate layer names,,?
    # or wait thats not even possible because dict..??
    return {
        f"L{i}": v
        for (i, (_k, v)) in enumerate(sorted(
            geoms.items(), key=lambda pair: hash_polys(pair[1])))
        }

def geoms_equal(
        geomss: Iterable[GeomsS],
        canon_geoms: CanoniserGeoms = None,  # TODO
        canon_polys: CanoniserPolys = None,
        canon_poly: CanoniserPoly = None,
        canon_vec2: CanoniserVec2 = None,
        ) -> bool:
    """
    Check whether a group of GeomsS are equal under some canonicalization.

    This works by applying the given canonicalizations
    to all the geometric primitives starting with
    the points (Vec2S), then hashing each GeomsS
    with the `hash_geoms` function and checking
    whether they all produce the same hash.

    Parameters
    ----------
    geomss
        The iterable of GeomsS to compare with each other

    canon_geoms
        Canonicalisation of GeomsS. This is applied LAST, AFTER canon_polys.
        `None` for noop.

    canon_polys
        Canonicalisation of each PolysS within each GeomsS.
        This is applied AFTER canon_poly.
        `None` for noop.

    canon_poly
        Canonicalisation of each PolyS within each PolysS.
        This is applied AFTER canon_vec2.
        `None` for noop.

    canon_vec2
        Canonicalisation of each Vec2S within each PolyS.
        This is applied FIRST.
        `None` for noop.

    Returns
    -------
    bool
        True if all GeomsS are equal (produce the same hash).
        False otherwise.
    """

    if canon_vec2 is not None:
        geomss = tuple(tf_vec2_in_geoms(canon_vec2, geoms) for geoms in geomss)

    if canon_poly is not None:
        geomss = tuple(tf_poly_in_geoms(canon_poly, geoms) for geoms in geomss)

    if canon_polys is not None:
        geomss = tuple(tf_polys_in_geoms(canon_polys, geoms) for geoms in geomss)

    if canon_geoms is not None:
        geomss = tuple(canon_geoms(geoms) for geoms in geomss)

    return len(set(map(hash_geoms, geomss))) == 1

