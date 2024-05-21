import unittest

import raimad as rai

class Unannotated(rai.Compo):
    class Marks:
        square_corner = rai.Mark('corner of the square')

    def _make(self):
        self.marks.triangle_corner = (20, 40)
        self.marks.square_center = (5, 5)
        self.marks.square_corner = (10, 10)

class Annotated(rai.Compo):
    class Marks:
        square_corner = rai.Mark('corner of the square')
        square_center = rai.Mark('corner of the square')
        triangle_corner = rai.Mark('corner of the square')

    def _make(self):
        self.marks.triangle_corner = (20, 40)
        self.marks.square_center = (5, 5)
        self.marks.square_corner = (10, 10)

class Reassign(rai.Compo):
    class Marks:
        square_corner = rai.Mark('corner of the square')

    def _make(self):
        self.marks.square_corner = (5, 5)
        self.marks.square_center = (1, 1)
        print('useless statement')
        self.marks.square_corner = (6, 6)

def same_viols(actual, expected):
    while len(actual) and len(expected):
        for i, (line, viol_class) in enumerate(expected):
            matched = False
            for j, viol in enumerate(actual):
                if isinstance(viol, viol_class) and viol.line == line:
                    del expected[i]
                    del actual[j]
                    matched = True
                    break
            if matched:
                break
        if not matched:
            return False
    if len(actual) or len(expected):
        return False
    return True


class TestCheckMarkNames(unittest.TestCase):

    def test_lint_annotated(self):
        viols = list(rai.check_compo(Annotated))
        self.assertEqual(len(viols), 0)

    def test_lint_unannotated(self):
        viols = list(rai.check_compo(Unannotated))
        self.assertTrue(same_viols(viols, [
            (6, rai.RAI442),
            (7, rai.RAI442),
            ]))

#    def test_lint_reassign(self):
#        viols = list(rai.check_compo(Reassign))
#        self.assertTrue(same_viols(viols, [
#            (6, rai.RAI412),
#            (7, rai.RAI442),
#            (9, rai.RAI412),
#            ]))


if __name__ == '__main__':
    unittest.main()

