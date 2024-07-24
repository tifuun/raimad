"""
Autotests for dictlist.
"""

import unittest

from raimad.dictlist import DictList

class TestDictList(unittest.TestCase):

    def test_dictlist_as_dict(self):
        dl = DictList()
        dl["a"] = 5
        dl["b"] = 6

        self.assertEqual(len(dl), 2)
        self.assertEqual(set(dl.keys()), {"a", "b"})
        self.assertEqual(set(dl.values()), {5, 6})
        self.assertEqual(dl["a"], 5)
        self.assertEqual(dl["b"], 6)

        dl["a"] += 2

        self.assertEqual(len(dl), 2)
        self.assertEqual(set(dl.keys()), {"a", "b"})
        self.assertEqual(set(dl.values()), {7, 6})
        self.assertEqual(dl["a"], 7)
        self.assertEqual(dl["b"], 6)

    def test_dictlist_as_list(self):
        dl = DictList()
        dl.append(4)
        dl.append(5)

        self.assertEqual(len(dl), 2)
        self.assertEqual(set(dl.keys()), {0, 1})
        self.assertEqual(set(dl.values()), {4, 5})
        self.assertEqual(dl[0], 4)
        self.assertEqual(dl[1], 5)

        dl[1] = 8

        self.assertEqual(len(dl), 2)
        self.assertEqual(dl[0], 4)
        self.assertEqual(dl[1], 8)
        self.assertEqual(set(dl.keys()), {0, 1})
        self.assertEqual(set(dl.values()), {4, 8})

    def test_dictlist_as_object(self):
        dl = DictList()
        dl.ayy = 5
        dl.b = 6

        self.assertEqual(len(dl), 2)
        self.assertEqual(set(dl.keys()), {"ayy", "b"})
        self.assertEqual(set(dl.values()), {5, 6})
        self.assertEqual(dl.ayy, 5)
        self.assertEqual(dl.b, 6)

        dl.ayy += 2

        self.assertEqual(len(dl), 2)
        self.assertEqual(set(dl.keys()), {"ayy", "b"})
        self.assertEqual(set(dl.values()), {7, 6})
        self.assertEqual(dl.ayy, 7)
        self.assertEqual(dl.b, 6)

    def test_dictlist_indexing(self):
        dl = DictList()
        dl["a"] = 5
        dl.b = 6

        self.assertEqual(len(dl), 2)
        self.assertEqual(set(dl.keys()), {"a", "b"})
        self.assertEqual(set(dl.values()), {5, 6})
        self.assertEqual(dl["a"], 5)
        self.assertEqual(dl["b"], 6)
        self.assertEqual(dl[0], 5)
        self.assertEqual(dl[1], 6)

        with self.assertRaises(IndexError):
            dl[2]

        with self.assertRaises(IndexError):
            dl[2] = 2

        dl[1] += 2

        self.assertEqual(len(dl), 2)
        self.assertEqual(set(dl.keys()), {"a", "b"})
        self.assertEqual(set(dl.values()), {5, 8})
        self.assertEqual(dl["a"], 5)
        self.assertEqual(dl["b"], 8)
        self.assertEqual(dl[0], 5)
        self.assertEqual(dl[1], 8)

    def test_dictlist_assign(self):
        dl = DictList()

        with self.assertRaises(KeyError):
            dl["keys"] = 5

        with self.assertRaises(KeyError):
            dl["_mydict"] = 5

        dl._mything = 5
        self.assertEqual(dl._mything, 5)
        self.assertEqual(len(dl), 0)

        with self.assertRaises(KeyError):
            dl["_mything"]

        with self.assertRaises(AttributeError):
            dl.keys = 5

    def _test_dictlist_filter(self, dl):
        """
        Helper method for testing whether _filter_set or _filter_get
        methods work correctly.
        They work exactly the same, but at different points in time
        (assigning an item vs querying and item),
        so we can use the same test payload.
        """

        dl.append('ayy')
        dl['foo'] = 'bar'
        dl.baz = 'baq'

        self.assertEqual(dl[0], 'AYY')
        self.assertEqual(dl[1], 'BAR')
        self.assertEqual(dl[2], 'BAQ')

        self.assertEqual(dl['foo'], 'BAR')
        self.assertEqual(dl['baz'], 'BAQ')

        self.assertEqual(dl.foo, 'BAR')
        self.assertEqual(dl.baz, 'BAQ')

        self.assertEqual(set(dl.keys()), {0, 'foo', 'baz'})
        self.assertEqual(set(dl.values()), {'AYY', 'BAR', 'BAQ'})
        self.assertEqual(
            [[key, val] for key, val in dl.items()],
            [
                [0, 'AYY'],
                ['foo', 'BAR'],
                ['baz', 'BAQ'],
                ]
            )

    def test_dictlist_filter_set(self):
        class DictListSet(DictList):
            def _filter_set(self, val):
                return val.upper()

        self._test_dictlist_filter(DictListSet())

    def test_dictlist_filter_get(self):
        class DictListGet(DictList):
            def _filter_get(self, val):
                return val.upper()

        self._test_dictlist_filter(DictListGet())

    def test_dictlist_init(self):
        class DictListSet(DictList):
            def _filter_set(self, val):
                return val.upper()

        dl = DictList()
        dl.append('ayy')
        dl_view = DictListSet(dl._dict, copy=False)
        dl_view.append('lmao')

        self.assertEqual(dl[0], 'ayy')
        self.assertEqual(dl[1], 'LMAO')

        with self.assertRaises(TypeError):
            DictList(dl._dict)

        with self.assertRaises(TypeError):
            DictList(dl._dict, True)

        with self.assertRaises(TypeError):
            DictList(dl)

        with self.assertRaises(TypeError):
            DictList('invalid type')

    def test_dictlist_post_init(self):
        class DictListPostInit(DictList):
            def _post_init(self):
                self._myattr = 'hello'

        dl = DictListPostInit()
        self.assertEqual(dl._myattr, 'hello')


if __name__ == '__main__':
    unittest.main()

