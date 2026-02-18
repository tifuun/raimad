import unittest
from io import StringIO

from .utils import GeomsEqual
import raimad as rai

class TestNewEditing(GeomsEqual, unittest.TestCase):
    def test_editing_methods(self):

        ### Common methods: Transform ###

        # Rotate around point (xy tuple)
        self.assertTrue(hasattr(rai.Transform, 'protate'))
        # Rotate around coord pair (separate x, y params)
        self.assertTrue(hasattr(rai.Transform, 'crotate'))
        # pick protate / crotate automatically based on number of args
        self.assertTrue(hasattr(rai.Transform,  'rotate'))

        # separate move by coords (single arg)
        self.assertTrue(hasattr(rai.Transform,  'movex'))
        self.assertTrue(hasattr(rai.Transform,  'movey'))
        # move by xy tuple
        self.assertTrue(hasattr(rai.Transform, 'pmove'))
        # move by separate x, y coords
        self.assertTrue(hasattr(rai.Transform, 'cmove'))
        # pick automatically based on number of args
        self.assertTrue(hasattr(rai.Transform,  'move'))

        # flip along x and y at once (tuple)
        self.assertTrue(hasattr(rai.Transform, 'pflip'))
        # flip along x and y at once (separate args)
        self.assertTrue(hasattr(rai.Transform, 'cflip'))
        # mirror along horizontal axis (y coord)
        self.assertTrue(hasattr(rai.Transform, 'vflip'))
        # mirror along vertical axis (x coord)
        self.assertTrue(hasattr(rai.Transform, 'hflip'))
        # pick pflip or cflip based on number of args
        self.assertTrue(hasattr(rai.Transform,  'flip'))

        # Scale should also take AROUND argument
        # scale both x and y axes by same factor
        self.assertTrue(hasattr(rai.Transform, 'ascale'))
        # scale x and y independently by different factors (xy tuple)
        self.assertTrue(hasattr(rai.Transform, 'pscale'))
        # scale x and y independently by different factors (x, y factors)
        self.assertTrue(hasattr(rai.Transform, 'cscale'))
        # pick ascale, pscale or cscale based on number and type of args
        self.assertTrue(hasattr(rai.Transform,  'scale'))

        ### Common methods: Proxy ###

        self.assertTrue(hasattr(rai.Proxy, 'protate'))
        self.assertTrue(hasattr(rai.Proxy, 'crotate'))
        self.assertTrue(hasattr(rai.Proxy,  'rotate'))

        self.assertTrue(hasattr(rai.Proxy,  'movex'))
        self.assertTrue(hasattr(rai.Proxy,  'movey'))
        self.assertTrue(hasattr(rai.Proxy, 'pmove'))
        self.assertTrue(hasattr(rai.Proxy, 'cmove'))
        self.assertTrue(hasattr(rai.Proxy,  'move'))

        self.assertTrue(hasattr(rai.Proxy, 'pflip'))
        self.assertTrue(hasattr(rai.Proxy, 'cflip'))
        self.assertTrue(hasattr(rai.Proxy, 'vflip'))
        self.assertTrue(hasattr(rai.Proxy, 'hflip'))
        self.assertTrue(hasattr(rai.Proxy,  'flip'))

        self.assertTrue(hasattr(rai.Proxy, 'pscale'))
        self.assertTrue(hasattr(rai.Proxy, 'cscale'))
        self.assertTrue(hasattr(rai.Proxy, 'ascale'))
        # pick ascale, pscale or cscale based on number and type of args
        self.assertTrue(hasattr(rai.Proxy,  'scale'))

        ### Common methods: BP ###

        # only one rotate method: the boundpoint itself
        # IS the x/y coords we're rotating about
        self.assertTrue(hasattr(rai.BoundPoint, 'rotate'))

        # These are same as transform/proxy methods --
        # doesn't make sense for movement to depend
        # on position of the bp
        self.assertTrue(hasattr(rai.BoundPoint,  'movex'))
        self.assertTrue(hasattr(rai.BoundPoint,  'movey'))
        self.assertTrue(hasattr(rai.BoundPoint, 'pmove'))
        self.assertTrue(hasattr(rai.BoundPoint, 'cmove'))
        self.assertTrue(hasattr(rai.BoundPoint,  'move'))

        # Again, the point itself IS what we're flipping about
        # either both coords or single coord
        self.assertTrue(hasattr(rai.BoundPoint,  'flip'))
        self.assertTrue(hasattr(rai.BoundPoint, 'vflip'))
        self.assertTrue(hasattr(rai.BoundPoint, 'hflip'))

        # Here the boundpoint acts as the reference point
        # of the scale
        self.assertTrue(hasattr(rai.BoundPoint, 'pscale'))
        self.assertTrue(hasattr(rai.BoundPoint, 'cscale'))
        self.assertTrue(hasattr(rai.BoundPoint, 'ascale'))
        self.assertTrue(hasattr(rai.BoundPoint,  'scale'))

        ### Boundpoint special: to ###

        self.assertTrue(hasattr(rai.BoundPoint,  'to'))
        self.assertTrue(hasattr(rai.BoundPoint, 'pto'))
        self.assertTrue(hasattr(rai.BoundPoint, 'cto'))

    def test_editing_rotate(self):
        shape = rai.CustomPoly((
            (0, 0),
            (15, 0),
            (12, 20),
            ))

        # Test tuple vs coord
        self.assertManyGeomsEqual((
            shape.proxy(). rotate(rai.quartercircle, (3, 5)),
            shape.proxy(). rotate(rai.quartercircle,  3, 5 ),
            shape.proxy().protate(rai.quartercircle, (3, 5)),
            shape.proxy().crotate(rai.quartercircle,  3, 5 ),
            ))

        # test that default rotation is around origin
        self.assertManyGeomsEqual((
            shape.proxy(). rotate(rai.quartercircle, (0, 0)),
            shape.proxy(). rotate(rai.quartercircle,       ),
            ))

        # test that default rotation is around origin (tuple)
        self.assertManyGeomsEqual((
            shape.proxy().protate(rai.quartercircle, (0, 0)),
            shape.proxy().protate(rai.quartercircle,       ),
            ))

        # test that default rotation is around origin (coords)
        self.assertManyGeomsEqual((
            shape.proxy().crotate(rai.quartercircle,  0, 0 ),
            shape.proxy().crotate(rai.quartercircle,       ),
            ))

        ## And also test boundpoint
        # remember, boundpoint has only one variant of rotate,
        # since the bp itself is the reference point of the rotation
        self.assertManyGeomsEqual((
            shape.proxy().bbox.bot_left.rotate(rai.quartercircle),
            shape.proxy().rotate(rai.quartercircle, shape.bbox.bot_left),
            ))

    def test_editing_move(self):
        shape = rai.CustomPoly((
            (0, 0),
            (15, 0),
            (12, 20),
            ))

        # Check coordinates vs tuple
        self.assertManyGeomsEqual((
            shape.proxy(). move((3, 5)),
            shape.proxy(). move( 3, 5 ),
            shape.proxy().pmove((3, 5)),
            shape.proxy().cmove( 3, 5 ),
            ))

        # check x
        self.assertManyGeomsEqual((
            shape.proxy(). move (5, 0),
            shape.proxy(). movex(5   ),
            ))

        # check y
        self.assertManyGeomsEqual((
            shape.proxy(). move (0, 5),
            shape.proxy(). movey(5   ),
            ))

        ## And also test boundpoint
        # This is no different from proxy move;
        # boundpoint position does not affect movement

        self.assertManyGeomsEqual((
            shape.proxy().bbox.bot_left. move((3, 5)),
            shape.proxy().bbox.bot_left. move( 3, 5 ),
            shape.proxy().bbox.bot_left.pmove((3, 5)),
            shape.proxy().bbox.bot_left.cmove( 3, 5 ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy().bbox.bot_left. move (5, 0),
            shape.proxy().bbox.bot_left. movex(5   ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy().bbox.bot_left. move (0, 5),
            shape.proxy().bbox.bot_left. movey(5   ),
            ))

    def test_editing_flip(self):
        shape = rai.CustomPoly((
            (0, 0),
            (15, 0),
            (12, 20),
            ))

        # test coords vs tuple
        self.assertManyGeomsEqual((
            shape.proxy(). flip((3, 5)),
            shape.proxy(). flip( 3, 5 ),
            shape.proxy().pflip((3, 5)),
            shape.proxy().cflip( 3, 5 ),
            ))

        # test vflip
        self.assertManyGeomsEqual((
            shape.proxy(). flip(5, 0),
            shape.proxy().vflip(5   ),
            ))

        # test hflip
        self.assertManyGeomsEqual((
            shape.proxy(). flip(0, 5),
            shape.proxy().hflip(5   ),
            ))

        ## Test boundpoint

        self.assertManyGeomsEqual((
            shape.proxy().flip(shape.bbox.bot_left),
            shape.proxy().bbox.bot_left.flip(),
            ))

        # test using only single coordinate of a boundpoint
        self.assertManyGeomsEqual((
            shape.proxy().vflip(shape.bbox.bot_left[1]),
            shape.proxy().bbox.bot_left.vflip(),
            ))

        self.assertManyGeomsEqual((
            shape.proxy().hflip(shape.bbox.bot_left[0]),
            shape.proxy().bbox.bot_left.hflip(),
            ))

        # same as above but with concrete coords

        box = rai.CustomPoly((
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1),
            ))

        # vflip along bottom left = mirror along left edge
        # left edge itself (x = -1) stays where it is
        self.assertManyGeomsEqual((
            box.proxy().vflip(box.bbox.bot_left[1]),
            box.proxy().bbox.bot_left.vflip(),
            {
                'root': [
                    [
                        (-1, -1),
                        (-2, -1),
                        (-2, 1),
                        (-1, 1),
                        ]
                    ]
                }
            ))

        # hflip along bottom left = mirror along bottom edge
        # bottom edge itself (y = -1) stays where it is
        self.assertManyGeomsEqual((
            box.proxy().hflip(box.bbox.bot_left[0]),
            box.proxy().bbox.bot_left.hflip(),
            {
                'root': [
                    [
                        (-1, -1),
                        (1, -1),
                        (1, -2),
                        (-1, -2),
                        ]
                    ]
                }
            ))

    def test_editing_scale(self):
        shape = rai.CustomPoly((
            (0, 0),
            (15, 0),
            (12, 20),
            ))

        self.assertManyGeomsEqual((
            shape.proxy(). scale((3, 5)),
            shape.proxy(). scale( 3, 5 ),
            shape.proxy().pscale((3, 5)),
            shape.proxy().cscale( 3, 5 ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy(). scale(  5, 5  ),
            shape.proxy(). scale( (5, 5) ),
            shape.proxy(). scale(  5,   ),
            shape.proxy().ascale(  5,   ),
            ))

        ## Test boundpoint

        self.assertManyGeomsEqual((
            shape.proxy().bbox.bot_left. scale((3, 5)),
            shape.proxy().bbox.bot_left. scale( 3, 5 ),
            shape.proxy().bbox.bot_left.pscale((3, 5)),
            shape.proxy().bbox.bot_left.cscale( 3, 5 ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy().bbox.bot_left. scale(  5, 5  ),
            shape.proxy().bbox.bot_left. scale( (5, 5) ),
            shape.proxy().bbox.bot_left. scale(  5,   ),
            shape.proxy().bbox.bot_left.ascale(  5,   ),
            ))

        ## Test reference point parameter
        ## Both manual parameter and boundpoint

        box = rai.CustomPoly((
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1),
            ))

        # around origin - blows up from center
        self.assertManyGeomsEqual((
            box.proxy().scale(2, (0, 0)),
            box.proxy().bbox.mid.scale(2),
            {
                'root': [
                    [
                        (-2, -2),
                        (2, -2),
                        (2, 2),
                        (-2, 2),
                        ]
                    ]
                }
            ))

        # around bottom left - blows up into top right
        self.assertManyGeoms((
            box.proxy().scale(2, (-1, -1)),
            box.proxy().bbox.bot_left.scale(2),
            {
                'root': [
                    [
                        (-1, -1),
                        (3, -1),
                        (3, 3),
                        (-1, 3),
                        ]
                    ]
                }
            ))





