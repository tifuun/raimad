import raimad as rai

class Snowman(rai.Compo):
    """
    Snowman

    A sample component with three layers, two options, and one mark.
    """
    browser_tags = ["builtin", "example"]

    class Marks:
        nose = rai.Mark("Tip of the snowman's nose")

    class Options:
        nose_length = rai.Option.Geometric("Length of nose")
        eye_size = rai.Option.Geometric("Eye radius")

    class Layers:
        pebble = rai.Layer(
            "Non-malleable polycrystalline silicon layer"
            )
        carrot = rai.Layer(
            "Bio-lithographic layer characterised by lambda = approx. 6E-7nm"
            )
        snow = rai.Layer(
            "A collection of individual crystals of frozen dihydrogen monoxide"
            )

    def _make(
            self,
            nose_length: float = 10,
            eye_size: float = 2,
            ):

        base = rai.Circle(50).proxy().map('snow')
        torso = rai.Circle(40).proxy().map('snow')
        head = rai.Circle(20).proxy().map('snow')

        torso.snap_above(base)
        head.snap_above(torso)

        eye_l = rai.Circle(eye_size).proxy().map('pebble')

        eye_l.marks.center.to(
            head.bbox.interpolate(0.3, 0.7)
            )

        eye_r = eye_l.copy()
        eye_r.vflip(head.bbox.mid[0])
        # TODO flip at arbitrary angle around point?
        # also, for hflip/vflip, is passed point,
        # automatically pick coordinate.

        nose = rai.CustomPoly([
            (0, 2),
            ('tip', (nose_length, 0)),
            (0, -2)
            ]).proxy().map('carrot')

        nose.move(
            *head.bbox.interpolate(0.5, 0.5)
            )

        self.marks.nose = nose.marks.tip

        self.subcompos.base = base
        self.subcompos.torso = torso
        self.subcompos.head = head
        self.subcompos.eye_l = eye_l
        self.subcompos.eye_r = eye_r
        self.subcompos.nose = nose

