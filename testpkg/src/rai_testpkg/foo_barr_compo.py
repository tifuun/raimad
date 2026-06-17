import raimad as rai

class FooBarrCompo(rai.Compo):
    class Options:
        width = rai.Option.Geometric("Width of the wire")

    class Layers:
        nbtin_opt = rai.Layer("Niobium-titanium-nitride optical deposition")

    class Marks:
        tip = rai.Mark("tip of the wire")

    browser_tags = ["example"]
    _experimental_extra_lname_transformers = [{
        'nbtin_opt': 'NBTN',
        }]

    _experimental_lyp = {
        'NBTN': rai.lyp.Properties(
            fill_color='#555555',
            frame_color='#880088',
            ),
        }

    def _make(self, width: float = 10):
        self.subcompos.box = rai.RectLW(20, width).proxy().map('nbtin_opt')
        self.marks.tip = self.subcompos.box.bbox.mid_right
