from functools import partial
from collections import defaultdict
import raimad as rai

def hash_vec2(vec2):
    return hash(vec2)

def canon_micron(vec2):
    return tuple(map(lambda coord: round(coord * 100), vec2))

def map_vec2_in_poly(fn, poly):
    return list(map(fn, poly))

def hash_poly(poly):
    return hash(tuple(map_vec2_in_poly(hash_vec2, poly)))

def canon_rot(poly):
    return min(
        (rai.rotated(poly, count) for count in range(len(poly))),
        key=hash_poly
        )

def canon_rot_or(poly):
    return min(
        (
            rai.rotated(rpoly, count)
            for rpoly in (poly, rai.reversed(poly))
            for count in range(len(poly))
            ),
        key=hash_poly
        )

def canon_or(poly):
    return min(
        (poly, rai.reversed_pin(poly)),
        key=hash_poly
        )

def poly_equal(one, two, canon_poly=None, canon_vec2=None):
    if canon_vec2 is not None:
        one = map_vec2_in_poly(canon_vec2, one)
        two = map_vec2_in_poly(canon_vec2, two)

    if canon_poly is not None:
        one = canon_poly(one)
        two = canon_poly(two)

    return hash_poly(one) == hash_poly(two)

def canon_order(polys):
    return list(sorted(polys, key=hash_poly))

def hash_polys(polys):
    return hash(tuple(map(hash_poly, polys)))

def map_vec2_in_polys(fn, polys):
    return [
        [fn(vec2) for vec2 in poly]
        for poly in polys
        ]

def map_poly_in_polys(fn, polys):
    return list(map(fn, polys))

def polys_equal(one, two, canon_polys=None, canon_poly=None, canon_vec2=None):
    if canon_vec2 is not None:
        one = map_vec2_in_polys(canon_vec2, one)
        two = map_vec2_in_polys(canon_vec2, two)

    if canon_poly is not None:
        one = map_poly_in_polys(canon_poly, one)
        two = map_poly_in_polys(canon_poly, two)

    if canon_polys is not None:
        one = canon_polys(one)
        two = canon_polys(two)

    return hash_polys(one) == hash_polys(two)

