import unittest

import raimad as rai


class TestProxy(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()

