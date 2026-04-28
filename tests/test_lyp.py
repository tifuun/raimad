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

LYP_BUILTIN_DITHERS="""\
<?xml version="1.0" encoding="utf-8"?>
<layer-properties>
<properties>
<source>FOO</source>
<dither-pattern>I0</dither-pattern>
</properties>
<properties>
<source>BAR</source>
<dither-pattern>I24</dither-pattern>
</properties>
<name/>
</layer-properties>"""

LYP_BUILTIN_LINES="""\
<?xml version="1.0" encoding="utf-8"?>
<layer-properties>
<properties>
<source>FOO</source>
<line-style>I1</line-style>
<width>5</width>
</properties>
<properties>
<source>BAR</source>
<line-style>I6</line-style>
<width>10</width>
</properties>
<name/>
</layer-properties>"""

LYP_CUSTOM_LINE="""\
<?xml version="1.0" encoding="utf-8"?>
<layer-properties>
<custom-line-style>
<pattern>*.*..*.*.....**..*..**..**.**...</pattern>
<order>0</order>
<name>ascii</name>
</custom-line-style>
<properties>
<source>FOO</source>
<line-style>C0</line-style>
<width>5</width>
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

        self.assertXmlEqual(
            raimad.export_lyp(raimad.Snowman().proxy()),
            SNOWMAN_LYP
            )

    def test_lyp_builtin_dithers(self):
        class Foo(raimad.Compo):
            _experimental_lyp = {
                'FOO': raimad.lyp.Properties(
                    dither_pattern=raimad.lyp.dithers.solid
                    ),
                'BAR': raimad.lyp.Properties(
                    dither_pattern=raimad.lyp.dithers['22.5 degree up']
                    ),
                }
            def _make(self):
                self.subcompos.r1 = raimad.RectLW(4, 4).proxy().map('foo')
                self.subcompos.r2 = (
                        raimad.RectLW(4, 4).proxy().map('bar').movex(5)
                        )

        self.assertXmlEqual(
            raimad.export_lyp(Foo()),
            LYP_BUILTIN_DITHERS
            )

        #raimad.export_lyp(Foo(), 'Foo.lyp')
        #raimad.export_cif(Foo(), 'Foo.cif')
        # TODO KLayout craps out if we rename FOO and BAR to L0 and L1
        # here???????????????

    def test_lyp_builtin_lines(self):
        class Foo(raimad.Compo):
            _experimental_lyp = {
                'FOO': raimad.lyp.Properties(
                    line_style=raimad.lyp.lines.dotted,
                    width=5,
                    ),
                'BAR': raimad.lyp.Properties(
                    line_style=raimad.lyp.lines['long dashed'],
                    width=10,
                    ),
                }
            def _make(self):
                self.subcompos.r1 = raimad.RectLW(4, 4).proxy().map('foo')
                self.subcompos.r2 = (
                        raimad.RectLW(4, 4).proxy().map('bar').movex(5)
                        )

        #raimad.export_lyp(Foo(), 'Foo.lyp')
        #raimad.export_cif(Foo(), 'Foo.cif')

        self.assertXmlEqual(
            raimad.export_lyp(Foo()),
            LYP_BUILTIN_LINES
            )

    def test_lyp_custom_lines(self):
        class Foo(raimad.Compo):
            _experimental_lyp = {
                'FOO': raimad.lyp.Properties(
                    line_style=raimad.lyp.CustomLineStyle(
                        name='ascii',
                        pattern='*.*..*.*.....**..*..**..**.**...',
                        ),
                    width=5,
                    ),
                }
            def _make(self):
                self.subcompos.r1 = raimad.RectLW(4, 4).proxy().map('foo')

        raimad.export_lyp(Foo(), 'Foo.lyp')
        raimad.export_cif(Foo(), 'Foo.cif')

        self.assertXmlEqual(
            raimad.export_lyp(Foo()),
            LYP_CUSTOM_LINE
            )

if __name__ == '__main__':
    snowman = raimad.Snowman()
    raimad.export_cif(snowman, 'Snowman.cif')
    raimad.export_lyp(snowman, 'Snowman.lyp')
#
