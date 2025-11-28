"""noreuse.py: home to the NoReuse CIF exporter."""

from typing import Iterator
from warnings import warn
from typing import TypeAlias, Literal

import raimad as rai

Cifmap: TypeAlias = dict[str, str | None]
LnamePolicy: TypeAlias = Literal[
    "klay-warn",
    "klay",
    "strict",
    "numeric",
    ]

class CIFLayerNameWarning(UserWarning):
    """Warning about layer names that are not compatible with CIF."""

class NoReuse:
    """CIF Exporter that doesn't reuse subroutines."""

    def __init__(
            self,
            compo: 'rai.typing.CompoLike',
            multiplier: float = 1e2,
            #lname_policy: LnamePolicy = 'fallback-klay-warn',
            lname_policy: LnamePolicy = 'fallback-numeric',
            ) -> None:

        self.compo = compo
        self.rout_num = 1
        self.multiplier = multiplier

        self.lname_policy = lname_policy
        self.experimental_cell_names = True  # TODO Param
        self.ignore_annot_cif_name = False

        # This is used for numeric and fallback-numeric
        # layer policies.
        # Filled out progressively during the export process.
        self.layer_indices = {
            }

        self.cif_string = self._export_cif()
        self.lyp_string = ''
        #self.lyp_string = '\n'.join(_gen_lyp(self.annotmap))

        # TODO validate lname policy

    def _export_cif(self) -> str:
        return ''.join(self._yield_cif())

    def _yield_cif(self) -> Iterator[str]:
        """Yield lines of cif file."""
        first_rout = self.rout_num
        yield from self.yield_cif_bare(
            self.compo,
            #{},
            experimental_cell_name=type(self.compo.final()).__name__
            )
        yield f'C {first_rout};\n'
        yield 'E'

    def yield_cif_bare(
            self,
            compo: 'rai.typing.CompoLike',
            experimental_cell_name: str,
            #annotmap,
            ) -> Iterator[str]:
        """
        Recursively yield fragments of CIF of a particular component.

        This function takes a CompoLike and yields
        lines that define it, recursing down the tree of subcomponents.
        First come the DS line, then the
        compo's raw geometry,
        then calls calls to procedures that define subcompos,
        then DF,
        and finally the definitions of the subcompo procedures,
        which themselves contain subcompos procedures, and so on.
        Note that a call to the toplevel procedure
        (the one corresponding to the compo being exported)
        is NOT yielded anywhere.

        Parameters
        ----------
        compo : rai.typing.CompoLike
            The compo or proxy to export.
        annotmap : TODO type
            Map of RAIMAD layer names to RAIMAD type annotations.
            Used for CIF Layer names, lyp properties.
            This gets composed with the layer annotations of each
            compo at each recursion step.

        Yields
        ------
        str
            Fragments of CIF code that can be joined together
            to form a complete CIF file.
            TODO windows CRLF??
        """

        # This clones annotmap and appends
        # values in new annotmap without overriding
        # existing ones
        #annotmap = {**compo.layers, **annotmap}

        #self.annotmap = {**compo.final().Layers, **self.annotmap}

        # Opening line, define the routine
        yield f'DS {self.rout_num} 1 1;\n'

        if self.experimental_cell_names:
            if experimental_cell_name:
                yield f'9 {experimental_cell_name};\n'
            # TODO L-edit doc says no duplicate cell names
            # but klayout supports it (adds `$1`, `$2`, `$3` and so on
            # to differentiate between them)
            # TODO what are the bounds on layer names?
            # no spaces it seems, but what else?

        # advance to next routine number
        self.rout_num += 1

        # Export all geometries
        for layer, geom in compo.geoms.items():

            # If a layer has been LMapp'ed to None,
            # that means the user wants it discarded. Skip.
            if layer is None:
                continue

            resolved_name = self._resolve_lname(
                compo,
                layer,
                )
            # TODO cache it???
            # TODO sit and think really hard about this --
            # can rai -> cif layer name change in one
            # compo export???

            assert rai.is_lname_valid(resolved_name)

            yield f'\tL {resolved_name};\n'
            for poly in geom:
                yield '\tP '
                for point in poly:
                    yield (
                        f'{int(point[0] * self.multiplier)} '
                        f'{int(point[1] * self.multiplier)} '
                        )
                yield ';\n'

        # Precompute a list of [routine number, subcomponent]
        # Remember, subcomponents can also have subcomponents,
        # so the subroutine numbers won't always be consecutive.
        # There's no way to know ahead of time,
        # you just have to generate each subcompo and keep track of
        # the routine number
        subcompos = []
        for subcompo_name, subcompo in compo.subcompos.items():

            if self.experimental_cell_names:
                experimental_cell_name = _experimental_compo_to_cell_name(
                    subcompo_name, subcompo)
            else:
                experimental_cell_name = None


            subcompos.append((
                self.rout_num,
                list(
                    self.yield_cif_bare(
                        subcompo,
                        experimental_cell_name,
                        #annotmap,
                        )
                    )
                ))

        # Call subcomponent procedures
        for i, _ in subcompos:
            yield f'\tC {i};\n'
        yield 'DF;\n'

        # Define those procedures
        for _, this_subcompo in subcompos:
            yield from this_subcompo

    def _resolve_lname(
            self,
            compo,
            layer,
            annotmap,
            ):

        if not self.ignore_annot_cif_name:
            if (annot_cif_name := annotmap.get(layer).cif_name) is not None:
                return annot_cif_name
                # TODO not validating that its valid here.
                # Are we validating it when creating annotation??

        if lname_policy == 'numeric':
            try:
                layer_index = self.layer_indices[layer]

            except KeyError:
                if len(self.layer_indices) >= 9999:
                    # TODO test this
                    raise RuntimeError(  # TODO custom exception class??
                        "Cannot generate numeric CIF layer name "
                        "because there are more than 9999 layers. "
                        "WHAT are you event doing!?!?!? "
                        )
                layer_index = len(self.layer_indices) + 1
                self.layer_indices[layer] = layer_index

            # TODO how does this play with layer order?? Annotations??

            return str(layer_index)

        if lname_policy == 'strict':
            raise CIFLayerNameWarning(
                f"Layer `{layer}` of component "
                f"`{compo}` is not annotated with a CIF-compatible layer name. "
                "Either add a CIF-compatible layer name using the `Layers` "
                "annotation class of your compo, or change the "
                "`lname_policy` of the CIF exporter to skip this error. "
                ,
                CIFLayerNameWarning
                )

        if lname_policy in {'klay', 'klay-warn'}:
            converted = rai.lname_to_klay(layer)

            if lname_policy == 'klay-warn':
                warn(
                    f"Layer name `{layer}` of component "
                    f"`{compo}` has been "
                    f"automatically converted to `{converted}`. "
                    "Either add a CIF-compatible layer name using the `Layers` "
                    "annotation class of your compo, or mute this warning "
                    "by passing `lname_policy='fallback-klay'` to the "
                    "CIF exporter."
                    ,
                    CIFLayerNameWarning
                )

            return converted
        
        else:
            raise ValueError(  # TODO custom exception class?
                "`lname_policy` must be one of "
                "'force-klay', 'fallback-klay', 'strict', 'fallback-klay-warn'."
                )

        # TODO what if raimad name HAPPENS to be cif-compatible?
        # Shouldn't happen because don't want ppl using
        # uppercase layer names, but what if they do??

        assert False

def _gen_lyp(annotmap):
    yield ''
    return

    # TODO not including a layer in lyp makes it
    # not show up at all???? Is this an issue??

    yield '<?xml version="1.0" encoding="utf-8"?>'
    yield '<layer-properties>'
    #yield from _lyp_pattern()

    for i, (full_name, annot) in enumerate(annotmap.items()):

        #yield ''.join(_dither_text(full_name))

        yield '<properties>'
        #yield '<expanded>false</expanded>'
        #yield '<frame-color>#00ffff</frame-color>'
        #yield '<fill-color>#00ffff</fill-color>'

        if fill_color := annot.lyp_fill_color:
            yield f'<fill-color>{fill_color}</fill-color>'

        if frame_color := annot.lyp_frame_color:
            yield f'<frame-color>{frame_color}</frame-color>'

        #yield '<frame-brightness>0</frame-brightness>'
        #yield '<fill-brightness>0</fill-brightness>'
        #yield '<dither-pattern>I9</dither-pattern>'

        #yield f'<dither-pattern>C{i}</dither-pattern>'

        #yield '<line-style/>'
        #yield '<valid>true</valid>'
        #yield '<visible>true</visible>'
        #yield '<transparent>false</transparent>'
        #yield '<width/>'
        #yield '<marked>false</marked>'
        #yield '<xfill>false</xfill>'
        #yield '<animation>0</animation>'

        #yield '<name/>'
        yield f'<name>{full_name}</name>'

        #yield '<source>CROT@1</source>'
        yield f'<source>{cif_name}</source>'

        yield '</properties>'

    yield '<name/>'
    yield '</layer-properties>'

# https://github.com/dhepper/font8x8/blob/master/font8x8_basic.h
FONT = (
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0000 (nul)
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0001
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0002
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0003
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0004
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0005
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0006
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0007
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0008
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0009
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+000A
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+000B
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+000C
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+000D
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+000E
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+000F
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0010
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0011
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0012
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0013
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0014
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0015
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0016
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0017
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0018
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0019
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+001A
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+001B
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+001C
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+001D
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+001E
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+001F
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0020 (space)
    ( 0x18, 0x3C, 0x3C, 0x18, 0x18, 0x00, 0x18, 0x00 ),   # U+0021 (!)
    ( 0x36, 0x36, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0022 (")
    ( 0x36, 0x36, 0x7F, 0x36, 0x7F, 0x36, 0x36, 0x00 ),   # U+0023 (#)
    ( 0x0C, 0x3E, 0x03, 0x1E, 0x30, 0x1F, 0x0C, 0x00 ),   # U+0024 ($)
    ( 0x00, 0x63, 0x33, 0x18, 0x0C, 0x66, 0x63, 0x00 ),   # U+0025 (%)
    ( 0x1C, 0x36, 0x1C, 0x6E, 0x3B, 0x33, 0x6E, 0x00 ),   # U+0026 (&)
    ( 0x06, 0x06, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0027 (')
    ( 0x18, 0x0C, 0x06, 0x06, 0x06, 0x0C, 0x18, 0x00 ),   # U+0028 (()
    ( 0x06, 0x0C, 0x18, 0x18, 0x18, 0x0C, 0x06, 0x00 ),   # U+0029 ())
    ( 0x00, 0x66, 0x3C, 0xFF, 0x3C, 0x66, 0x00, 0x00 ),   # U+002A (*)
    ( 0x00, 0x0C, 0x0C, 0x3F, 0x0C, 0x0C, 0x00, 0x00 ),   # U+002B (+)
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C, 0x06 ),   # U+002C (,)
    ( 0x00, 0x00, 0x00, 0x3F, 0x00, 0x00, 0x00, 0x00 ),   # U+002D (-)
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C, 0x00 ),   # U+002E (.)
    ( 0x60, 0x30, 0x18, 0x0C, 0x06, 0x03, 0x01, 0x00 ),   # U+002F (/)
    ( 0x3E, 0x63, 0x73, 0x7B, 0x6F, 0x67, 0x3E, 0x00 ),   # U+0030 (0)
    ( 0x0C, 0x0E, 0x0C, 0x0C, 0x0C, 0x0C, 0x3F, 0x00 ),   # U+0031 (1)
    ( 0x1E, 0x33, 0x30, 0x1C, 0x06, 0x33, 0x3F, 0x00 ),   # U+0032 (2)
    ( 0x1E, 0x33, 0x30, 0x1C, 0x30, 0x33, 0x1E, 0x00 ),   # U+0033 (3)
    ( 0x38, 0x3C, 0x36, 0x33, 0x7F, 0x30, 0x78, 0x00 ),   # U+0034 (4)
    ( 0x3F, 0x03, 0x1F, 0x30, 0x30, 0x33, 0x1E, 0x00 ),   # U+0035 (5)
    ( 0x1C, 0x06, 0x03, 0x1F, 0x33, 0x33, 0x1E, 0x00 ),   # U+0036 (6)
    ( 0x3F, 0x33, 0x30, 0x18, 0x0C, 0x0C, 0x0C, 0x00 ),   # U+0037 (7)
    ( 0x1E, 0x33, 0x33, 0x1E, 0x33, 0x33, 0x1E, 0x00 ),   # U+0038 (8)
    ( 0x1E, 0x33, 0x33, 0x3E, 0x30, 0x18, 0x0E, 0x00 ),   # U+0039 (9)
    ( 0x00, 0x0C, 0x0C, 0x00, 0x00, 0x0C, 0x0C, 0x00 ),   # U+003A (:)
    ( 0x00, 0x0C, 0x0C, 0x00, 0x00, 0x0C, 0x0C, 0x06 ),   # U+003B (;)
    ( 0x18, 0x0C, 0x06, 0x03, 0x06, 0x0C, 0x18, 0x00 ),   # U+003C (<)
    ( 0x00, 0x00, 0x3F, 0x00, 0x00, 0x3F, 0x00, 0x00 ),   # U+003D (=)
    ( 0x06, 0x0C, 0x18, 0x30, 0x18, 0x0C, 0x06, 0x00 ),   # U+003E (>)
    ( 0x1E, 0x33, 0x30, 0x18, 0x0C, 0x00, 0x0C, 0x00 ),   # U+003F (?)
    ( 0x3E, 0x63, 0x7B, 0x7B, 0x7B, 0x03, 0x1E, 0x00 ),   # U+0040 (@)
    ( 0x0C, 0x1E, 0x33, 0x33, 0x3F, 0x33, 0x33, 0x00 ),   # U+0041 (A)
    ( 0x3F, 0x66, 0x66, 0x3E, 0x66, 0x66, 0x3F, 0x00 ),   # U+0042 (B)
    ( 0x3C, 0x66, 0x03, 0x03, 0x03, 0x66, 0x3C, 0x00 ),   # U+0043 (C)
    ( 0x1F, 0x36, 0x66, 0x66, 0x66, 0x36, 0x1F, 0x00 ),   # U+0044 (D)
    ( 0x7F, 0x46, 0x16, 0x1E, 0x16, 0x46, 0x7F, 0x00 ),   # U+0045 (E)
    ( 0x7F, 0x46, 0x16, 0x1E, 0x16, 0x06, 0x0F, 0x00 ),   # U+0046 (F)
    ( 0x3C, 0x66, 0x03, 0x03, 0x73, 0x66, 0x7C, 0x00 ),   # U+0047 (G)
    ( 0x33, 0x33, 0x33, 0x3F, 0x33, 0x33, 0x33, 0x00 ),   # U+0048 (H)
    ( 0x1E, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x1E, 0x00 ),   # U+0049 (I)
    ( 0x78, 0x30, 0x30, 0x30, 0x33, 0x33, 0x1E, 0x00 ),   # U+004A (J)
    ( 0x67, 0x66, 0x36, 0x1E, 0x36, 0x66, 0x67, 0x00 ),   # U+004B (K)
    ( 0x0F, 0x06, 0x06, 0x06, 0x46, 0x66, 0x7F, 0x00 ),   # U+004C (L)
    ( 0x63, 0x77, 0x7F, 0x7F, 0x6B, 0x63, 0x63, 0x00 ),   # U+004D (M)
    ( 0x63, 0x67, 0x6F, 0x7B, 0x73, 0x63, 0x63, 0x00 ),   # U+004E (N)
    ( 0x1C, 0x36, 0x63, 0x63, 0x63, 0x36, 0x1C, 0x00 ),   # U+004F (O)
    ( 0x3F, 0x66, 0x66, 0x3E, 0x06, 0x06, 0x0F, 0x00 ),   # U+0050 (P)
    ( 0x1E, 0x33, 0x33, 0x33, 0x3B, 0x1E, 0x38, 0x00 ),   # U+0051 (Q)
    ( 0x3F, 0x66, 0x66, 0x3E, 0x36, 0x66, 0x67, 0x00 ),   # U+0052 (R)
    ( 0x1E, 0x33, 0x07, 0x0E, 0x38, 0x33, 0x1E, 0x00 ),   # U+0053 (S)
    ( 0x3F, 0x2D, 0x0C, 0x0C, 0x0C, 0x0C, 0x1E, 0x00 ),   # U+0054 (T)
    ( 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x3F, 0x00 ),   # U+0055 (U)
    ( 0x33, 0x33, 0x33, 0x33, 0x33, 0x1E, 0x0C, 0x00 ),   # U+0056 (V)
    ( 0x63, 0x63, 0x63, 0x6B, 0x7F, 0x77, 0x63, 0x00 ),   # U+0057 (W)
    ( 0x63, 0x63, 0x36, 0x1C, 0x1C, 0x36, 0x63, 0x00 ),   # U+0058 (X)
    ( 0x33, 0x33, 0x33, 0x1E, 0x0C, 0x0C, 0x1E, 0x00 ),   # U+0059 (Y)
    ( 0x7F, 0x63, 0x31, 0x18, 0x4C, 0x66, 0x7F, 0x00 ),   # U+005A (Z)
    ( 0x1E, 0x06, 0x06, 0x06, 0x06, 0x06, 0x1E, 0x00 ),   # U+005B ([)
    ( 0x03, 0x06, 0x0C, 0x18, 0x30, 0x60, 0x40, 0x00 ),   # U+005C (\)
    ( 0x1E, 0x18, 0x18, 0x18, 0x18, 0x18, 0x1E, 0x00 ),   # U+005D (])
    ( 0x08, 0x1C, 0x36, 0x63, 0x00, 0x00, 0x00, 0x00 ),   # U+005E (^)
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF ),   # U+005F (_)
    ( 0x0C, 0x0C, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+0060 (`)
    ( 0x00, 0x00, 0x1E, 0x30, 0x3E, 0x33, 0x6E, 0x00 ),   # U+0061 (a)
    ( 0x07, 0x06, 0x06, 0x3E, 0x66, 0x66, 0x3B, 0x00 ),   # U+0062 (b)
    ( 0x00, 0x00, 0x1E, 0x33, 0x03, 0x33, 0x1E, 0x00 ),   # U+0063 (c)
    ( 0x38, 0x30, 0x30, 0x3e, 0x33, 0x33, 0x6E, 0x00 ),   # U+0064 (d)
    ( 0x00, 0x00, 0x1E, 0x33, 0x3f, 0x03, 0x1E, 0x00 ),   # U+0065 (e)
    ( 0x1C, 0x36, 0x06, 0x0f, 0x06, 0x06, 0x0F, 0x00 ),   # U+0066 (f)
    ( 0x00, 0x00, 0x6E, 0x33, 0x33, 0x3E, 0x30, 0x1F ),   # U+0067 (g)
    ( 0x07, 0x06, 0x36, 0x6E, 0x66, 0x66, 0x67, 0x00 ),   # U+0068 (h)
    ( 0x0C, 0x00, 0x0E, 0x0C, 0x0C, 0x0C, 0x1E, 0x00 ),   # U+0069 (i)
    ( 0x30, 0x00, 0x30, 0x30, 0x30, 0x33, 0x33, 0x1E ),   # U+006A (j)
    ( 0x07, 0x06, 0x66, 0x36, 0x1E, 0x36, 0x67, 0x00 ),   # U+006B (k)
    ( 0x0E, 0x0C, 0x0C, 0x0C, 0x0C, 0x0C, 0x1E, 0x00 ),   # U+006C (l)
    ( 0x00, 0x00, 0x33, 0x7F, 0x7F, 0x6B, 0x63, 0x00 ),   # U+006D (m)
    ( 0x00, 0x00, 0x1F, 0x33, 0x33, 0x33, 0x33, 0x00 ),   # U+006E (n)
    ( 0x00, 0x00, 0x1E, 0x33, 0x33, 0x33, 0x1E, 0x00 ),   # U+006F (o)
    ( 0x00, 0x00, 0x3B, 0x66, 0x66, 0x3E, 0x06, 0x0F ),   # U+0070 (p)
    ( 0x00, 0x00, 0x6E, 0x33, 0x33, 0x3E, 0x30, 0x78 ),   # U+0071 (q)
    ( 0x00, 0x00, 0x3B, 0x6E, 0x66, 0x06, 0x0F, 0x00 ),   # U+0072 (r)
    ( 0x00, 0x00, 0x3E, 0x03, 0x1E, 0x30, 0x1F, 0x00 ),   # U+0073 (s)
    ( 0x08, 0x0C, 0x3E, 0x0C, 0x0C, 0x2C, 0x18, 0x00 ),   # U+0074 (t)
    ( 0x00, 0x00, 0x33, 0x33, 0x33, 0x33, 0x6E, 0x00 ),   # U+0075 (u)
    ( 0x00, 0x00, 0x33, 0x33, 0x33, 0x1E, 0x0C, 0x00 ),   # U+0076 (v)
    ( 0x00, 0x00, 0x63, 0x6B, 0x7F, 0x7F, 0x36, 0x00 ),   # U+0077 (w)
    ( 0x00, 0x00, 0x63, 0x36, 0x1C, 0x36, 0x63, 0x00 ),   # U+0078 (x)
    ( 0x00, 0x00, 0x33, 0x33, 0x33, 0x3E, 0x30, 0x1F ),   # U+0079 (y)
    ( 0x00, 0x00, 0x3F, 0x19, 0x0C, 0x26, 0x3F, 0x00 ),   # U+007A (z)
    ( 0x38, 0x0C, 0x0C, 0x07, 0x0C, 0x0C, 0x38, 0x00 ),   # U+007B ({)
    ( 0x18, 0x18, 0x18, 0x00, 0x18, 0x18, 0x18, 0x00 ),   # U+007C (|)
    ( 0x07, 0x0C, 0x0C, 0x38, 0x0C, 0x0C, 0x07, 0x00 ),   # U+007D (})
    ( 0x6E, 0x3B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+007E (~)
    ( 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ),   # U+007F
    )

def _dither_text(text):
    yield '<custom-dither-pattern>\n'
    yield '<pattern>\n'

    pattern = [['.'] * 32 for _ in range(32)]
    for crow in range(4):
        for ccol, char in enumerate(text[crow * 4:(crow + 1)*4]):
            lines = FONT[ord(char)]
            for row, line in enumerate(lines):
                for col in range(8):
                    print(row, col)
                    pattern[crow * 8 + row][ccol * 8 + col] = ['.', '*'][bool(line & (1 << col))]

    for line in pattern:
        yield f'<line>{''.join(line)}</line>\n'

    yield '</pattern>\n'
    yield '<order>1</order>\n'
    yield '<name>Irregular</name>\n'
    yield '</custom-dither-pattern>\n'

def _lyp_pattern():
    yield '<custom-dither-pattern>'
    yield '<pattern>'
    yield '<line>.......................*........</line>'
    yield '<line>...**..................*........</line>'
    yield '<line>.......................**.......</line>'
    yield '<line>..*.....................*******.</line>'
    yield '<line>...............*..............*.</line>'
    yield '<line>*..........*****..............*.</line>'
    yield '<line>*........*.....*..............*.</line>'
    yield '<line>*.....*.......*...............*.</line>'
    yield '<line>*****.........*...............*.</line>'
    yield '<line>..............................*.</line>'
    yield '<line>............*.....*****.......**</line>'
    yield '<line>...........*.....**...*.........</line>'
    yield '<line>..........*.....**....*.........</line>'
    yield '<line>.........*...........*..........</line>'
    yield '<line>.......*......*......*..........</line>'
    yield '<line>......*.....**..................</line>'
    yield '<line>.......*..*........*............</line>'
    yield '<line>*......****........*....*.......</line>'
    yield '<line>*......**........*.....**.......</line>'
    yield '<line>**.....................**.......</line>'
    yield '<line>.****..........*......***.......</line>'
    yield '<line>......***....**.....*...*.......</line>'
    yield '<line>.......**....*......*...*.......</line>'
    yield '<line>.......*.....*....*.....*.......</line>'
    yield '<line>.......*.....****......*........</line>'
    yield '<line>......*.......**................</line>'
    yield '<line>.....*................*.........</line>'
    yield '<line>.....*................*..**.....</line>'
    yield '<line>....*.................*****.....</line>'
    yield '<line>....**....................*.....</line>'
    yield '<line>.....******...............*.....</line>'
    yield '<line>..........**....................</line>'
    yield '</pattern>'
    yield '<order>1</order>'
    yield '<name>Irregular</name>'
    yield '</custom-dither-pattern>'

def _experimental_compo_to_cell_name(subcompo_name, subcompo):
    if isinstance(subcompo_name, int):
        instance_name = f'{subcompo_name}-ANON'
    elif isinstance(subcompo_name, str):
        instance_name = subcompo_name
    else:
        assert False

    type_name = type(subcompo.final()).__name__

    return f"{type_name}::{instance_name}"

