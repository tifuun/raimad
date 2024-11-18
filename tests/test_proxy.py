import unittest

import raimad as rai

class TestProxy(unittest.TestCase):

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

        self.assertFalse(p1.autogenned)
        self.assertFalse(p1.deepcopied)

        # The `.subcompos` of a component should return
        # directly the proxies that were assigned into it,
        # which were created explicitly in the _make function,
        # so should be marked not autogenned

        class MyCompo(rai.Compo):
            def _make(self):
                self.subcompos.c = rai.Circle(10).proxy()

        mycompo = MyCompo()

        self.assertFalse(mycompo.subcompos.c.autogenned)
        self.assertFalse(mycompo.subcompos.c.deepcopied)

        # `.subcompos` of a *proxy*, on the other hand,
        # should autogenerate proxies on top of the manual proxies.
        # It should be a deepcopy, since we can do
        # `.subcompos` on `.subcompos`.

        mycompo_p = mycompo.proxy()

        self.assertTrue(mycompo_p.subcompos.c.autogenned)
        self.assertTrue(mycompo_p.subcompos.c.deepcopied)

if __name__ == '__main__':
    unittest.main()

