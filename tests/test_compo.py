import unittest
import re

import raimad as rai

class BareGeometric(rai.Compo):
    def _make(self):
        self.geoms.update({
            'root': [
                [
                    [0, 0],
                    [0, 10],
                    [10, 10],
                    [10, 0],
                    ],
                [
                    [20, 20],
                    [40, 20],
                    [30, 40],
                    ],
                ]
            })

class BareStructural(rai.Compo):
    def _make(self):
        self.subcompos.append(
            rai.Proxy(
                BareGeometric(),
                {'root': 'upper'},
                )
            )
        self.subcompos.append(
            rai.Proxy(
                BareGeometric(),
                {'root': 'lower'},
                )
            )

class TestCompo(unittest.TestCase):

    def test_bare_geometric(self):
        compo = BareGeometric()
        geom = compo.steamroll()

        # Test one root layer
        self.assertEqual(geom.keys(), {'root'})

        # Test two polys on the layer
        self.assertEqual(len(geom['root']), 2)

    def test_bare_geometric_copied(self):
        compo = BareGeometric()
        self.assertIsNot(compo.geoms, compo.steamroll())

    def test_bare_structural(self):
        compo = BareStructural()
        geom = compo.steamroll()

        # Test one root layer
        self.assertEqual(geom.keys(), {'upper', 'lower'})

        # Test two polys on the top lyaer
        self.assertEqual(len(geom['upper']), 2)

        # Test two polys on the top lyaer
        self.assertEqual(len(geom['lower']), 2)

    def test_add_invalid_subcompo(self):
        """
        Test that adding anything other than a Proxy
        as a subcomponent raises an error
        """
        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.invalid = 'invalid'

        with self.assertRaises(rai.err.InvalidSubcompoError):
            MyCompo()

    def test_add_invalid_compo_as_subcompo(self):
        """
        Test that adding a Compo as a subcompo
        (instead of a Proxy) raises an error
        """
        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.invalid = rai.Snowman()

        with self.assertRaises(rai.err.CompoInsteadOfProxyAsSubcompoError):
            MyCompo()

        # This tests the inheritance relationship between the two error types
        with self.assertRaises(rai.err.InvalidSubcompoError):
            MyCompo()

    def test_fail_transform_compo(self):
        """
        Test that trying to use transformation methods on a compo
        (move, scale, etc)
        raises an error telling you to transform a Proxy of it instead
        """
        compo = rai.Snowman()

        with self.assertRaises(rai.err.TransformCompoError):
            compo.move(10, 10)

        with self.assertRaises(rai.err.TransformCompoError):
            compo.movex(10)

        with self.assertRaises(rai.err.TransformCompoError):
            compo.movey(10)

        with self.assertRaises(rai.err.TransformCompoError):
            compo.scale(10, 10)

        with self.assertRaises(rai.err.TransformCompoError):
            compo.rotate(10)

        with self.assertRaises(rai.err.TransformCompoError):
            compo.hflip()

        with self.assertRaises(rai.err.TransformCompoError):
            compo.vflip()

        with self.assertRaises(rai.err.TransformCompoError):
            compo.flip()

    def test_compo_str(self):

        compo = rai.Circle(10)

        self.assertTrue(
            re.match(
                r'<Circle at .*>',
                str(compo)
                )
            )
        self.assertEqual(str(compo), repr(compo))

    #def test_fail_copy_compo(self):
    #    """
    #    Test that trying to copy a compo
    #    raises an error telling you to copy a Proxy of it instead
    #    """
    #    compo = rai.Snowman()

    #    with self.assertRaises(rai.err.CopyCompoError):
    #        compo.copy()

    #    # Test the inheritance relationship between the error types
    #    with self.assertRaises(rai.err.ProxyCompoConfusionError):
    #        compo.copy()


if __name__ == '__main__':
    unittest.main()

