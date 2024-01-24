"""
Helpers for understanding what's going on inside compos
"""

def print_compo(compo, depth=0):
    print(
        '    ' * depth,
        compo,
        )

def print_poly(poly, depth=0):
    print(
        '    ' * depth,
        poly,
        )

def print_compo_tree(compo, depth=0):
    """
    Print hierarchy of a compo, down to the polys
    """

    print_compo(compo, depth=depth)

    for subcompo in compo.subcompos:
        print_compo_tree(subcompo.compo, depth=depth + 1)

    for subpoly in compo.subpolys:
        print_poly(subpoly.poly, depth=depth + 1)


