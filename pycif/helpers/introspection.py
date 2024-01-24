"""
Helpers for understanding what's going on inside compos
"""

def print_compo(compo, depth=0):
    print(
        '    ' * depth,
        compo,
        )

def print_polygon(poly, depth=0):
    print(
        '    ' * depth,
        poly,
        )

def print_compo_tree(compo, depth=0):
    """
    Print hierarchy of a compo, down to the polygons
    """

    print_compo(compo, depth=depth)

    for subcompo in compo.subcompos:
        print_compo_tree(subcompo.compo, depth=depth + 1)

    for subpoly in compo.subpolygons:
        print_polygon(subpoly.polygon, depth=depth + 1)


