"""
Test for lmap
"""

import unittest

import pycif as pc

class TestLMap(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_lmap_compose_none_x_none(self):
        """
        """
        below = pc.LMap(None)
        above = pc.LMap(None)
        below.compose(above)

        self.assertEqual(below.shorthand, None)
        self.assertEqual(below['somelayer'], 'somelayer')
        self.assertEqual(below['someotherlayer'], 'someotherlayer')

    def test_lmap_compose_none_x_str(self):
        """
        """
        below = pc.LMap(None)
        above = pc.LMap('theonelayer')
        below.compose(above)

        self.assertEqual(below.shorthand, 'theonelayer')
        self.assertEqual(below['test1'], 'theonelayer')
        self.assertEqual(below['test2'], 'theonelayer')

    def test_lmap_compose_none_x_dict(self):
        """
        """
        below = pc.LMap(None)
        above = pc.LMap({
            'ayy': 'lmao',
            'foo': 'bar',
            })
        below.compose(above)

        self.assertEqual(below['ayy'], 'lmao')
        self.assertEqual(below['foo'], 'bar')
        with self.assertRaises(KeyError):
            # TODO custom error for lmap that derives from
            # keyerror?
            below['notpresent']

    def test_lmap_compose_str_x_none(self):
        """
        """
        below = pc.LMap('theonelayer')
        above = pc.LMap(None)
        below.compose(above)

        self.assertEqual(below.shorthand, 'theonelayer')
        self.assertEqual(below['first'], 'theonelayer')
        self.assertEqual(below['second'], 'theonelayer')

    def test_lmap_compose_str_x_str(self):
        """
        """
        below = pc.LMap('first')
        above = pc.LMap('theonelayer')
        below.compose(above)

        self.assertEqual(below.shorthand, 'theonelayer')
        self.assertEqual(below['first'], 'theonelayer')
        self.assertEqual(below['second'], 'theonelayer')

    def test_lmap_compose_str_x_dict(self):
        """
        """
        below = pc.LMap('theone')
        above = pc.LMap({
            'theone': 'theother',
            'notpresent': 'cantgethere',
            })
        below.compose(above)

        self.assertEqual(below['theone'], 'theother')
        # TODO unsure what the proper behavior should be
        # when getting `notpresent` or some completely other key

    def test_lmap_compose_dict_x_none(self):
        """
        """
        below = pc.LMap({
            'ayy': 'lmao',
            'foo': 'bar',
            })
        above = pc.LMap(None)
        below.compose(above)

        self.assertEqual(below['ayy'], 'lmao')
        self.assertEqual(below['foo'], 'bar')
        with self.assertRaises(KeyError):
            below['notpresent']
        with self.assertRaises(KeyError):
            below['bar']

    def test_lmap_compose_dict_x_str(self):
        """
        """
        below = pc.LMap({
            'ayy': 'lmao',
            'foo': 'bar',
            })
        above = pc.LMap('theone')
        below.compose(above)

        self.assertEqual(below['ayy'], 'theone')
        self.assertEqual(below['foo'], 'theone')
        self.assertEqual(below['rando'], 'theone')
        # TODO do we want to be able to specify a
        # "lenient dict" layermap that acts like a dict layermap,
        # but instead throwing error on unknown layer,
        # it just passes it thru?

    def test_lmap_compose_dict_x_dict(self):
        """
        """
        below = pc.LMap({
            'ayy': 'lmao',
            'foo': 'bar',
            'syn': 'ack',
            'yin': 'yang',
            })
        above = pc.LMap({
            'bar': 'baz',
            'ack': 'nack',
            })
        below.compose(above)

        self.assertEqual(below['ayy'], 'lmao')
        self.assertEqual(below['foo'], 'baz')
        self.assertEqual(below['syn'], 'nack')
        self.assertEqual(below['yin'], 'yang')


if __name__ == '__main__':
    unittest.main()

