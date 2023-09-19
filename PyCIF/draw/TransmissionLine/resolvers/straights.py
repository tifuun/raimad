import PyCIF as pc
from PyCIF.draw import TransmissionLine as tl

def make_straight_components(path, Compo: pc.typing.ComponentClass):
    straights = []
    for conn, after in pc.iter.duplets(path):
        if not isinstance(after, tl.StraightTo):
            continue

        straights.append(
            Compo(opts=dict(
                length=pc.distance_between(conn.to, after.to),
                ))
                .marks.tl_enter.to(conn.to)
                .marks.tl_enter.rotate(
                    pc.angle_between(conn.to, after.to),
                    ),
            )
    return straights

