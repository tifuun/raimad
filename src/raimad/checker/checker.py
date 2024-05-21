import ast
import inspect

import raimad as rai

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
    exec(
        "match match:\n"
        f"   case {case}:\n"
        "       did_match = True",
        globals(),
        locs := {'match': match}
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

    redundancy = {}
    for assign in mark_assigns:
        mark_name = assign.attr

        if mark_name not in [mark.name for mark in compo.Marks.values()]:
            yield rai.RAI442(assign, mark=mark_name)

        if mark_name not in redundancy.keys():
            redundancy[mark_name] = []
        redundancy[mark_name].append(assign)

    # TODO how to deal with multiple asignment
    # that's not actually multiple asignment
    # because it's in a mutually exclusive `if`?
    #for mark_name, nodes in redundancy.items():
    #    if len(nodes) > 1:
    #        for node in nodes:
    #            yield rai.RAI412(node, mark=mark_name, lines=[
    #                node.lineno for node in nodes
    #                ])


def check_compo(compo):
    code = inspect.getsource(compo)
    root = ast.parse(code)
    tree = __find(root, """ast.ClassDef()""")
    write_parents(tree)
    yield from _check_compo(compo, tree)

def check_module(tree):
    compiled = compile(tree, '<string>', 'exec')
    exec(
        compiled,
        globals(),  # TODO is this correct?
        locs := {}
        )

    for compo_node in __find(tree, "ast.ClassDef()", True):
        compo = locs.get(compo_node.name, None)
        if compo is None:
            continue
        if not isinstance(compo, type):
            continue
        if not issubclass(compo, rai.Compo):
            continue
        yield from _check_compo(compo, compo_node)

class Flake8Checker:
    name = __name__
    version = 0

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self):
        if not hasattr(self._tree, 'body'):
            return
        for toplevel in self._tree.body:
            match toplevel:
                case ast.Expr(value=ast.Constant(value='pc_checkme')):
                    break
        else:
            return

        for viol in check_module(self._tree):
            yield viol.line, viol.col, viol.flake8(), type


