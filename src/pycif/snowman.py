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

        base = pc.Circle(50).proxy().map('snow')
        torso = pc.Circle(40).proxy().map('snow')
        head = pc.Circle(20).proxy().map('snow')

        torso.snap_above(base)
        head.snap_above(torso)

        eye_l = pc.Circle(eye_size).proxy().map('pebble')

        eye_l.marks.center.to(
            head.bbox.interpolate(0.3, 0.7)
            )

        eye_r = eye_l.copy()
        eye_r.vflip(head.bbox.mid[0])
        # TODO flip at arbitrary angle around point?
        # also, for hflip/vflip, is passed point,
        # automatically pick coordinate.

        nose = pc.CustomPoly([
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

