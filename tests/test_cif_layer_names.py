import unittest

import raimad as rai
import cift as cf

from .utils import GeomsEqual, ArrayAlmostEqual

class TestLayerNames(GeomsEqual, ArrayAlmostEqual, unittest.TestCase):
    """
    Ensure that layer names are CIF-compatible.
    """
    def test_builtin_compos_layer_names(self):
        """
        Test that all builtin compos have CIF-compatible layer names.

        Builtin compos are extracted automatically, instantiated,
        and the `geoms` dict is tested.
        `Layers` annotation class is tested.
        Layer names in exported CIF file is NOT tested here.
        """
        builtin_compos = [
            compo for name, compo in rai.__dict__.items()
            if 
                not name.startswith('_')
                and isinstance(compo, type)
                and issubclass(compo, rai.Compo)
                and compo is not rai.Compo
            ]

        self.assertTrue(len(builtin_compos) > 2)

        for compo in builtin_compos:

            # This incantation instantiates a compo with its
            # browser_default options.
            # TODO would be nice to break it out into a separate helper.

            instance = compo(**{
                option.name: option.browser_default
                for option in compo.Options.values()
                if option.browser_default is not rai.Empty
                })

            exporter = rai.cif.NoReuse(
                instance,
                multiplier=1,
                )

            layers = cf.parse(
                exporter.cif_string,
                grammar=cf.grammar.strict
                )

            layers = tuple(layers.keys())
            self.assertTrue(len(layers) > 0)

            for layer_name in layers:
                print(layer_name)
                self.assertTrue(rai.is_lname_valid(layer_name))
                self.assertTrue(layer_name != 'L')

            #layers = tuple(instance.steamroll().keys())
            #self.assertTrue(len(layers) > 0)

            #for layer_name in layers:
            #    print(layer_name)
            #    self.assertTrue(rai.is_lname_valid(layer_name))

    def test_warn_layer_names(self):
        """
        Test emmission of warning for cif-incompatible layer names.
        """

    def test_cif_layername_helper(self):
        """
        Test rai.is_lname_valid
        """

        # Valid names

        self.assertTrue(rai.is_lname_valid('ROOT'))
        self.assertTrue(rai.is_lname_valid('FOOO'))
        self.assertTrue(rai.is_lname_valid('FOO'))
        self.assertTrue(rai.is_lname_valid('FO'))
        self.assertTrue(rai.is_lname_valid('F'))
        self.assertTrue(rai.is_lname_valid('0'))
        self.assertTrue(rai.is_lname_valid('00'))
        self.assertTrue(rai.is_lname_valid('000'))
        self.assertTrue(rai.is_lname_valid('0000'))
        self.assertTrue(rai.is_lname_valid('A000'))
        self.assertTrue(rai.is_lname_valid('A00Z'))
        self.assertTrue(rai.is_lname_valid('Z00A'))
        self.assertTrue(rai.is_lname_valid('Z0'))
        self.assertTrue(rai.is_lname_valid('1'))

        # These are given as the starting set of layer names
        # in the 1980 spec

        self.assertTrue(rai.is_lname_valid('ND'))
        self.assertTrue(rai.is_lname_valid('NP'))
        self.assertTrue(rai.is_lname_valid('NC'))
        self.assertTrue(rai.is_lname_valid('NM'))
        self.assertTrue(rai.is_lname_valid('NI'))
        self.assertTrue(rai.is_lname_valid('NB'))
        self.assertTrue(rai.is_lname_valid('NG'))

        # Invalid names

        self.assertFalse(rai.is_lname_valid('ZZZZ'))
        self.assertFalse(rai.is_lname_valid('ZZZz'))
        self.assertFalse(rai.is_lname_valid('root'))
        self.assertFalse(rai.is_lname_valid('Lroot'))
        self.assertFalse(rai.is_lname_valid('FOOOO'))
        self.assertFalse(rai.is_lname_valid('99999'))
        self.assertFalse(rai.is_lname_valid('F9999'))
        self.assertFalse(rai.is_lname_valid(''))
        self.assertFalse(rai.is_lname_valid('----'))
        self.assertFalse(rai.is_lname_valid('aaaa'))
        self.assertFalse(rai.is_lname_valid('abcd'))
        self.assertFalse(rai.is_lname_valid('0aaa'))
        self.assertFalse(rai.is_lname_valid('    '))
        self.assertFalse(rai.is_lname_valid(' '))
        self.assertFalse(rai.is_lname_valid('\n'))
        self.assertFalse(rai.is_lname_valid('\t'))
        self.assertFalse(rai.is_lname_valid('\r'))
        self.assertFalse(rai.is_lname_valid('\x00'))
        self.assertFalse(rai.is_lname_valid('\x00\x00\x00\x00'))
        self.assertFalse(rai.is_lname_valid('今朝毎朝'))

