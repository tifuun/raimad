from functools import partial
from collections import defaultdict
import raimad as rai

def hash_poly(poly):
    return hash(tuple(poly))

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

def poly_equal(one, two, canon_poly=None):
    if canon_poly is not None:
        one = canon_poly(one)
        two = canon_poly(two)

    return hash_poly(one) == hash_poly(two)

def canon_order(polys):
    return list(sorted(polys, key=hash_poly))

def hash_polys(polys):
    return hash(tuple(map(hash_poly, polys)))

def polys_equal(one, two, canon_polys=None, canon_poly=None):
    if canon_poly is not None:
        one = tuple(map(canon_poly, one))
        two = tuple(map(canon_poly, two))

    if canon_polys is not None:
        one = canon_polys(one)
        two = canon_polys(two)

    return hash_polys(one) == hash_polys(two)
    #if not check_poly_order:
    #    counter_one = defaultdict(int)
    #    counter_two = defaultdict(int)

    #    for poly in one:
    #        poly = canon(poly, check_rotation, check_orientation)
    #        counter_one[hash_poly(poly)] += 1

    #    for poly in two:
    #        poly = canon(poly, check_rotation, check_orientation)
    #        counter_two[hash_poly(poly)] += 1

    #    return counter_one == counter_two

    #thiscanon = partial(canon, check_rotation=check_rotation, check_orientation=check_orientation)
    #return tuple(map(thiscanon, one)) == tuple(map(thiscanon, two))

    #return rai.is_rotated(
    #    one,
    #    two,
    #    partial(
    #        poly_equal,
    #        check_rotation=check_rotation,
    #        check_orientation=check_orientation,
    #        )
    #    )

