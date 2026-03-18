"""
Test that new editing works with different types of point-like objects.

RAIMAD does not use numpy,
but we want people to be able to pass in numpy arrays
as points,
and also other weird but workable things.

Transform's methods are not tested here directly,
only Proxy and BoundPoint.
Hopefully test_new_editing.py tests
Transform's methods sufficiently.
"""
import unittest
import inspect
import typing

import numpy as np

from .utils import GeomsEqual
import raimad as rai

class IdxVec2:
    """
    custom vec2 class that supports indexing
    """
    _x: float
    _y: float

    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    def __getitem__(self, idx: int) -> float:
        """
        Get either x or y coordinate.

        Deliberately lazy `int` type hint instead of `Literal[0, 1]`.
        """
        if idx == 0:
            return self._x
        if idx == 1:
            return self._y
        raise TypeError('foobar')

#class AttrVec2:
#    """
#    custom vec2 class that supports x, y attributes
#    """
#    def __init__(self, x, y):
#        self._x = x
#        self._y = y
#
#    @property
#    def x(self):
#        return self._x
#
#    @property
#    def y(self):
#        return self._y

# TODO negative test incompatible classes

ALL_VECS = (
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

### BEGIN (edited) LLM CODE ###
#
# PROMPT:
#
# write python script that scans all methods of class `Foo` and makes sure
# none of their arguments are annotated as type `float`
#

def contains_strict_annotation(annotation: type) -> bool:
    if annotation in rai.types.types_strict:
        return True

    # Handle typing constructs like Optional[float], list[float], dict[str, float], etc.
    origin = typing.get_origin(annotation)
    if origin is None:
        return False

    args = typing.get_args(annotation)
    return any(contains_strict_annotation(arg) for arg in args)

def ensure_no_strict_args(cls: type) -> None:
    for name, member in inspect.getmembers(cls, predicate=inspect.isfunction):
        sig = inspect.signature(member)
        for param in sig.parameters.values():
            ann = param.annotation
            if ann is inspect._empty:  # no annotation
                continue
            if contains_strict_annotation(ann):
                raise AssertionError(
                    f"Method {cls.__name__}.{name} has parameter "
                    f"'{param.name}' annotated with or containing strict type: {ann!r}"
                )


### END LLM CODE ###

class TestNewEditingWeirdVectors(GeomsEqual, unittest.TestCase):
    def test_internal(self):

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

        for vec in ALL_VECS:
            self.assertIsInstance(vec, rai.types.Vec2)

    def test_no_strict_args(self):
        """
        Test that Proxy, BoundPoint, and Transform
        never take `Vec2S` or `NumS` (i.e. strict raimad types)
        as input -- should be the more open-ended
        `Vec2` and `Num` types to allow user to pass in a broader
        range of things.
        """
        ensure_no_strict_args(rai.Proxy)
        ensure_no_strict_args(rai.BoundPoint)
        ensure_no_strict_args(rai.Transform)
        ensure_no_strict_args(rai.Compo)


    #------------#
    # Proxy      #
    #------------#

    def test_move_weird_vectors_proxy(self):
        box = rai.CustomPoly((
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1),
            ))

        self.assertManyGeomsEqual((
            #*(
            #    box.proxy().move(vec)
            #    for vec in ALL_VECS),
            box.proxy().move(ALL_VECS[0]),
            box.proxy().move(ALL_VECS[1]),
            box.proxy().move(ALL_VECS[2]),
            box.proxy().move(ALL_VECS[3]),
            box.proxy().move(ALL_VECS[4]),
            box.proxy().move(ALL_VECS[5]),
            box.proxy().move(ALL_VECS[6]),
            box.proxy().move(ALL_VECS[7]),
            box.proxy().move(ALL_VECS[8]),
            box.proxy().move(ALL_VECS[9]),
            box.proxy().move(ALL_VECS[10]),
            box.proxy().move(ALL_VECS[11]),
            box.proxy().move(ALL_VECS[12]),
            box.proxy().move(ALL_VECS[13]),
            box.proxy().move(ALL_VECS[14]),
            box.proxy().move(ALL_VECS[15]),
            box.proxy().move(ALL_VECS[16]),
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

    def test_scale_weird_vectors_proxy(self):
        box = rai.CustomPoly((
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1),
            ))

        self.assertManyGeomsEqual((
            *(
                box.proxy().scale(vec)
                for vec in ALL_VECS),
            *(
                {
                    'root': [
                        [
                            (-1 * 2, -1 * 3),
                            (1  * 2, -1 * 3),
                            (1  * 2, 1  * 3),
                            (-1 * 2, 1  * 3),
                            ]
                        ]
                    }
                ,)
            ))

        self.assertManyGeomsEqual((
            *(
                box.proxy().scale(vec, vec)
                for vec in ALL_VECS),
            *(
                {
                    'root': [
                        [
                            (-4, -9),
                            (-0, -9),
                            (-0, -3),
                            (-4, -3),
                            ]
                        ]
                    }
                ,)
            ))

    def test_flip_weird_vectors_proxy(self):
        box = rai.CustomPoly((
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1),
            ))

        self.assertManyGeomsEqual((
            *(
                box.proxy().flip(vec)
                for vec in ALL_VECS),
            *(
                {
                    'root': [
                        [
                            (5, 7),
                            (3, 7),
                            (3, 5),
                            (5, 5),
                            ]
                        ]
                    }
                ,)
            ))

    def test_rotate_weird_vectors_proxy(self):
        box = rai.CustomPoly((
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1),
            ))

        self.assertManyGeomsEqual((
            *(
                box.proxy().rotate(angle, vec)
                for vec in ALL_VECS
                for angle in (
                    rai.quartercircle,
                    90 / 180 * 3.14159,
                    np.float64(np.pi / 2),
                    )
                ),
            *(
                {
                    'root': [
                        [
                            (6, 0),
                            (6, 2),
                            (4, 2),
                            (4, 0),
                            ]
                        ]
                    }
                ,)
            ))

    #------------#
    # BoundPoint #
    #------------#

    def test_move_weird_vectors_bp(self):
        box = rai.CustomPoly((
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1),
            ))

        self.assertManyGeomsEqual((
            *(
                box.proxy().bbox.mid_left.move(vec)
                for vec in ALL_VECS),
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

    def test_scale_weird_vectors_bp(self):
        box = rai.CustomPoly((
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1),
            ))

        self.assertManyGeomsEqual((
            *(
                box.proxy().bbox.mid.scale(vec)
                for vec in ALL_VECS),
            *(
                {
                    'root': [
                        [
                            (-1 * 2, -1 * 3),
                            (1  * 2, -1 * 3),
                            (1  * 2, 1  * 3),
                            (-1 * 2, 1  * 3),
                            ]
                        ]
                    }
                ,)
            ))

        self.assertManyGeomsEqual((
            *(
                box.proxy().scale(vec, vec)
                for vec in ALL_VECS),
            *(
                {
                    'root': [
                        [
                            (-4, -9),
                            (-0, -9),
                            (-0, -3),
                            (-4, -3),
                            ]
                        ]
                    }
                ,)
            ))

    def test_rotate_weird_vectors_bp(self):
        box = rai.CustomPoly((
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1),
            ))

        self.assertManyGeomsEqual((
            *(
                box.proxy().bbox.mid.rotate(angle)
                for angle in (
                    rai.quartercircle,
                    90 / 180 * 3.14159,
                    np.float64(np.pi / 2),
                    )
                ),
            *(
                {
                    'root': [
                        [
                            (1, -1),
                            (1, 1),
                            (-1, 1),
                            (-1, -1),
                            ]
                        ]
                    }
                ,)
            ))

    def test_to_weird_vectors(self):
        box = rai.CustomPoly((
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1),
            ))

        self.assertManyGeomsEqual((
            *(
                box.proxy().bbox.mid.to(vec)
                for vec in ALL_VECS),
            *(
                {
                    'root': [
                        [
                            (1, 2),
                            (3, 2),
                            (3, 4),
                            (1, 4),
                            ]
                        ]
                    }
                ,)
            ))

