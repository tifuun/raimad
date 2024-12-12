import unittest
import re

import raimad as rai

from .utils import GeomsEqual

class TestProxy(GeomsEqual, unittest.TestCase):

    def check_tower(self, proxy, expected):
        try:
            tower_actual = tuple(proxy.descend_p())
            self.assertEqual(len(tower_actual), len(expected))
            for \
                    this_proxy, (expected_autogenned, expected_deepcopied) \
                    in zip(tower_actual, expected, strict=True):

                #print(expected_autogenned, this_proxy.autogenned, expected_deepcopied, this_proxy.deepcopied)
                self.assertEqual(expected_autogenned, this_proxy.autogenned)
                self.assertEqual(expected_deepcopied, this_proxy.deepcopied)

        except AssertionError as err:
            print("EXPECTED: ")
            print(expected)
            print("ACTUAL: ")
            print(proxy)
            raise err

    def test_proxy_origin(self):
        """
        Test that the "origin" of a proxy is tracked correctly.
        By "origin" I mean whether the proxy was created explicitly
        or automatically (Proxy.autogenned),
        and whether it was a result of a deepcopy operation
        (Proxy.deepcopied)
        """

        # Just a regular proxy of a compo,
        # should be labeled not autogenned
        # (because we explicitly create it)
        compo = rai.Circle(10)
        p1 = compo.proxy()

        self.check_tower(p1, (
            (False, False),
            ))

        # The `.subcompos` of a component should return
        # directly the proxies that were assigned into it,
        # which were created explicitly in the _make function,
        # so should be marked not autogenned

        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.c = rai.Circle(10).proxy()

        mycompo = MyCompo()

        self.check_tower(mycompo.subcompos.c, (
            (False, False),
            ))

        # `.subcompos` of a *proxy*, on the other hand,
        # should autogenerate proxies on top of the manual proxies.
        # It should be created via Proxy.deep_copy_reassign, since we can do
        # `.subcompos` on `.subcompos`,
        # but it should not be marked a `deepcopied`,
        # since it's the top of the tower

        mycompo_p = mycompo.proxy()

        self.check_tower(mycompo_p.subcompos.c, (
            (True, False),
            (False, False),
            ))

        # Okay, but now if the use `Proxy.subcompos.subcompos`,
        # the result should be marked both autogenned and deepcopied,
        # because it was created as the result of a deepcopy
        class MyUpperCompo(rai.Compo):
            def _make(self):
                self.subcompos.m = MyCompo().proxy()

        my_upper_compo = MyUpperCompo()

        # TODO is this good?
        self.check_tower(my_upper_compo.subcompos.m.subcompos.c, (
            (True, False),
            (False, False),
            ))

        # TODO is this good?
        my_upper_compo_p = my_upper_compo.proxy()
        self.check_tower(my_upper_compo_p.subcompos.m.subcompos.c, (
            (True, False),
            (True, True),
            (False, False),
            ))

    def test_proxy_str(self):

        compo = rai.Snowman()
        p = compo.proxy().proxy().deep_copy()
        p2 = p.subcompos.base.proxy()

        self.assertTrue(
            re.match(
                r'^<Manual Proxy at .* with <.*> of\s*'
                r'Automatic Proxy at .* with <.*> of\s*'
                r'Automatic deepcopied Proxy at .* with <.*> of\s*'
                r'Manual Proxy at .* with <.*> of\s*'
                r'Circle at .*>'
                ,
                str(p2)
                )
            )
        self.assertEqual(str(p2), repr(p2))

    def test_proxy_scale(self):
        rect = rai.RectLW(10, 10).proxy().bbox.mid.to((0, 0))

        horiz = rect.proxy().scale(2, 1)
        vert = rect.proxy().scale(1, 2)
        both = rect.proxy().scale(2, 2)
        both_alt = rect.proxy().scale(2)

        self.assertGeomsEqual(
            rect.steamroll(),
            {'root': [[(-5, -5), (5, -5), (5, 5), (-5, 5)]]}
            )

        self.assertGeomsEqual(
            horiz.steamroll(),
            {'root': [[(-10, -5), (10, -5), (10, 5), (-10, 5)]]}
            )

        self.assertGeomsEqual(
            vert.steamroll(),
            {'root': [[(-5, -10), (5, -10), (5, 10), (-5, 10)]]}
            )

        self.assertGeomsEqual(
            both.steamroll(),
            {'root': [[(-10, -10), (10, -10), (10, 10), (-10, 10)]]}
            )

        self.assertGeomsEqual(
            both_alt.steamroll(),
            {'root': [[(-10, -10), (10, -10), (10, 10), (-10, 10)]]}
            )


if __name__ == '__main__':
    unittest.main()

