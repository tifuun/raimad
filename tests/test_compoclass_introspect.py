import unittest

import raimad as rai

class Annotated(rai.Compo):
    class Marks:
        square_corner = rai.Mark('corner of the square')
        square_center = rai.Mark('center of the square')

    class Layers:
        al = rai.Layer('Aluminium')
        insl = rai.Layer('Insulator')
        gnd = rai.Layer('Ground')

    class Options:
        width = rai.Option.Geometric('width of coupler')
        freq = rai.Option.Functional('resonant frequency')
        grav = rai.Option.Environmental('Gravitational constant')
        skip_beams = rai.Option.Debug('Do not generate beams')
        print_beams = rai.Option('Print a line for every beam')

    def _make(
            width,
            freq=3e9,
            grav: float = 6.67430e-11,
            skip_beams: bool = True,
            print_beams=False,
            ):
        pass


class TestClassIntrospection(unittest.TestCase):

    def test_class_introspection_marks(self):

        self.assertEqual(
            Annotated.Marks[0].name,
            'square_corner'
            )

        self.assertEqual(
            Annotated.Marks[1].desc,
            'center of the square'
            )

        self.assertEqual(
            Annotated.Marks['square_corner'].name,
            'square_corner'
            )

        self.assertEqual(
            Annotated.Marks['square_center'].desc,
            'center of the square'
            )

    def test_class_introspection_layers(self):

        self.assertEqual(
            Annotated.Layers[2].name,
            'gnd'
            )

        self.assertEqual(
            Annotated.Layers[2].desc,
            'Ground'
            )

    def test_class_introspection_options(self):

        self.assertEqual(
            Annotated.Options[3].name,
            'skip_beams'
            )

        self.assertEqual(
            Annotated.Options[4].desc,
            'Print a line for every beam'
            )

        self.assertTrue(
            Annotated.Options[3].category
            is
            rai.Option.Debug
            )

        self.assertTrue(
            Annotated.Options[4].category
            is
            rai.Option
            )

    def test_class_introspection_options_shorthands(self):

        self.assertTrue(Annotated.Options[3].default is True)
        self.assertTrue(Annotated.Options[4].default is False)

        # Type specified explicitly with an annotation
        self.assertEqual(Annotated.Options[3].annot, bool)
        # Type guessed from type of default
        self.assertEqual(Annotated.Options[4].annot, bool)
        self.assertEqual(Annotated.Options[1].annot, float)
        # No type specified annotated, and no default value
        self.assertEqual(Annotated.Options[0].annot, rai.Empty)


if __name__ == '__main__':
    unittest.main()

