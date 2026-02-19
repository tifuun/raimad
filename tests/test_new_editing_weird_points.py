"""
Test that new editing works with different types of point-like objects.

RAIMAD does not use numpy,
but we want people to be able to pass in numpy arrays
as points,
and also other weird but workable things.
"""
import unittest

import numpy as np

from .utils import GeomsEqual
import raimad as rai

class IdxVec2:
    """
    custom vec2 class that supports indexing
    """
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __getitem__(self, idx):
        if idx == 0:
            return self._x
        if idx == 1:
            return self._y
        raise ArgumentError('foobar')

class AttrVec2:
    """
    custom vec2 class that supports x, y attributes
    """
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

# TODO test incompatible classes
# TODO what takes precedence, indexing, or x/y


class TestNewEditingWeirdVectors(GeomsEqual, unittest.TestCase):
    def test_move_weird_vectors(self):
        all_vecs = (
            tup_i := (2,   3  ),
            tup_f := (2.0, 3.0),
            tup_m := (2,   3.0),
            tup_n := (2,   np.float64(3)),
            lst_i := [2,   3  ],
            lst_f := [2.0, 3.0],
            lst_m := [2,   3.0],
            lst_n := [2,   np.float64(3)],
            arr_i32 := np.array((2, 3), dtype=np.int32),
            arr_i64 := np.array((2, 3), dtype=np.int64),
            arr_f32 := np.array((2, 3), dtype=np.float32),
            arr_f64 := np.array((2, 3), dtype=np.float64),
            arr_m := np.array((np.float64(2), np.int32(3)), dtype=object),
            idx_i := IdxVec2(2,   3  ),
            idx_f := IdxVec2(2.0, 3.0),
            idx_m := IdxVec2(2,   3.0),
            idx_n := IdxVec2(2,   np.float64(3)),
            #atr_i := AttrVec2(2,   3  ),
            #atr_f := AttrVec2(2.0, 3.0),
            #atr_m := AttrVec2(2,   3.0),
            #atr_n := AttrVec2(2,   np.float64(3)),
        )

        self.assertIs(type(arr_m[0]), type(arr_f64[0]))
        self.assertIs(type(lst_n[1]), type(arr_f64[0]))
        self.assertIs(type(lst_n[0]), int)
        self.assertIs(type(tup_n[1]), type(arr_f64[0]))
        self.assertIs(type(tup_n[0]), int)
        self.assertIs(type(idx_n[1]), type(arr_f64[0]))
        self.assertIs(type(idx_n[0]), int)
        #self.assertIs(type(atr_n.y), type(arr_f64[0]))
        #self.assertIs(type(atr_n.x), int)
        self.assertIs(type(arr_m[1]), type(arr_i32[0]))

        for vec in all_vecs:
            self.assertIsInstance(vec, rai.types.Vec2)

        box = rai.CustomPoly((
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1),
            ))

        self.assertManyGeomsEqual((
            *(
                box.proxy().move(vec)
                for vec in all_vecs),
            *(
                {
                    'root': [
                        [
                            (-1 + 2, -1 + 3),
                            (1  + 2, -1 + 3),
                            (1  + 2, 1  + 3),
                            (-1 + 2, 1  + 3),
                            ]
                        ]
                    }
                ,)
            ))


