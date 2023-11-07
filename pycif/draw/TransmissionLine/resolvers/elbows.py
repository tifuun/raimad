import pycif as pc
from pycif.draw import TransmissionLine as tl

def resolve_elbows(path):
    newpath = path[0:1]
    for before_conn, conn in pc.iter.duplets(path):
        if isinstance(conn, tl.ElbowTo):
            newpath.extend(
                resolve_elbow(
                    before_conn.to,
                    conn,
                    ),
                )
        else:
            newpath.append(conn)

    return newpath

def resolve_elbow(_from: pc.typing.Point, elbow: tl.ElbowTo):
    """
    Convert single tl.ElbowTo into three instances of tl.StraightTo
    Expects POINTS!
    """
    if _from[0] == elbow.to[0] or _from[1] == elbow.to[1]:
        return [
            tl.StraightTo(elbow.to),
            ]

    mid = pc.midpoint(_from, elbow.to)
    p1 = pc.Point(mid[0], _from[1])
    p2 = pc.Point(mid[0], elbow.to[1])
    return [
        tl.StraightTo(p1, clone_from=elbow),
        tl.StraightTo(p2, clone_from=elbow),
        tl.StraightTo(elbow.to, clone_from=elbow),
        ]

