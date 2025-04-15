"""
Test layer handling.

More higher-level version of test_lmap.py
"""

import unittest

import raimad as rai

from .utils import GeomsEqual

class TestLayers(unittest.TestCase, GeomsEqual):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_layers_root(self):
        """
        Test that a rectlw with no map ends up on root
        """
        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.append(
                    rai.RectLW(10, 10).proxy()
                    )

        self.assertEqual(
            set(MyCompo().steamroll().keys()),
            {'root'}
            )

    def test_layers_root_none(self):
        """
        Test that a rectlw with an explicit None lmap ends up on root
        """
        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.append(
                    rai.RectLW(10, 10)
                    .proxy()
                    .map(None)
                    )

        self.assertEqual(
            set(MyCompo().steamroll().keys()),
            {'root'}
            )

    def test_layers_discard(self):
        """
        Test that LMAPping a layer to None actually discards it.
        (bug 2025-04-14)
        """
        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.extend((
                    rai.RectLW(10, 10).proxy().map('foo'),
                    rai.RectLW(20, 20).proxy().map('bar'),
                ))

        compo = MyCompo()

        p0 = compo.proxy()
        p1 = compo.proxy().map({'foo': None, 'bar': 'bar'})
        p2 = compo.proxy().map({'foo': 'foo', 'bar': None})
        p3 = compo.proxy().map({'foo': None, 'bar': None})
        p4 = compo.proxy().map({'foo': None, 'bar': 'ayy'})
        p5 = compo.proxy().map({'foo': 'ayy', 'bar': None})
        p6 = compo.proxy().map({'foo': 'ayy', 'bar': 'lmao'})

        self.assertEqual(set(p0.steamroll().keys()), {'foo', 'bar'})
        self.assertEqual(set(p1.steamroll().keys()), {'bar'})
        self.assertEqual(set(p2.steamroll().keys()), {'foo'})
        self.assertEqual(set(p3.steamroll().keys()), set())
        self.assertEqual(set(p4.steamroll().keys()), {'ayy'})
        self.assertEqual(set(p5.steamroll().keys()), {'ayy'})
        self.assertEqual(set(p6.steamroll().keys()), {'ayy', 'lmao'})

        self.assertGeomsEqualButAllowDifferentNames(p0.steamroll(), p6.steamroll())
        self.assertGeomsEqualButAllowDifferentNames(p1.steamroll(), p4.steamroll())
        self.assertGeomsEqualButAllowDifferentNames(p2.steamroll(), p5.steamroll())
        self.assertEqual(len(p3.steamroll()), 0)

    def test_layers_root_stack(self):
        """
        Test that a "stack" of subcompos with no maps end up on root
        """
        class First(rai.Compo):
            def _make(self):
                self.subcompos.append(
                    rai.RectLW(10, 10)
                    .proxy()
                    )

        class Second(rai.Compo):
            def _make(self):
                self.subcompos.append(
                    First()
                    .proxy()
                    )

        class Third(rai.Compo):
            def _make(self):
                self.subcompos.append(
                    Second()
                    .proxy()
                    )

        self.assertEqual(
            set(Third().steamroll().keys()),
            {'root'}
            )

    def test_layers_root_stack_complex(self):
        """
        Test a "stack" of subcompos, each with a one-to-one lmap
        """
        class First(rai.Compo):
            def _make(self):
                self.subcompos.append(
                    rai.RectLW(10, 10)
                    .proxy()
                    .map({'root': 'foot'})
                    )

        class Second(rai.Compo):
            def _make(self):
                self.subcompos.append(
                    First()
                    .proxy()
                    .map({'foot': 'toot'})
                    )

        class Third(rai.Compo):
            def _make(self):
                self.subcompos.append(
                    Second()
                    .proxy()
                    .map({'toot': 'boot'})
                    )

        self.assertEqual(
            set(Third().steamroll().keys()),
            {'boot'}
            )


if __name__ == '__main__':
    unittest.main()

