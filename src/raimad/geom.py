from functools import partial
from collections import defaultdict
import raimad as rai

#def hash_poly(poly, mind_rotation, mind_orientation):
#    pass

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

def canon(poly, check_rotation, check_orientation):
    if check_rotation and check_orientation:
        return poly
    elif check_rotation and not check_orientation:
        return canon_or(poly)
    elif not check_rotation and check_orientation:
        return canon_rot(poly)
    elif not check_rotation and not check_orientation:
        return canon_rot_or(poly)
    assert False


def poly_equal(one, two, check_rotation, check_orientation):
    one = canon(one, check_rotation, check_orientation)
    two = canon(two, check_rotation, check_orientation)
    #one, two = map(
    #    (
    #        canon_rot_or,
    #        canon_rot,
    #        canon_or,
    #        lambda x: x,
    #        )[check_rotation << 1 | check_orientation],
    #    (one, two)
    #    )

    return one == two

    #if check_rotation and check_orientation:
    #    return one == two
    #elif not check_rotation and check_orientation:
    #    return rai.is_rotated(one, two)
    #elif check_rotation and not check_orientation:
    #    return (
    #        one == rai.reversed_pin(two)
    #        or one == two
    #        )
    #elif not check_rotation and not check_orientation:
    #    return (
    #        rai.is_rotated(one, two)
    #        or rai.is_rotated(one, rai.reversed(two))
    #        )
    #assert False


def polys_equal(one, two, check_poly_order, check_rotation, check_orientation):
    if not check_poly_order:
        counter_one = defaultdict(int)
        counter_two = defaultdict(int)

        for poly in one:
            poly = canon(poly, check_rotation, check_orientation)
            counter_one[hash_poly(poly)] += 1

        for poly in two:
            poly = canon(poly, check_rotation, check_orientation)
            counter_two[hash_poly(poly)] += 1

        return counter_one == counter_two

    thiscanon = partial(canon, check_rotation=check_rotation, check_orientation=check_orientation)
    return tuple(map(thiscanon, one)) == tuple(map(thiscanon, two))

    #return rai.is_rotated(
    #    one,
    #    two,
    #    partial(
    #        poly_equal,
    #        check_rotation=check_rotation,
    #        check_orientation=check_orientation,
    #        )
    #    )

