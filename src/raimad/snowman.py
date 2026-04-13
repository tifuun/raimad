"""snowman.py: home to Snowman compo."""

import raimad as rai

#
# DITHER PATTERNS PRODUCED BY PERPLEXITY.AI
#
# PROMPTS: produce a 32x32 binary bitmap artwork fitting the theme "snow". Use
# `.` for white pixels and `*` for black pixels.
#
# produce one more artwork with the same parameters, now fitting the theme
# "carrot".
#
# produce one more artwork with the same parameters, now fitting the theme
# "pebble".
#

pattern_snow = rai.lyp.DitherPattern(
    lines=(
            "................................",
            "...................*............",
            ".........*......................",
            "..................*.............",
            "......*.........................",
            "...................**...........",
            "...........*....................",
            "....................*...........",
            "...*............................",
            "......................*.........",
            "..................*.............",
            "....................*...........",
            "........*.......................",
            "....................*...........",
            "..............*.................",
            "...................*............",
            "......................*.........",
            "..................*.............",
            "....................*...........",
            "...................*............",
            "....*...........................",
            "..................**............",
            "..................**............",
            "..................***...........",
            ".............*****..............",
            "..........***********...........",
            ".......****************.........",
            ".....********************.......",
            "...**********************.......",
            "..************************......",
            ".****************************...",
            "******************************..",
        ),
    name='snow',
    )

pattern_carrot = rai.lyp.DitherPattern(
    lines=(
            "................................",
            "................................",
            "................................",
            "...............***..............",
            "..............*****.............",
            "..............*****.............",
            "...............***..............",
            "................*...............",
            "................*...............",
            "................**..............",
            "...............****.............",
            "..............******............",
            ".............*******............",
            "............********............",
            "............*********...........",
            "...........**********...........",
            "..........***********...........",
            "..........************..........",
            "........**************..........",
            ".......***************..........",
            ".......****************.........",
            "......*****************.........",
            ".....******************.........",
            ".....*******************........",
            ".....********************.......",
            "......********************......",
            ".......*******************......",
            "........******************......",
            ".........****************.......",
            "..........***************.......",
            "...........*************........",
            "............***********.........",
            ".............*********..........",
        ),
    name='carrot',
    )

pattern_pebble = rai.lyp.DitherPattern(
    lines=(
            "................................",
            "................................",
            "................................",
            "................................",
            "..............*****.............",
            ".............*******............",
            "............*********...........",
            "............*********...........",
            ".............*******............",
            "..............*****.............",
            "................................",
            "..........******................",
            ".........********...............",
            "........**********..............",
            "........***********.............",
            ".........**********.............",
            "..........*******...............",
            ".............****...............",
            "................................",
            "..............******............",
            ".............********...........",
            "............*********...........",
            "............**********..........",
            ".............********...........",
            "..............******............",
            "................................",
            "................................",
            "................................",
            "................................",
            "................................",
            "................................",
            "................................",
        ),
    name='pebble',
    )

class Snowman(rai.Compo):
    """A sample component."""

    browser_tags = ["builtin", "example"]
    _experimental_extra_lname_transformers = [{
        'snow': 'SNOW',
        'carrot': 'CROT',
        'pebble': 'PEBL',
        }]

    _experimental_lyp = {
        'SNOW': rai.lyp.Properties(
            fill_color='#eeeeee',
            frame_color='#444444',
            dither_pattern=pattern_snow,
            ),
        'CROT': rai.lyp.Properties(
            fill_color='#ff8800',
            frame_color='#444444',
            dither_pattern=pattern_carrot,
            ),
        'PEBL': rai.lyp.Properties(
            fill_color='#444444',
            frame_color='#aaaaaa',
            dither_pattern=pattern_pebble,
            ),
        }

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
            ) -> None:

        base = rai.Circle(50).proxy().map('snow')
        torso = rai.Circle(40).proxy().map('snow')
        head = rai.Circle(20).proxy().map('snow')

        torso.snap_above(base)
        head.snap_above(torso)

        eye_l = rai.Circle(eye_size).proxy().map('pebble')

        eye_l.marks.center.to(
            head.bbox.interpolate(0.3, 0.7)
            )

        eye_r = eye_l.shallow_copy()
        eye_r.hflip(head.bbox.mid[0])
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

