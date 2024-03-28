import ast

import pycif as pc

def write_parents(tree):
    """
    Walk a tree and add a `parent` attribute to every node
    (that points to the direct parent)
    and an `ancestors` attribute that is a list of ancestors
    from closest to latest.
    """
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):

            child.ancestors = []
            ancestor = child
            while 1:
                try:
                    ancestor = ancestor.parent
                except AttributeError:
                    break

                child.ancestors.append(ancestor)

#def __matches(match, case):
#    if match == case:
#        return True
#
#    if not hasattr(case, '__match_args__'):
#        return False
#
#    if not isinstance(match, type(case)):
#        return False
#
#    for arg in case.__match_args__:
#        try:
#            attr_match = getattr(match, arg)
#            attr_case = getattr(case, arg)
#        except AttributeError:
#            continue
#
#        if not __matches(attr_match, attr_case):
#            return False
#
#    return True

# The name won't actually get scrambled since it's not in a class,
# but this gets the point across that you really shouldn't use this
# outside of this module.
def __matches(match, case):
    locs = {'match': match}
    exec(
        "match match:\n"
        f"   case {case}:\n"
        "       did_match = True",
        globals(),
        locs,
        )
    return 'did_match' in locs.keys()

def __find(tree, node, multiple=False):
    found = []
    for child in ast.iter_child_nodes(tree):
        if __matches(child, node):
            if multiple:
                found.append(child)
            else:
                return child
    if multiple and found:
        return found

    raise Exception  # TODO

def __find_recursive(tree, node, multiple=False):
    found = []
    for child in ast.walk(tree):
        if __matches(child, node):
            if multiple:
                found.append(child)
            else:
                return child
    if multiple and found:
        return found
    raise Exception  # TODO

def _check_compo(compo, tree):
    """
    """
    make_func = __find(tree, """ast.FunctionDef(
        name='_make'
        )""")

    mark_assigns = __find_recursive(tree, """ast.Attribute(
        value=ast.Attribute(
            value=ast.Name(id='self'),
            attr='marks',
            ),
        )""", True)

    for assign in mark_assigns:
        if assign.attr not in compo.Marks:
            yield pc.RAI442(assign.lineno, mark=assign.attr)


def check_compo(compo, root):
    tree = __find(root, """ast.ClassDef()""")
    write_parents(tree)
    yield from _check_compo(compo, tree)

