"""
Test layer handling.

More higher-level version of test_lmap.py
"""

import unittest

import raimad as rai

class TestLayers(unittest.TestCase):

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

