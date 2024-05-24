import unittest

import raimad as rai

class TestSnowman(unittest.TestCase):

    def test_snowman(self):
        compo = rai.Snowman(nose_length=20, eye_size=2.5)
        geom = compo.steamroll()

        # Test layers
        self.assertEqual(geom.keys(), {'snow', 'carrot', 'pebble'})

        # Test three circles on snow layer
        self.assertEqual(len(geom['snow']), 3)

        # Test marks
        self.assertTrue('nose' in compo.marks.keys())


if __name__ == '__main__':
    unittest.main()

