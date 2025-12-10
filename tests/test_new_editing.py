import unittest
from io import StringIO

import raimad as rai

class TestNewEditing(unittest.TestCase):
    def test_editing_methods(self):

        ### Common methods: Transform ###

        self.assertTrue(hasattr(rai.Transform,  'rotate'))
        self.assertTrue(hasattr(rai.Transform, 'protate'))
        self.assertTrue(hasattr(rai.Transform, 'crotate'))

        self.assertTrue(hasattr(rai.Transform,  'movex'))
        self.assertTrue(hasattr(rai.Transform,  'movey'))
        self.assertTrue(hasattr(rai.Transform,  'move'))
        self.assertTrue(hasattr(rai.Transform, 'pmove'))
        self.assertTrue(hasattr(rai.Transform, 'cmove'))

        self.assertTrue(hasattr(rai.Transform,  'flip'))
        self.assertTrue(hasattr(rai.Transform, 'pflip'))
        self.assertTrue(hasattr(rai.Transform, 'cflip'))
        self.assertTrue(hasattr(rai.Transform, 'vflip'))
        self.assertTrue(hasattr(rai.Transform, 'hflip'))

        self.assertTrue(hasattr(rai.Transform,  'scale'))
        self.assertTrue(hasattr(rai.Transform, 'pscale'))
        self.assertTrue(hasattr(rai.Transform, 'cscale'))
        self.assertTrue(hasattr(rai.Transform, 'ascale'))

        ### Common methods: Proxy ###

        self.assertTrue(hasattr(rai.Proxy,  'rotate'))
        self.assertTrue(hasattr(rai.Proxy, 'protate'))
        self.assertTrue(hasattr(rai.Proxy, 'crotate'))

        self.assertTrue(hasattr(rai.Proxy,  'movex'))
        self.assertTrue(hasattr(rai.Proxy,  'movey'))
        self.assertTrue(hasattr(rai.Proxy,  'move'))
        self.assertTrue(hasattr(rai.Proxy, 'pmove'))
        self.assertTrue(hasattr(rai.Proxy, 'cmove'))

        self.assertTrue(hasattr(rai.Proxy,  'flip'))
        self.assertTrue(hasattr(rai.Proxy, 'pflip'))
        self.assertTrue(hasattr(rai.Proxy, 'cflip'))
        self.assertTrue(hasattr(rai.Proxy, 'vflip'))
        self.assertTrue(hasattr(rai.Proxy, 'hflip'))

        self.assertTrue(hasattr(rai.Proxy,  'scale'))
        self.assertTrue(hasattr(rai.Proxy, 'pscale'))
        self.assertTrue(hasattr(rai.Proxy, 'cscale'))
        self.assertTrue(hasattr(rai.Proxy, 'ascale'))

        ### Common methods: BP ###

        self.assertTrue(hasattr(rai.BoundPoint, 'rotate'))

        self.assertTrue(hasattr(rai.BoundPoint,  'movex'))
        self.assertTrue(hasattr(rai.BoundPoint,  'movey'))
        self.assertTrue(hasattr(rai.BoundPoint,  'move'))
        self.assertTrue(hasattr(rai.BoundPoint, 'pmove'))
        self.assertTrue(hasattr(rai.BoundPoint, 'cmove'))

        self.assertTrue(hasattr(rai.BoundPoint,  'flip'))

        self.assertTrue(hasattr(rai.BoundPoint,  'scale'))
        self.assertTrue(hasattr(rai.BoundPoint, 'pscale'))
        self.assertTrue(hasattr(rai.BoundPoint, 'cscale'))
        self.assertTrue(hasattr(rai.BoundPoint, 'ascale'))

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
        self.assertManyGeomsEqual((
            shape.proxy(). rotate(rai.quartercicle, (3, 5)),
            shape.proxy(). rotate(rai.quartercicle,  3, 5 ),
            shape.proxy().protate(rai.quartercicle, (3, 5)),
            shape.proxy().crotate(rai.quartercicle,  3, 5 ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy(). rotate(rai.quartercicle, (0, 0)),
            shape.proxy(). rotate(rai.quartercicle,       ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy().protate(rai.quartercicle, (0, 0)),
            shape.proxy().protate(rai.quartercicle,       ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy().crotate(rai.quartercicle,  0, 0 ),
            shape.proxy().crotate(rai.quartercicle,       ),
            ))

        ## And also test boundpoint

        self.assertManyGeomsEqual((
            shape.proxy().bbox.bot_left.rotate(rai.quartercicle),
            shape.proxy().rotate(rai.quartercicle, shape.bbox.bot_left),
            ))

    def test_editing_move(self):
        shape = rai.CustomPoly((
            (0, 0),
            (15, 0),
            (12, 20),
            ))

        self.assertManyGeomsEqual((
            shape.proxy(). move((3, 5)),
            shape.proxy(). move( 3, 5 ),
            shape.proxy().pmove((3, 5)),
            shape.proxy().cmove( 3, 5 ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy(). move (5, 0),
            shape.proxy(). movex(5   ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy(). move (0, 5),
            shape.proxy(). movey(5   ),
            shape.proxy(). movey(5   ),
            ))

        ## And also test boundpoint

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
            shape.proxy().bbox.bot_left. movey(5   ),
            ))

    def test_editing_flip(self):
        shape = rai.CustomPoly((
            (0, 0),
            (15, 0),
            (12, 20),
            ))

        self.assertManyGeomsEqual((
            shape.proxy(). flip((3, 5)),
            shape.proxy(). flip( 3, 5 ),
            shape.proxy().pflip((3, 5)),
            shape.proxy().cflip( 3, 5 ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy(). flip(5, 0),
            shape.proxy().vflip(5   ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy(). flip(0, 5),
            shape.proxy().hflip(5   ),
            ))

        ## Test boundpoint

        self.assertManyGeomsEqual((
            shape.proxy().flip(shape.bbox.bot_left)
            shape.proxy().bbox.bot_left.flip(),
            ))

        self.assertManyGeomsEqual((
            shape.proxy().vflip(shape.bbox.bot_left[1])
            shape.proxy().bbox.bot_left.vflip(),
            ))

        self.assertManyGeomsEqual((
            shape.proxy().vflip(shape.bbox.bot_left[0])
            shape.proxy().bbox.bot_left.hflip(),
            ))

    def test_editing_scale(self):
        shape = rai.CustomPoly((
            (0, 0),
            (15, 0),
            (12, 20),
            ))

        # AROUND PARAMETER????
        self.assertManyGeomsEqual((
            shape.proxy(). scale((3, 5)),
            shape.proxy(). scale( 3, 5 ),
            shape.proxy().pscale((3, 5)),
            shape.proxy().cscale( 3, 5 ),
            ))

        self.assertManyGeomsEqual((
            shape.proxy(). scale( 5, 5 ),
            shape.proxy(). scale( 5,   ),
            shape.proxy().ascale( 5,   ),
            ))


