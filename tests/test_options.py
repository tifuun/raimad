import unittest

import pycif as pc

log = pc.get_logger(__name__)

class A(pc.Component.Layers):
    l2 = pc.Layer()
    l1 = pc.Layer()

class B(pc.Component.Layers):
    l5 = pc.Layer()
    weeee = pc.Layer()
    l3 = pc.Layer()

class C(B, A):
    l8 = pc.Layer()
    l7 = pc.Layer()
    l6 = pc.Layer()

class TestLayers(unittest.TestCase):

    def test_invalid_layer_name(self):
        with self.assertRaises(pc.err.InvalidLayerNameError):
            class InvalidLayers(pc.Component.Layers):
                root = pc.Layer('this should be fine')
                keys = pc.Layer('this one should fail')

    def test_layer_inheritance(self):

        a = A()
        b = B()
        c = C()

        self.assertTupleEqual(a, ('l2', 'l1'))
        self.assertTupleEqual(b, ('l5', 'weeee', 'l3'))
        self.assertTupleEqual(c, ('l8', 'l7', 'l6', 'l5', 'weeee', 'l3', 'l2', 'l1'))

    def test_layer_iter(self):

        la = []
        for layer in A:
            la.append(layer)

        self.assertListEqual(la, ['l2', 'l1'])

        la.clear()

        la = []
        for layer in A():
            la.append(layer)

        self.assertListEqual(la, ['l2', 'l1'])

    def test_layer_get(self):

        a = A()
        self.assertIs(a.l2, a[0])
        self.assertIs(a.l2, A[0])
        self.assertIs(a.l2, A.l2)
        self.assertIs(a, A())

