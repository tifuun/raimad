import unittest
from sys import stderr

from .utils.mixins import GeomsEqual
import raimad as rai

# Checks whether each method does or does not exist.
# String of three chars is just syntax sugar for list of 3 bools.
# x = Method should exist
# space = method should not exist
# idx 0: in Transform
# idx 1: in Proxy
# idx 2: in BoundPoint

TABLE = {
        'protate'    : 'xx ',
        'crotate'    : 'xx ',
        'orotate'    : 'xx ',
        'rotate'     : 'xxx',

        'pmove'      : 'xxx',
        'cmove'      : 'xxx',
        'movex'      : 'xxx',
        'movey'      : 'xxx',
        'move'       : 'xxx',

        'pflip'      : 'xx ',
        'cflip'      : 'xx ',
        'hflip'      : 'xxx',
        'vflip'      : 'xxx',
        'flip'       : 'xxx',

        'apscale'    : 'xx ',
        'acscale'    : 'xx ',
        'ppscale'    : 'xx ',
        'ccscale'    : 'xx ',
        'cpscale'    : 'xx ',
        'pcscale'    : 'xx ',
        'ascale'     : '  x',
        'pscale'     : '  x',
        'cscale'     : '  x',
        'scale'      : 'xxx',

        'to'         : '  x',
        'pto'        : '  x',
        'cto'        : '  x',

        'snap_above' : ' x ',
        'snap_below' : ' x ',
        'snap_left'  : ' x ',
        'snap_right' : ' x ',
}


class TestNewEditingTable(GeomsEqual, unittest.TestCase):
    def test_editing_table(self):
        for method, ticks in TABLE.items():
            print(f'{method = }', file=stderr)
            in_tf, in_proxy, in_bp = (c == 'x' for c in ticks)
            self.assertIs(in_tf, hasattr(rai.Transform, method))
            self.assertIs(in_proxy, hasattr(rai.Proxy, method))
            self.assertIs(in_bp, hasattr(rai.BoundPoint, method))

