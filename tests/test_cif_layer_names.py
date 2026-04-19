import unittest

import os
import tempfile
from pathlib import Path
import subprocess
import shlex
import sys
import raimad as rai
import cift as cf

from .utils import AssertDoesntWarn

def autoinit(compo_class):
    # This incantation instantiates a compo with its
    # browser_default options.
    # TODO would be nice to break it out into a separate helper.

    instance = compo_class(**{
        option.name: option.browser_default
        for option in compo_class.Options.values()
        if option.browser_default is not rai.Empty
        })

    return instance

def get_cif_layers(
        instance,
        grammar=cf.grammar.strict,
        exporter_args=None
        ):

    exporter = rai.cif.NoReuse(
            instance,
            multiplier=1,
            **(exporter_args or {})
            )

    layers = cf.parse(
        exporter.cif_string,
        grammar=grammar
        )

    layers = set(layers.keys())

    return layers

class TestLayerNames(AssertDoesntWarn, unittest.TestCase):
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

        #builtin_compos = [rai.RectLW]

        for compo in builtin_compos:

            with self.assertDoesntWarn():
                layers = get_cif_layers(autoinit(compo))

            self.assertTrue(len(layers) > 0)

            for layer_name in layers:
                self.assertTrue(rai.is_lname_valid(layer_name))
                self.assertTrue(layer_name != 'L')

            #layers = tuple(instance.steamroll().keys())
            #self.assertTrue(len(layers) > 0)

            #for layer_name in layers:
            #    print(layer_name)
            #    self.assertTrue(rai.is_lname_valid(layer_name))

    def test_error_untransformable_lname(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = (
                rai.cif.lname_transformers.root,
                rai.cif.lname_transformers.noop,
                )

            def _make(self):
                self.geoms.update({'foo': [[(0, 0), (0, 1), (1, 1)]]})

        with self.assertRaises(rai.err.UntransformableLayerName):
            rai.export_cif(Foo())

        with self.assertRaises(rai.err.UntransformableLayerName):
            rai.export_cif(Foo().proxy())

    def test_custom_transformer(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = (
                {
                    'baz': 'BAZ',
                    },
                {
                    'foo': 'FOO',
                    },
                lambda name: 'BAR' if name == 'bar' else None,
                rai.cif.lname_transformers.root,
                rai.cif.lname_transformers.noop,
                )

            def _make(self):
                self.geoms.update({
                    'foo': [[(0, 0), (0, 1), (1, 1)]],
                    'bar': [[(0, 0), (0, 1), (1, 1)]],
                    'baz': [[(0, 0), (0, 1), (1, 1)]],
                    'root': [[(0, 0), (0, 1), (1, 1)]],  # caught by root
                    'HAHA': [[(0, 0), (0, 1), (1, 1)]],  # caught by noop
                    })

        layers = get_cif_layers(Foo(), cf.grammar.lenient_layers)
        self.assertEqual(layers, {'FOO', 'BAR', 'BAZ', 'ROOT', 'HAHA'})

    def test_invalid_transformer(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = [{
                'foo': 'invalid lol'
                }]

            def _make(self):
                self.geoms.update({'foo': [[(0, 0), (0, 1), (1, 1)]]})

        with self.assertWarns(rai.err.InvalidLayerNameTransformerOutput):
            rai.export_cif(Foo())

        with self.assertWarns(rai.err.InvalidLayerNameTransformerOutput):
            rai.export_cif(Foo().proxy())

    ### test klayout ###

    def test_transformer_klayout(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = [
                rai.cif.lname_transformers.klayout,
                ]

            def _make(self):
                self.geoms.update({
                    'foo': [[(0, 0), (0, 1), (1, 1)]],
                    'root': [[(0, 0), (0, 1), (1, 1)]],
                    'foo_BAR': [[(0, 0), (0, 1), (1, 1)]],
                    })

        with self.assertWarns(rai.err.InvalidLayerNameTransformerOutput):
            layers = get_cif_layers(Foo(), cf.grammar.lenient_layers)
        self.assertEqual(layers, {'Lfoo', 'Lroot', 'Lfoo_BAR'})

        #rai.export_cif(Foo(), 'Foo.cif')

    ### test root ###

    def test_transformer_root(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = [
                rai.cif.lname_transformers.root,
                ]

            def _make(self):
                self.geoms.update({'root': [[(0, 0), (0, 1), (1, 1)]]})

        layers = get_cif_layers(Foo(), cf.grammar.lenient_layers)
        self.assertEqual(layers, {'ROOT'})

    def test_transformer_root_neg(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = [
                rai.cif.lname_transformers.root,
                ]

            def _make(self):
                self.geoms.update({'rooooot': [[(0, 0), (0, 1), (1, 1)]]})

        with self.assertRaises(rai.err.UntransformableLayerName):
            rai.export_cif(Foo())

        with self.assertRaises(rai.err.UntransformableLayerName):
            rai.export_cif(Foo().proxy())

    ### test noop ###

    def test_transformer_noop(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = [
                rai.cif.lname_transformers.noop,
                ]

            def _make(self):
                self.geoms.update({
                    'NOOP': [[(0, 0), (0, 1), (1, 1)]],
                    'A234': [[(0, 0), (0, 1), (1, 1)]],
                    'A00A': [[(0, 0), (0, 1), (1, 1)]],
                    })

        layers = get_cif_layers(Foo(), cf.grammar.lenient_layers)
        self.assertEqual(layers, {'NOOP', 'A234', 'A00A'})

    def test_transformer_noop_neg(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = [
                rai.cif.lname_transformers.noop,
                ]

            def _make(self):
                self.geoms.update({
                    'NOOP': [[(0, 0), (0, 1), (1, 1)]],
                    'A2345': [[(0, 0), (0, 1), (1, 1)]],
                    'AA00': [[(0, 0), (0, 1), (1, 1)]],
                    })

        with self.assertRaises(rai.err.UntransformableLayerName):
            rai.export_cif(Foo())

        with self.assertRaises(rai.err.UntransformableLayerName):
            rai.export_cif(Foo().proxy())

    ### test capitalise ###

    def test_transformer_capitalise(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = [
                rai.cif.lname_transformers.capitalise,
                ]

            def _make(self):
                self.geoms.update({
                    'oooo': [[(0, 0), (0, 1), (1, 1)]],
                    'ab12': [[(0, 0), (0, 1), (1, 1)]],
                    'aBcD': [[(0, 0), (0, 1), (1, 1)]],
                    })

        layers = get_cif_layers(Foo(), cf.grammar.lenient_layers)
        self.assertEqual(layers, {'OOOO', 'AB12', 'ABCD'})

    def test_transformer_capitalise_neg(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = [
                rai.cif.lname_transformers.capitalise,
                ]

            def _make(self):
                self.geoms.update({'toolong': [[(0, 0), (0, 1), (1, 1)]]})

        with self.assertRaises(rai.err.UntransformableLayerName):
            rai.export_cif(Foo())

    ### test enumerator ###

    def test_transformer_enumerator(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = [
                rai.cif.lname_transformers.Enumerator(),
                ]

            def _make(self):
                self.geoms.update({
                    'oooo': [[(0, 0), (0, 1), (1, 1)]],
                    'ab12': [[(0, 0), (0, 1), (1, 1)]],
                    'aBcD': [[(0, 0), (0, 1), (1, 1)]],
                    })

        layers = get_cif_layers(Foo(), cf.grammar.lenient_layers)
        self.assertEqual(layers, {'0001', '0002', '0003'})

    def test_enumerator_state_not_persistent(self):
        class Foo(rai.Compo):

            _experimental_lname_transformers = lambda _: [
                rai.cif.lname_transformers.Enumerator(),
                ]

            def _make(self, alternative: bool = False):
                if alternative:
                    self.geoms.update({
                        'alt': [[(0, 0), (0, 1), (1, 1)]],
                        'alt2': [[(0, 0), (0, 1), (1, 1)]],
                        })
                else:
                    self.geoms.update({
                        'oooo': [[(0, 0), (0, 1), (1, 1)]],
                        'ab12': [[(0, 0), (0, 1), (1, 1)]],
                        'aBcD': [[(0, 0), (0, 1), (1, 1)]],
                        })

        foo1 = Foo(alternative=False)
        foo2 = Foo(alternative=True)

        layers1 = get_cif_layers(foo1, cf.grammar.lenient_layers)
        self.assertEqual(layers1, {'0001', '0002', '0003'})
        del layers1

        layers2 = get_cif_layers(foo2, cf.grammar.lenient_layers)
        self.assertEqual(layers2, {'0001', '0002'})
        del layers2

    def test_enumerator_state_persistent(self):
        my_persistent_enumerator = rai.cif.lname_transformers.Enumerator()

        class Foo(rai.Compo):

            _experimental_lname_transformers = [
                my_persistent_enumerator,
                ]

            def _make(self, alternative: bool = False):
                if alternative:
                    self.geoms.update({
                        'alt': [[(0, 0), (0, 1), (1, 1)]],
                        'alt2': [[(0, 0), (0, 1), (1, 1)]],
                        })
                else:
                    self.geoms.update({
                        'oooo': [[(0, 0), (0, 1), (1, 1)]],
                        'ab12': [[(0, 0), (0, 1), (1, 1)]],
                        'aBcD': [[(0, 0), (0, 1), (1, 1)]],
                        })

        foo1 = Foo(alternative=False)
        foo2 = Foo(alternative=True)

        layers1 = get_cif_layers(foo1, cf.grammar.lenient_layers)
        self.assertEqual(layers1, {'0001', '0002', '0003'})
        del layers1

        layers2 = get_cif_layers(foo2, cf.grammar.lenient_layers)
        self.assertEqual(layers2, {'0004', '0005'})
        del layers2


    def test_default_lname_transformers(self):
        class Foo(rai.Compo):
            def _make(self):
                self.geoms.update({
                    'root': [[(0, 0), (0, 1), (1, 1)]],  # caught by root
                    'VLID': [[(0, 0), (0, 1), (1, 1)]],  # caught by noop
                    'ab12': [[(0, 0), (0, 1), (1, 1)]],  # caught by capitalise
                    'invalid': [[(0, 0), (0, 1), (1, 1)]],
                    # ^ caught by enumerator
                    'otherone': [[(0, 0), (0, 1), (1, 1)]],
                    # ^ caught by enumerator
                    })

        with self.assertWarns(rai.err.CIFLayerNameWarning):
            layers = get_cif_layers(Foo(), cf.grammar.lenient_layers)
        self.assertEqual(layers, {'ROOT', 'VLID', 'AB12', '0001', '0002'})


    #def test_warn_layer_names(self):
    #    """
    #    Test emmission of warning for cif-incompatible layer names.
    #    """

    #    # Default behavior on undefined layer name:
    #    # use lname_to_klay and warn

    #    class Foo(rai.Compo):
    #        def _make(self):
    #            self.geoms.update({'foo': [[(0, 0), (0, 1), (1, 1)]]})
    #            self.geoms.update({'root': [[(0, 0), (0, 1), (1, 1)]]})

    #    with self.assertWarns(rai.err.CIFLayerNameWarning):
    #        layers = get_cif_layers(Foo, cf.grammar.lenient_layers)
    #    self.assertEqual(layers, {'ROOT', 'Lfoo'})

    #    # Set lname_policy to `fallback_klay_warn` to
    #    # manually specify this default behavior

    #    with self.assertWarns(rai.err.CIFLayerNameWarning):
    #        layers = get_cif_layers(
    #            Foo,
    #            cf.grammar.lenient_layers,
    #            exporter_args={'lname_policy': 'fallback-klay-warn'}
    #            )
    #    self.assertEqual(layers, {'ROOT', 'Lfoo'})

    #    # `fallback-klay` to use klayout-compatible name as fallback

    #    with self.assertDoesntWarn():
    #        layers = get_cif_layers(
    #            Foo,
    #            grammar=cf.grammar.lenient_layers,
    #            exporter_args={'lname_policy': 'fallback-klay'}
    #            )
    #    self.assertEqual(layers, {'ROOT', 'Lfoo'})

    #    # `force-klay` to use klayout-compatible name for all layers

    #    with self.assertDoesntWarn():
    #        layers = get_cif_layers(
    #            Foo,
    #            grammar=cf.grammar.lenient_layers,
    #            exporter_args={'lname_policy': 'force-klay'}
    #            )
    #    self.assertEqual(layers, {'Lroot', 'Lfoo'})

    #    # `strict` to emit error on any cif-incompatible layer name

    #    with self.assertRaises(rai.err.CIFLayerNameWarning):
    #        get_cif_layers(
    #            Foo,
    #            grammar=cf.grammar.lenient_layers,
    #            exporter_args={'lname_policy': 'strict'}
    #            )

    #    # Check that error is emitted on invalid lname_policy

    #    with self.assertRaises(ValueError):
    #        get_cif_layers(
    #            Foo,
    #            grammar=cf.grammar.lenient_layers,
    #            exporter_args={'lname_policy': 'this does not exist'}
    #            )
    #    
    #def test_cif_layer_name_composition(self):

    #    class Foo(rai.Compo):
    #        class Layers:
    #            foo = rai.Layer("Foo", cif_name="FOO")
    #        def _make(self):
    #            self.geoms.update({'foo': [[(0, 0), (0, 1), (1, 1)]]})

    #    self.assertEqual(get_cif_layers(Foo), {"FOO", })

    #    class Bar(rai.Compo):
    #        class Layers:
    #            bar = rai.Layer("Bar", cif_name="BAR")
    #        def _make(self):
    #            self.geoms.update({'bar': [[(0, 0), (0, 1), (1, 1)]]})

    #    self.assertEqual(get_cif_layers(Bar), {"BAR", })

    #    class Baz(rai.Compo):
    #        def _make(self):
    #            self.subcompos.append(Foo().proxy())
    #            self.subcompos.append(Bar().proxy())

    #    self.assertEqual(get_cif_layers(Baz), {"FOO", "BAR"})

    #    class Baq(rai.Compo):
    #        def _make(self):
    #            self.subcompos.append(Foo().proxy())
    #            self.subcompos.append(Bar().proxy())
    #            self.subcompos.append(Baz().proxy())

    #    self.assertEqual(get_cif_layers(Baq), {"FOO", "BAR"})

    #    # Overshadow subcompo's cif_name with new one
    #    class Ayy(rai.Compo):
    #        class Layers:
    #            bar = rai.Layer("Bar", cif_name="RAB")
    #        def _make(self):
    #            self.subcompos.append(Foo().proxy())
    #            self.subcompos.append(Bar().proxy())

    #    self.assertEqual(get_cif_layers(Ayy), {"FOO", "RAB"})

    #    # Overshadow overshadowed cif_name
    #    # BAR -> RAB -> BAZ
    #    class Lmao(rai.Compo):
    #        class Layers:
    #            bar = rai.Layer("Bar", cif_name="BAZ")
    #        def _make(self):
    #            self.subcompos.append(Ayy().proxy())

    #    self.assertEqual(get_cif_layers(Lmao), {"FOO", "BAZ"})

    #    # No overshadowing whatsoever in the toplevel compo
    #    # so should be exactly same as Lmao (subcompo)
    #    class Wrap(rai.Compo):
    #        def _make(self):
    #            self.subcompos.append(Lmao().proxy())

    #    self.assertEqual(get_cif_layers(Wrap), {"FOO", "BAZ"})

    #    class Lmap(rai.Compo):
    #        class Layers:
    #            ayy = rai.Layer("Ayy", cif_name="AYY")
    #            lmao = rai.Layer("Ayy", cif_name="LMAO")
    #        def _make(self):
    #            self.subcompos.append(Foo().proxy().map('ayy'))
    #            self.subcompos.append(Bar().proxy().map('lmao'))

    #    self.assertEqual(get_cif_layers(Lmap), {"AYY", "LMAO"})

    #    class HalfLmap(rai.Compo):
    #        class Layers:
    #            ayy = rai.Layer("Ayy", cif_name="AYY")
    #            lmao = rai.Layer("Ayy", cif_name="LMAO")
    #        def _make(self):
    #            self.subcompos.append(Foo().proxy().map('ayy'))
    #            self.subcompos.append(Bar().proxy())

    #    self.assertEqual(get_cif_layers(HalfLmap), {"AYY", "BAR"})


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


    # TODO
    # still figuring out how best to pass exporter options
    # or whether these types of things should even be handled in exporter

    #def test_lname_policy_cli(self):
    #    pwd = os.getcwd()
    #    with tempfile.TemporaryDirectory() as folder:
    #        os.chdir(folder)

    #        Path('mymodule.py').write_text(
    #            "import raimad as rai\n"
    #            "\n"
    #            "class MyCompo(rai.Compo):\n"
    #            "    def _make(self):\n"
    #            "        self.geoms.update({'foo': [[(0, 0), (0, 1), (1, 1)]]})"
    #            )

    #        proc_default = subprocess.run(shlex.split(
    #            f'{sys.executable} -m raimad export mymodule:MyCompo'
    #            ), check=True, capture_output=True)

    #        proc_warn = subprocess.run(shlex.split(
    #            f'{sys.executable} -m raimad export mymodule:MyCompo '
    #            '--exporter-opts lname_policy fallback-klay-warn'
    #            ), check=True, capture_output=True)

    #        proc_nowarn = subprocess.run(shlex.split(
    #            f'{sys.executable} -m raimad export mymodule:MyCompo '
    #            '--exporter-opts lname_policy fallback-klay'
    #            ), check=True, capture_output=True)


    #    os.chdir(pwd)

    #    self.assertTrue(b'CIFLayerNameWarning' in proc_default.stderr)
    #    self.assertTrue(b'CIFLayerNameWarning' in proc_warn.stderr)
    #    self.assertTrue(b'CIFLayerNameWarning' not in proc_nowarn.stderr)


