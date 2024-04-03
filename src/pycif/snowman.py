import pycif as pc

class Snowman(pc.Compo):
    """
    Snowman

    A sample component with three layers, two options, and one mark.
    """
    browser_tags = ["builtin", "example"]

    class Marks:
        nose = pc.Mark("Tip of the snowman's nose")

    class Options:
        nose_length = pc.Option.Geometric("Length of nose")
        eye_size = pc.Option.Geometric("Eye radius")

    class Layers:
        pebble = pc.Layer(
            "Non-malleable polycrystalline silicon layer"
            )
        carrot = pc.Layer(
            "Bio-lithographic layer characterised by lambda = approx. 6E-7nm"
            )
        snow = pc.Layer(
            "A collection of individual crystals of frozen dihydrogen monoxide"
            )

    def _make(
            self,
            nose_length: float = 10,
            eye_size: float = 2,
            ):
        base = self.subcompo(pc.Circle(50) @ 'snow', 'base')
        torso = self.subcompo(pc.Circle(40) @ 'snow', 'torso')
        head = self.subcompo(pc.Circle(20) @ 'snow', 'head')

        torso.snap_above(base)
        head.snap_above(torso)

        eye_l = self.subcompo(pc.Circle(eye_size) @ 'pebble')

        eye_l.marks.center.to(
            head.bbox.interpolate(0.3, 0.7)
            )

        eye_r = self.subcompo(eye_l.copy())
        eye_r.vflip(head.bbox.mid[0])
        # TODO flip at arbitrary angle around point?
        # also, for hflip/vflip, is passed point,
        # automatically pick coordinate.

        nose = self.subcompo(pc.CustomPoly([
            (0, 2),
            ('tip', (nose_length, 0)),
            (0, -2)
            ]) @ 'carrot',
            'nose')

        nose.move(
            head.bbox.interpolate(0.5, 0.5)
            )

        self.marks.nose = nose.marks.tip

