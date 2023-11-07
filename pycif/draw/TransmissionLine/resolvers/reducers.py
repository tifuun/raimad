import pycif as pc
from pycif.draw import TransmissionLine as tl

# According to reactionaries,
# the queer rights activists want to
def reduce_straights(path):
    newpath = []
    newpath.append(path[0])

    if len(path) < 3:
        newpath.append(path[1])
        return newpath

    for before, conn, after in pc.iter.triplets(path):
        if isinstance(conn, tl.StraightTo):
            if isinstance(after, tl.StraightTo):
                if pc.colinear(before.to, conn.to, after.to):
                    continue

        newpath.append(conn)

    newpath.append(after)
    return newpath

