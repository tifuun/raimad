"""
Tests for pycif 1.0.0 cif exporter.
As opposed to `test_cif_100`,
these tests use CIFT to verify the generated CIF files.
"""

import unittest

import cift as cf

import pycif as pc

class TestCIFT(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_cif_layer_simple(self):
        """
        """
        class MyCompo(pc.Compo):
            def _make(self):
                self.subcompos.rec = (
                    pc.RectWH(10, 20).proxy()
                    .map('mylayer')
                    .bbox.bot_left.to((0, 0))
                    )

        compo = MyCompo()
        exporter = pc.CIFExporter(
            compo,
            multiplier=1,
            rot_multiplier=1,
            cif_native=False,
            flatten_proxies=False,
            native_inline=False,
            transform_fatal=False
            )
        cif_string = exporter.cif_string
        parser = cf.Parser()
        parser.parse(cif_string)
        self.assertEqual(
            parser.layers,
            {
                'Lmylayer': [
                    (
                        (0, 0),
                        (10, 0),
                        (10, 20),
                        (0, 20),
                        )
                    ]
                }
            )


if __name__ == '__main__':
    unittest.main()

