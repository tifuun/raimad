"""Snowman: very basic example component."""

import pycif as pc

class Snowman(pc.Component):
    """Snowman: very basic example component."""

    class Layers(pc.Component.Layers):
        snow = pc.Layer(
            "A collection of individual crystals of frozen dihydrogen monoxide"
            )
        carrot = pc.Layer(
            "Bio-lithographic layer characterised by lambda = approx. 6E-7nm"
            )
        pebble = pc.Layer(
            "Non-malleable polycrystalline silicon layer"
            )

    class Options(pc.Component.Options):
        l_nose = pc.Option.Geometric(
            10,
            "Nose length"
            )
        eye_size = pc.Option(
            2,
            "Eye radius"
            )

    class Marks(pc.Component.Marks):
        nose_tip = pc.Mark("Tip of the nose")

    def _make(self):
        base = pc.Circle(50)
        torso = pc.Circle(40)
        head = pc.Circle(20)

        torso.snap_above(base)
        head.snap_above(torso)

        eye_l = pc.Circle(self.options.eye_size)
        eye_r = eye_l.copy()

        eye_l.marks.center.to(
            head.bbox.interpolate(0.3, 0.7)
            )

        eye_r.marks.center.to(
            head.bbox.interpolate(0.7, 0.7)
            )

        nose_tip = (self.options.l_nose, 0)
        nose = pc.CustomPolygon([
            (0, 2),
            nose_tip,
            (0, -2)
            ])

        nose.move(
            head.bbox.interpolate(0.5, 0.5)
            )

        self.add_subpolygon(base, self.layers.snow)
        self.add_subpolygon(torso, self.layers.snow)
        self.add_subpolygon(head, self.layers.snow)

        self.add_subpolygon(eye_l, self.layers.pebble)
        self.add_subpolygon(eye_r, self.layers.pebble)

        self.add_subpolygon(nose, self.layers.carrot)

        self.marks.nose_tip = nose_tip

