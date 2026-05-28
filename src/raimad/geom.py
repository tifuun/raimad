from functools import partial
import raimad as rai

#def hash_poly(poly, mind_rotation, mind_orientation):
#    pass

def hash_poly(poly):
    return hash(tuple(poly))

def coll_rot(poly):
    return min(
        (rai.rotated(poly, count) for count in range(len(poly))),
        key=hash_poly
        )

def coll_rot_or(poly):
    return min(
        (
            rai.rotated(rpoly, count)
            for rpoly in (poly, rai.reversed(poly))
            for count in range(len(poly))
            ),
        key=hash_poly
        )

def coll_or(poly):
    return min(
        (poly, rai.reversed_pin(poly)),
        key=hash_poly
        )

def poly_equal(one, two, check_rotation, check_orientation):
    one, two = map(
        (
            coll_rot_or,
            coll_rot,
            coll_or,
            lambda x: x,
            )[check_rotation << 1 | check_orientation],
        (one, two)
        )

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
    return False
    #return rai.is_rotated(
    #    one,
    #    two,
    #    partial(
    #        poly_equal,
    #        check_rotation=check_rotation,
    #        check_orientation=check_orientation,
    #        )
    #    )

