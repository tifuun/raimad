import unittest
from .utils import XmlComparisonMixin
from io import StringIO

import raimad

SNOWMAN_LYP="""\
<?xml version="1.0" encoding="utf-8"?>
<layer-properties>
<custom-dither-pattern>
<pattern>
<line>................................</line>
<line>...................*............</line>
<line>.........*......................</line>
<line>..................*.............</line>
<line>......*.........................</line>
<line>...................**...........</line>
<line>...........*....................</line>
<line>....................*...........</line>
<line>...*............................</line>
<line>......................*.........</line>
<line>..................*.............</line>
<line>....................*...........</line>
<line>........*.......................</line>
<line>....................*...........</line>
<line>..............*.................</line>
<line>...................*............</line>
<line>......................*.........</line>
<line>..................*.............</line>
<line>....................*...........</line>
<line>...................*............</line>
<line>....*...........................</line>
<line>..................**............</line>
<line>..................**............</line>
<line>..................***...........</line>
<line>.............*****..............</line>
<line>..........***********...........</line>
<line>.......****************.........</line>
<line>.....********************.......</line>
<line>...**********************.......</line>
<line>..************************......</line>
<line>.****************************...</line>
<line>******************************..</line>
</pattern>
<order>0</order>
<name>snow</name>
</custom-dither-pattern>
<custom-dither-pattern>
<pattern>
<line>................................</line>
<line>................................</line>
<line>................................</line>
<line>...............***..............</line>
<line>..............*****.............</line>
<line>..............*****.............</line>
<line>...............***..............</line>
<line>................*...............</line>
<line>................*...............</line>
<line>................**..............</line>
<line>...............****.............</line>
<line>..............******............</line>
<line>.............*******............</line>
<line>............********............</line>
<line>............*********...........</line>
<line>...........**********...........</line>
<line>..........***********...........</line>
<line>..........************..........</line>
<line>........**************..........</line>
<line>.......***************..........</line>
<line>.......****************.........</line>
<line>......*****************.........</line>
<line>.....******************.........</line>
<line>.....*******************........</line>
<line>.....********************.......</line>
<line>......********************......</line>
<line>.......*******************......</line>
<line>........******************......</line>
<line>.........****************.......</line>
<line>..........***************.......</line>
<line>...........*************........</line>
<line>............***********.........</line>
<line>.............*********..........</line>
</pattern>
<order>1</order>
<name>carrot</name>
</custom-dither-pattern>
<custom-dither-pattern>
<pattern>
<line>................................</line>
<line>................................</line>
<line>................................</line>
<line>................................</line>
<line>..............*****.............</line>
<line>.............*******............</line>
<line>............*********...........</line>
<line>............*********...........</line>
<line>.............*******............</line>
<line>..............*****.............</line>
<line>................................</line>
<line>..........******................</line>
<line>.........********...............</line>
<line>........**********..............</line>
<line>........***********.............</line>
<line>.........**********.............</line>
<line>..........*******...............</line>
<line>.............****...............</line>
<line>................................</line>
<line>..............******............</line>
<line>.............********...........</line>
<line>............*********...........</line>
<line>............**********..........</line>
<line>.............********...........</line>
<line>..............******............</line>
<line>................................</line>
<line>................................</line>
<line>................................</line>
<line>................................</line>
<line>................................</line>
<line>................................</line>
<line>................................</line>
</pattern>
<order>2</order>
<name>pebble</name>
</custom-dither-pattern>
<properties>
<source>SNOW</source>
<frame-color>#444444</frame-color>
<fill-color>#eeeeee</fill-color>
<dither-pattern>C0</dither-pattern>
</properties>
<properties>
<source>CROT</source>
<frame-color>#444444</frame-color>
<fill-color>#ff8800</fill-color>
<dither-pattern>C1</dither-pattern>
</properties>
<properties>
<source>PEBL</source>
<frame-color>#aaaaaa</frame-color>
<fill-color>#444444</fill-color>
<dither-pattern>C2</dither-pattern>
</properties>
<name/>
</layer-properties>"""

class TestLYP(XmlComparisonMixin, unittest.TestCase):
    #def test_lyp_dict(self):
    #    self.assertXmlEqual(
    #        raimad.export_lyp({
    #            'FOO': {'name': 'bar', 'frame_color': '#ff00ff'},
    #            'BAR': {'name': 'foo', 'width': 10},
    #            }),
    #        (
    #            '<?xml version="1.0" encoding="utf-8"?>\n'
    #            '<layer-properties>\n'
    #            '<properties>\n'
    #            '<source>FOO</source>\n'
    #            '<frame-color>#ff00ff</frame-color>\n'
    #            '<name>bar</name>\n'
    #            '</properties>\n'
    #            '<properties>\n'
    #            '<source>BAR</source>\n'
    #            '<width>10</width>\n'
    #            '<name>foo</name>\n'
    #            '</properties>\n'
    #            '<name/>\n'
    #            '</layer-properties>'
    #            )
    #        )

    def test_lyp_dataclass(self):
        self.assertXmlEqual(
            raimad.cif.lyp.export_properties({
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
            raimad.cif.lyp.export_properties({
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

    def test_lyp_exporter(self):
        self.assertXmlEqual(
            raimad.export_lyp(raimad.Snowman()),
            SNOWMAN_LYP
            )

#if __name__ == '__main__':
#    snowman = raimad.Snowman()
#    raimad.export_cif(snowman, 'Snowman.cif')
#    raimad.export_lyp(snowman, 'Snowman.lyp')
#
