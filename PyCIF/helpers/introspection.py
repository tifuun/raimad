"""
Helpers for understanding what's going on inside components
"""

def print_component(compo, depth=0):
    print(
        '    ' * depth,
        compo,
        compo.transform.translate_x,
        compo.transform.translate_y,
        )

def print_polygon(poly, depth=0):
    print(
        '    ' * depth,
        poly,
        poly.transform.translate_x,
        poly.transform.translate_y,
        )

def print_component_tree(compo, depth=0):
    """
    Print hierarchy of a component, down to the polygons
    """

    print_component(compo, depth=depth)

    for subcompo in compo.subcomponents:
        print_component_tree(subcompo.component, depth=depth + 1)

    for subpoly in compo.subpolygons:
        print_polygon(subpoly.polygon, depth=depth + 1)


