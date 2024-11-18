"""Test that the .subcompos attribute works properly."""

import unittest

import raimad as rai

class TestSubcompoIntrospection(unittest.TestCase):

    def test_subcompo_introspection_basic(self):
        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.a = rai.RectLW(10, 10).proxy()

        compo = MyCompo()
        self.assertTrue(
            rai.eq(
                compo.bbox.top_left,
                compo.subcompos.a.bbox.top_left
                )
            )

    def test_subcompo_introspection_proxy(self):
        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.a = (
                    rai.RectLW(10, 10)
                    .proxy()
                    .move(10, 0)
                    )

        compo = MyCompo()
        self.assertTrue(
            rai.eq(
                compo.bbox.top_left,
                compo.subcompos.a.bbox.top_left
                )
            )

    def test_subcompo_introspection_proxy_proxy(self):
        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.a = (
                    rai.RectLW(10, 10)
                    .proxy()
                    .move(10, 0)
                    )

        compo = MyCompo()
        proxy = compo.proxy().move(0, 10)

        self.assertTrue(
            rai.eq(
                compo.bbox.top_left,
                compo.subcompos.a.bbox.top_left
                )
            )

        self.assertTrue(
            rai.eq(
                proxy.bbox.top_left,
                proxy.subcompos.a.bbox.top_left
                )
            )

        self.assertFalse(
            rai.eq(
                compo.bbox.top_left,
                proxy.subcompos.a.bbox.top_left
                )
            )

        self.assertFalse(
            rai.eq(
                proxy.bbox.top_left,
                compo.subcompos.a.bbox.top_left
                )
            )




if __name__ == '__main__':
    unittest.main()

