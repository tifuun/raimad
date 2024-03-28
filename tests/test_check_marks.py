import unittest
import ast

import pycif as pc

code = """\
class Unannotated(pc.Compo):
    class Marks:
        square_corner = pc.Mark['corner of the square']

    def _make(self):
        self.marks.triangle_corner = (20, 40)
        self.marks.square_center = (5, 5)
        self.marks.square_corner = (10, 10)
"""

def all_isinstance(actual, expected):
    return all(isinstance(a, e) for e, a in zip(expected, actual))

class TestLintMarkNames(unittest.TestCase):

    def test_lint_mark_names(self):
        locs = {}
        exec(code, globals(), locs)
        Compo = locs['Unannotated']
        viols = list(pc.check_compo(Compo, ast.parse(code)))
        self.assertTrue(all_isinstance(viols, [pc.RAI442, pc.RAI442]))


if __name__ == '__main__':
    unittest.main()

