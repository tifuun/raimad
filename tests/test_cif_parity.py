import unittest

from functools import partial
import raimad as rai
import cift as cf

from .utils import GeomsEqual

def polydump(compo, n):
    from pathlib import Path
    from subprocess import run
    exporter = rai.cif.Reuse(compo)
    Path(f'{n}_r.cif').write_text(exporter.cif_string)
    Path(f'{n}.gv').write_text(exporter.stat.call_graph_dot())
    rai.export_cif(compo, f'{n}_nr.cif', exporter=rai.cif.NoReuse)
    run(f'dot -Tpdf < {n}.gv > {n}.pdf', shell=True, check=True)


class TestCIFReuse(GeomsEqual, unittest.TestCase):

    def assertParity(self, compo):
        """Assert that compo produces same footprint in reuse and noreuse."""

        parse = partial(cf.parse, grammar=cf.grammar.lenient_layers)

        reuse = rai.cif.Reuse(compo)
        noreuse = rai.cif.NoReuse(compo)

        geoms_reuse = parse(reuse.cif_string)
        geoms_noreuse = parse(noreuse.cif_string)

        self.assertGeomsEqual(geoms_reuse, geoms_noreuse)


    def test_cif_parity_rectlw(self):
        self.assertParity(rai.RectLW(10, 10))


    def test_cif_reuse_staircase(self):
        """
        Generate weird staircase thing with lots of stacked proxies
        """
        class Foo(rai.Compo):
            def _make(self):
                box = rai.RectLW(10, 20).proxy().bbox.mid.to(0, 0)
                self.subcompos.append(box)
                for x in range(15):
                    box = (box.proxy()
                        .move(25, 25)
                        .bbox.mid.rotate(rai.fullcircle / 26)
                        )
                    self.subcompos.append(box)

                
        #compo = Foo()
        #polydump(compo, 'staircase')

        # TODO this test does nothing now actually because cift
        # is WAY TOO SLOW to parse this thing!!
        #self.assertParity(Foo())



if __name__ == '__main__':

    unittest.main()

