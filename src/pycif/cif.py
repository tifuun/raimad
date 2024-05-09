from dataclasses import dataclass
from collections import namedtuple

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
    rout_caller: int
    name: str | None = None


Edge = namedtuple('Edge', ("caller", "callee"))

class SubroutineContext:
    """
    Context manager for CIF subroutines.
    It's in charge of incrementing exporter.indent_depth,
    writing the `DS` and `DF` commands,
    and making sure we don't accidentally open a new subroutine
    definition
    before the previous one is closed
    (if that happens, something has gone horribly wrong).
    """
    def __init__(self, exporter, rout_num):
        self.exporter = exporter
        self.rout_num = rout_num

    def __enter__(self):
        assert not self.exporter._is_inside_subroutine, \
            "Tried to define a new subroutine before the previous one " \
            "was finished."

        self.exporter._is_inside_subroutine = True
        self.exporter.indent_depth += 1
        self.exporter._append(
            f"{'\t' * self.exporter.indent_depth}DS {self.rout_num} 1 1;\n",
            self.rout_num
            )

    def __exit__(self, exc_type, exc_value, exc_tb):

        if exc_value is not None:
            # If there's an exception, raise it immediately.
            return False

        assert self.exporter._is_inside_subroutine, \
            "Tried to finish a subroutine definition " \
            "before one was opened...? " \
            "How on earth did that happen!?"

        self.exporter._is_inside_subroutine = False

        self.exporter.indent_depth -= 1
        assert self.exporter.indent_depth >= 0
        self.exporter._append(
            f"{'\t' * self.exporter.indent_depth}DF;\n",
            self.rout_num
            )

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
        self.indent_depth = 0
        self._is_inside_subroutine = False
        self.cif_string = ''

        self.compo2rout = {}  # Map proxy/compo to routine numbers
        self.rout2compo = {}  # Map routine numbers to proxy/compo
        self.edges = []  # List of `Edge`
        self.rout2name = {}  # Map routine numbers to names
        self._rout2cif = {}  # Map routine numbers to corresponding CIF code
        self.rout2cif = {}
        self.invalid_transforms = []

        self._export_cif()

        self.rout2cif = {
            rout_num: ''.join(fragments)
            for rout_num, fragments in self._rout2cif.items()
            }

        # TODO there is currently a thing I don't like:
        # the CIF code is stored in two places at once,
        # self.cif_fragments and self.rout2cif.
        # There should be only one primary place, and the other one
        # deriving from it.
        # Should self.cif_fragments keep track of which fragment
        # belongs to which rout, and self.cif2rout be assembled later?
        # Or maybe the other way around, like in the below code?
        #
        # self.cif_string = ''.join((
        #     *(
        #         rout_code
        #         for rout_num, rout_code in self.rout2cif.items()
        #         if rout_num >= 0
        #         ),
        #     self.rout2cif[-1]
        #     ))

    def _subroutine(self, rout_num):
        return SubroutineContext(self, rout_num)

    @pc.join_generator('')
    def _call_routine(self, number, transform=''):
        yield '\t' * self.indent_depth
        yield 'C '
        yield str(number)

        if transform:
            yield ' '
            yield transform

        yield ';\n'

    @pc.join_generator('')
    def _make_poly(self, xyarray):
        yield '\t' * self.indent_depth
        yield 'P '
        for point in xyarray:
            for coordinate in point:
                yield f'{int(coordinate * self.multiplier)} '
        yield ';\n'

    @pc.join_generator('')
    def _switch_layer(self, layer_name):
        yield '\t' * self.indent_depth
        yield f'L L{layer_name};\n'

    @pc.join_generator('')
    def _comment(self, comment_text):
        yield '\t' * self.indent_depth
        yield f'({comment_text})\n'

    @pc.join_generator('')
    def _make_geoms(self, geoms):
        """
        return the direct geometries of a compo as CIF polygons,
        with the appropriate layer switches.
        """
        for layer_name, layer_geoms in geoms.items():
            yield self._switch_layer(layer_name)
            for xyarray in layer_geoms:
                yield self._make_poly(xyarray)

    def _append(self, cif_string, rout):
        self.cif_fragments.append(cif_string)

        assert rout in self._rout2cif.keys(), \
            f"_rout2cif[{rout}] should have been created earlier."

        self._rout2cif[rout].append(cif_string)

    @pc.join_generator('')
    def _steamroll(self, compo, transform) -> str:
        """
        Export a compo into a CIF file with no subroutines.
        This function can be used independently,
        as well as a part of CIFExporter to steamroll
        compos with unCIFable transforms.
        """
        # This proxy is used to combine `compo`'s
        # transform with the explicitly specified `transform`.
        proxy = pc.Proxy(compo, transform=transform)

        yield self._comment('flat')
        yield self._make_geoms(proxy.steamroll())

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

        rout_callee = (
            self.compo2rout.get(call.compo, None)
            or
            self._make_compo(call.compo)
        )

        rout_call = self._call_routine(rout_callee, compiled_transform)

        self.edges.append(Edge(call.rout_caller, rout_callee))
        self.rout2name[rout_callee] = call.name

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

            realized_call: str = self._realize_delayed_rout_call(fragment)
            self.cif_fragments[i] = realized_call

            # TODO this horrible monstrosity finds the delayed routine
            # in self._rout2cif and replaces it with the realized call.
            # This is as ugly as it is inefficient.
            (
                f := self._rout2cif[fragment.rout_caller]
                )[f.index(fragment)] = realized_call

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

    def _delayed(self, compo, transform, rout_caller, name=None):
        fragment = DelayedRoutCall(compo, transform, rout_caller, name)
        self.cif_fragments.append(fragment)

        assert rout_caller in self._rout2cif.keys(), \
            f"_rout2cif[{rout_caller}] should have been created earlier."

        self._rout2cif[rout_caller].append(fragment)

    def _call_root(self) -> None:
        """
        This finalizes the CIF file by calling subroutine 1
        (which corresponds to the toplevel compo)
        at the very end of the CIF file.
        """
        self._rout2cif[-1] = []
        self._append('C 1;\n', -1)
        self._append('E', -1)

    def _make_compo(self, compo):
        rout_num = self.rout_num
        self.rout_num += 1
        self.compo2rout[compo] = rout_num
        self.rout2compo[rout_num] = compo
        self._rout2cif[rout_num] = []

        if isinstance(compo, pc.Proxy):
            with self._subroutine(rout_num):
                if self.native_inline:
                    # This branch only ever happens if flatten_proxies is off,
                    # but native_inline is on.... I think
                    assert not self.flatten_proxies, \
                        "Wait, how did we get here again...?"

                    did_make_inline = self._actually_make_compo(
                        compo.final(),
                        rout_num,
                        compo.get_flat_transform()
                        )

                if not self.native_inline or not did_make_inline:
                    self._delayed(compo.compo, compo.transform, rout_num)

        else:
            # TODO this is bad, use a context manager or something
            with self._subroutine(rout_num):
                self._actually_make_compo(compo, rout_num)

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

                self._append(native_inline, rout_num)
                return True

            native = compo._export_cif(self)
            if native is not NotImplemented:
                self._append(native, rout_num)
                return True

        self._append(self._make_geoms(compo.geoms), rout_num)

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
            compo = self.rout2compo[rout_num]

            label = []
            if include_meta:
                label.append(f'Cell {rout_num}')

            if isinstance(compo, pc.Proxy):
                shape = 'note'
                if include_name:
                    if (name := self.rout2name.get(rout_num)):
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
                    self.rout2cif[rout_num]
                    ]).rstrip(r'\l'))

            label = r'\l'.join(label)

            yield f'\t{rout_num} [shape={shape} label="{label}\\l"];\n'

        for from_, to in self.edges:
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



