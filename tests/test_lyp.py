import unittest
from .utils import XmlComparisonMixin
from io import StringIO

import raimad

class TestLYP(XmlComparisonMixin, unittest.TestCase):
    def test_lyp_dict(self):
        self.assertXmlEqual(
            raimad.export_lyp({
                'FOO': {'name': 'bar', 'frame_color': '#ff00ff'},
                'BAR': {'name': 'foo', 'width': 10},
                }),
            (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                '<layer-properties>\n'
                '<properties>\n'
                '<source>FOO</source>\n'
                '<frame-color>#ff00ff</frame-color>\n'
                '<name>bar</name>\n'
                '</properties>\n'
                '<properties>\n'
                '<source>BAR</source>\n'
                '<width>10</width>\n'
                '<name>foo</name>\n'
                '</properties>\n'
                '<name/>\n'
                '</layer-properties>'
                )
            )

    def test_lyp_dataclass(self):
        self.assertXmlEqual(
            raimad.export_lyp({
                'FOO': raimad.lyp.Properties(
                    name='bar',
                    frame_color='#ff00ff'
                    ),
                'BAR': raimad.lyp.Properties(
                    name='foo',
                    width=10
                    ),
                }),
            (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                '<layer-properties>\n'
                '<properties>\n'
                '<source>FOO</source>\n'
                '<frame-color>#ff00ff</frame-color>\n'
                '<name>bar</name>\n'
                '</properties>\n'
                '<properties>\n'
                '<source>BAR</source>\n'
                '<width>10</width>\n'
                '<name>foo</name>\n'
                '</properties>\n'
                '<name/>\n'
                '</layer-properties>'
                )
            )

    def test_lyp_stream(self):
        stream = StringIO()

        self.assertXmlEqual(
            raimad.export_lyp({
                'FOO': raimad.lyp.Properties(
                    name='bar',
                    frame_color='#ff00ff'
                    ),
                'BAR': raimad.lyp.Properties(
                    name='foo',
                    width=10
                    ),
                }),
            (
                '<?xml version="1.0" encoding="utf-8"?>\n'
                '<layer-properties>\n'
                '<properties>\n'
                '<source>FOO</source>\n'
                '<frame-color>#ff00ff</frame-color>\n'
                '<name>bar</name>\n'
                '</properties>\n'
                '<properties>\n'
                '<source>BAR</source>\n'
                '<width>10</width>\n'
                '<name>foo</name>\n'
                '</properties>\n'
                '<name/>\n'
                '</layer-properties>'
                )
            )


