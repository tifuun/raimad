import raimad as rai

def poly_equal(one, two, check_rotation, check_orientation):
    if check_rotation and check_orientation:
        return one == two
    elif check_rotation and not check_orientation:
        return rai.is_rotated(one, two)
    elif not check_rotation and check_orientation:
        return one == rai.reversed_keep_0(two)
    elif not check_rotation and not check_orientation:
        return (
            rai.is_rotated(one, two)
            or rai.is_rotated(one, rai.reversed(two))
            )
    assert False

