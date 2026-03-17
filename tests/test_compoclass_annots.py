"""
Test compo class Marks, Layers, Options annotations

It seems that RAIMAD's monkey patch approach to these annotation
classes cannot be feasibly reconciled with mypy.
Any access to .Marks, .Layer, and .Options unfortunately requires a
type: ignore
"""

import unittest
from typing import Protocol, cast

import raimad as rai

#class CompoProto(Protocol):
#    Marks: rai.DictList[rai.Mark]
#    Layers: rai.DictList[rai.Layer]
#    Options: rai.DictList[rai.Option]


#class xMarks:
#    def __class_getitem__(cls, idx: str | int) -> rai.Mark:
#        assert False
#        return rai.Mark()
#
#class xLayers:
#    def __class_getitem__(cls, idx: str | int) -> rai.Layer:
#        assert False
#        return rai.Layer()
#
#class xOptions:
#    def __class_getitem__(cls, idx: str | int) -> rai.Option:
#        assert False
#        return rai.Option()
#
# TODO fixme!!

class Annotated(rai.Compo):
    #class Marks(xMarks):
    class Marks:
        square_corner = rai.Mark('corner of the square')
        square_center = rai.Mark('center of the square')

    #class Layers(xLayers):
    class Layers:
        al = rai.Layer('Aluminium')
        insl = rai.Layer('Insulator')
        gnd = rai.Layer('Ground')

    #class Options(xOptions):
    class Options:
        width = rai.Option.Geometric('width of coupler')
        freq = rai.Option.Functional('resonant frequency')
        grav = rai.Option.Environmental('Gravitational constant')
        skip_beams = rai.Option.Debug('Do not generate beams')
        print_beams = rai.Option('Print a line for every beam')

    def _make(
            self,
            width: float,
            freq: float = 3e9,
            grav: float = 6.67430e-11,
            skip_beams: bool = True,
            print_beams: bool = False,
            ) -> None:
        pass

#Annotated = cast(CompoProto, Annotated)

class TestClassAnnots(unittest.TestCase):

    def test_class_annots_marks(self):
        #reveal_type(Annotated.Marks)
        #Annotated.Marks = cast(rai.DictList[rai.Mark], Annotated.Marks)
        #reveal_type(Annotated.Marks)

        self.assertEqual(
            #Annotated.Marks.__class_getitem__(0).name,
            Annotated.Marks[0].desc,  # type: ignore
            'square_corner'
            )

        self.assertEqual(
            Annotated.Marks[1].desc,  # type: ignore
            'center of the square'
            )

        self.assertEqual(
            Annotated.Marks['square_corner'].name,  # type: ignore
            'square_corner'
            )

        self.assertEqual(
            Annotated.Marks['square_center'].desc,  # type: ignore
            'center of the square'
            )

    def test_class_annots_layers(self):

        self.assertEqual(
            Annotated.Layers[2].name,  # type: ignore
            'gnd'
            )

        self.assertEqual(
            Annotated.Layers[2].desc,  # type: ignore
            'Ground'
            )

    def test_class_annots_options(self):

        self.assertEqual(
            Annotated.Options[3].name,  # type: ignore
            'skip_beams'
            )

        self.assertEqual(
            Annotated.Options[4].desc,  # type: ignore
            'Print a line for every beam'
            )

        self.assertTrue(
            Annotated.Options[3].category  # type: ignore
            is
            rai.Option.Debug
            )

        self.assertTrue(
            Annotated.Options[4].category  # type: ignore
            is
            rai.Option
            )

    def test_class_annots_options_shorthands(self):

        self.assertTrue(Annotated.Options[3].default is True)  # type: ignore
        self.assertTrue(Annotated.Options[4].default is False)  # type: ignore

        # Type specified explicitly with an annotation
        self.assertEqual(Annotated.Options[3].annot, bool)  # type: ignore
        # Type guessed from type of default
        self.assertEqual(Annotated.Options[4].annot, bool)  # type: ignore
        self.assertEqual(Annotated.Options[1].annot, float)  # type: ignore
        # No type specified annotated, and no default value
        self.assertEqual(Annotated.Options[0].annot, rai.Empty)  # type: ignore


if __name__ == '__main__':
    unittest.main()

