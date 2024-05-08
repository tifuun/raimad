from dataclasses import dataclass

import numpy as np

import pycif as pc

class CIFExportError(Exception):
    """
    Generic CIF export error.
    This is an abstract base class for all other CIF export errors.
    """

class CannotCompileTransformError(CIFExportError):
    """
    This error is raised when it's impossible to compile
    a RAIMAD Transform into a CIF transform.
    RAIMAD transforms are affine transforms;
    that is, they support rotation, scaling, shearing, and translation.
    CIF only supports rotation and translation.

    When using CIFExporter with `transform_fatal=False`,
    this error is caught internally,
    and the offending transform is "baked into"
    its corresponding compo.
    When `transform_fatal=True`,
    this error is emitted and the export process stops.
    """

@dataclass
class DelayedRoutCall():
    """
    Delayed subroutine call.
    When a compo contains a subcompo that has not been exported
    yet (does not have a CIF subroutine that corresponds to it),
    the CIFExporter emmits a `DelayedRoutCall`
    that keeps track of the subcompo,
    the transform of that subcompo in relation to the parent compo,
    the subroutine number of the parent compo,
    and the name of the subcompo.
    During subsequent passes,
    the CIFExporter sees the DelayedRoutCall,
    generates the needed subroutine,
    and replaces the DelayedRoutCall with an actually CIF subroutine call.
    """
    compo: pc.Proxy
    transform: pc.Transform
    rout_num: int
    name: str | None = None

# TODO native_inline must imply cif_native!!
# TODO native_inline is broken?
# TODO stacked proxies lose subcompo names?
class CIFExporter:
    multiplier: float = 1e3
    rot_multiplier: float = 1e3

    def __init__(
            self,
            compo,
            multiplier=None,
            rot_multiplier=None,
            cif_native=False,
            flatten_proxies=False,
            native_inline=False,
            transform_fatal: bool = False
            ):

        self.compo = compo
        self.rout_num = 1
        if multiplier is not None:
            self.multiplier = multiplier
        if rot_multiplier is not None:
            self.rot_multiplier = rot_multiplier
        self.cif_native = cif_native
        self.flatten_proxies = flatten_proxies
        self.native_inline = native_inline
        self.transform_fatal = transform_fatal

        self.cif_fragments = []

        # map proxy/compo objects to routine numbers
        self.rout_map = {}
        # map routine numbers to oroxy/compo objects
        self.reverse_rout_map = {}

        # list of (caller, callee) that shows which
        # cif routine calls which routines
        self.rout_list = list()

        self.rout_names = {}

        # Map routine numbers to lists of cif fragments
        self.cif_map = {}

        # The resulting cif file
        self.cif_string = ''

        # list of transforms that could not be compiled
        self.invalid_transforms = []

        self._export_cif()

    @pc.join_generator('')
    def _steamroll(self, compo, transform) -> str:
        """
        Export a compo into a CIF file with no subroutines.
        This function can be used independently,
        as well as a part of CIFExporter to steamroll
        compos with unCIFable transforms.
        """
        indt = '\t' * 1  # TODO indent_depth
        proxy = pc.Proxy(compo, transform=transform)

        for layer_name, layer_geoms in proxy.steamroll().items():
            yield f'{indt}(flat)\n'
            yield f'{indt}L L{layer_name};\n'
            for xyarray in layer_geoms:
                yield f'{indt}P '
                for point in xyarray:
                    for coordinate in point:
                        yield f'{int(coordinate * self.multiplier)} '
                yield ';\n'

    def _realize_delayed_rout_call(self, call: DelayedRoutCall) -> str:
        """
        This function takes a DelayedRoutCall and converts it
        to an actual CIF subroutine call string.

        :param call: the DelayedRoutCall to realize
        :returns: a string with the CIF subroutine call.
        :raises: `CannotCompileTransformError`
        """
        compiled_transform = self.compile_transform(
            call.compo.get_flat_transform()
            .compose(
                call.transform
                )
            )

        if compiled_transform is None:
            self.invalid_transforms.append('TODO')
            return self._steamroll(call.compo, call.transform)

        rout_num = (
            self.rout_map.get(call.compo, None)
            or
            self._make_compo(call.compo)
        )

        rout_call = ''.join((
            f'\tC {rout_num} ',
            compiled_transform,
            ";\n"
            ))

        if call.rout_num not in self.cif_map.keys():
            # TODO defaultdict?
            self.cif_map[call.rout_num] = []

        self.cif_map[call.rout_num][
            self.cif_map[call.rout_num].index(call)
            #] = f'\t C {rout_num} [...];\n'
            ] = rout_call  # TODO!!!
        # TODO the above line is a mess

        self.rout_list.append((call.rout_num, rout_num))
        self.rout_names[rout_num] = call.name

        return rout_call

    def _do_pass(self) -> int:
        """
        Run one pass of the CIF export process.
        During each pass, the exporter scans for `DelayedRoutCall`s
        and replaces them with actual CIF subroutine calls.

        :returns: the number of new routines generated in this pass.
            If there are zero new routines, that means that no more passes
            are necessary, and you can move on to finalizing the CIF file.
        :raises: CannotCompileTransformError if CIFExporter was initialized
            with `transform_fatal` and a transform was encountered that cannot
            be compiled to CIF.
        """
        new_compos: int = 0

        for i, fragment in enumerate(self.cif_fragments):
            if not isinstance(fragment, DelayedRoutCall):
                continue

            self.cif_fragments[i] = self._realize_delayed_rout_call(fragment)

            new_compos += 1

        return new_compos

    def _export_cif(self) -> None:
        """
        This is the main entrypoint for CIFExporter.
        This function makes the root compo,
        repeatedly calls `self._do_pass()` until no more DelayedRoutCalls
        are left,
        finalizes the CIF file,
        and saves the CIF string to `self.cif_string`.

        :returns: None. The output CIF string is stored to
            `self.cif_string`.
        :raises: A `CannotCompileTransformError` may be propagated
            from self._do_pass()
        """
        self._make_compo(self.compo)

        while self._do_pass() > 0:
            pass

        self._call_root()
        self.cif_string = ''.join(self.cif_fragments)

    def _frag(self, fragment, rout_num=None):
        self.cif_fragments.append(fragment)
        if rout_num is not None:
            self.cif_map[rout_num].append(fragment)

    def _delayed(self, compo, transform, rout_num, name=None):
        fragment = DelayedRoutCall(compo, transform, rout_num, name)
        self.cif_fragments.append(fragment)

        if rout_num not in self.cif_map.keys():
            # TODO defaultdict?
            self.cif_map[rout_num] = []
        self.cif_map[rout_num].append(fragment)

    def _call_root(self) -> None:
        """
        This finalizes the CIF file by calling subroutine 1
        (which corresponds to the toplevel compo)
        at the very end of the CIF file.
        """
        self._frag( 'C 1;\n' )
        self._frag( 'E' )

    def _make_compo(self, compo):
        rout_num = self.rout_num
        self.rout_num += 1
        self.rout_map[compo] = rout_num
        self.reverse_rout_map[rout_num] = compo
        self.cif_map[rout_num] = []

        if isinstance(compo, pc.Proxy):
            self._frag( f'DS {rout_num};\n', rout_num )

            if self.native_inline:
                # This branch only ever happens if flatten_proxies is off,
                # but native_inline is on.... I think
                did_make_inline = self._actually_make_compo(
                    compo.final(),
                    rout_num,
                    compo.get_flat_transform()
                    )

            if not self.native_inline or not did_make_inline:
                self._delayed(compo.compo, compo.transform, rout_num)

            self._frag( 'DF;\n', rout_num )

        else:
            # TODO this is bad, use a context manager or something
            self._frag( f'DS {rout_num} 1 1;\n', rout_num )
            self._actually_make_compo(compo, rout_num)
            self._frag( 'DF;\n', rout_num )

        return rout_num

    def _actually_make_compo(self, compo, rout_num, transform=None):
        """
        TODO better function name
        """
        assert isinstance(compo, pc.Compo)
        assert not isinstance(compo, pc.Proxy)
        if self.cif_native:
            if transform is not None:
                native_inline = compo._export_cif_transformed(self, transform)
                if native_inline is NotImplemented:
                    # TODO Bug here?
                    return False

                self._frag(native_inline, rout_num)
                return True

            native = compo._export_cif(self)
            if native is not NotImplemented:
                self._frag(native, rout_num)
                return True

        self._make_geometries(compo, rout_num)

        for name, proxy in compo.subcompos.items():
            if self.flatten_proxies:
                if self.native_inline:
                    did_make_inline = self._actually_make_compo(
                        proxy.final(),
                        rout_num,
                        proxy.get_flat_transform()
                        )

                if not self.native_inline or not did_make_inline:
                    self._delayed(
                        proxy.final(),
                        proxy.get_flat_transform(),
                        rout_num
                        )

            else:
                self._delayed(proxy, None, rout_num, name)

        return True

    def _make_geometries(self, compo, rout_num):
        """
        yield the direct geometries of a compo as CIF polygons,
        with the appropriate layer switches.
        """
        for layer, geom in compo.geoms.items():
            self._frag(f'\tL L{layer};\n', rout_num)
            for poly in geom:
                self._frag('\tP ', rout_num)
                for point in poly:
                    self._frag(
                        f'{int(point[0] * self.multiplier)} '
                        f'{int(point[1] * self.multiplier)} ',
                        rout_num
                        )
                #self.cif_map[rout_num].append('[...]')
                self._frag(';\n', rout_num)

    def compile_transform(self, transform):
        if transform is None:
            return ''

        if transform.does_scale():
            # TODO also possible to mirror in cif
            if not self.transform_fatal:
                return None

            raise CannotCompileTransformError(
                f"Cannot compile {transform} to CIF "
                "because it scales."
                )

        if transform.does_shear():
            if not self.transform_fatal:
                return None

            raise CannotCompileTransformError(
                f"Cannot compile {transform} to CIF "
                "because it shears."
                )

        # TODO order matters here! rotation before translation
        # Not a syntax thing, just transform.get_rotation is around
        # origin

        if transform.does_rotate():
            return self.compile_rotation(transform.get_rotation())

        if transform.does_translate():
            return self.compile_translation(*transform.get_translation())

        # Turns out this is an identity transform
        return ''

    @pc.join_generator('')
    def compile_rotation(self, rotation):
        yield 'R '
        yield str(int(np.cos(rotation) * self.rot_multiplier))
        yield ' '
        yield str(int(np.sin(rotation) * self.rot_multiplier))
        yield ' '

    @pc.join_generator('')
    def compile_translation(self, move_x, move_y):
        yield 'T '
        yield str(int(move_x * self.multiplier))
        yield ' '
        yield str(int(move_y * self.multiplier))
        yield ' '

    @pc.join_generator('', pc.gv.DOTString)
    def as_dot(self, include_code=True, include_meta=False, include_name=True):
        yield 'digraph D {\n'

        for rout_num in range(1, self.rout_num):
            compo = self.reverse_rout_map[rout_num]

            label = []
            if include_meta:
                label.append(f'Cell {rout_num}')

            if isinstance(compo, pc.Proxy):
                shape = 'note'
                if include_name:
                    if (name := self.rout_names.get(rout_num)):
                        label.append(rf'({name})')

                if include_meta:
                    if compo.transform.does_translate:
                        transl = compo.transform.get_translation()
                        label.append(f'Move {transl[0]:.3g}, {transl[1]:.3g}')

                    if compo.transform.does_rotate:
                        rot = pc.rad2deg(compo.transform.get_rotation())
                        label.append(f'Rotate {rot:.3g}')
            else:
                shape = 'box'
                if include_name:
                    # TODO this entire funtion is getting out of hand as well
                    label.append(rf'({type(compo).__name__})')

            if include_code:
                label.append(''.join([
                    line.replace('\n', r'\l').replace('\t', '    ')
                    for line in
                    self.cif_map[rout_num]
                    ]).rstrip(r'\l'))

            label = r'\l'.join(label)

            yield f'\t{rout_num} [shape={shape} label="{label}\\l"];\n'

        for from_, to in self.rout_list:
            yield f'\t{from_} -> {to};\n'

        yield '}\n'

def export_cif(
        compo,
        multiplier=1e3,
        rot_multiplier=1e3,
        cif_native=True,
        flatten_proxies=False,
        native_inline=True,
        transform_fatal=False,
        ):
    exporter = CIFExporter(
        compo,
        multiplier,
        rot_multiplier,
        cif_native,
        flatten_proxies,
        native_inline,
        transform_fatal,
        )
    return exporter.cif_string



