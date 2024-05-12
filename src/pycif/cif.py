from typing import Generator, Self, Type
from types import TracebackType
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
class CIFCommand():
    """
    Concrete CIF command.
    This is simply a wrapper for a string that also keeps track
    of what subroutine it corresponds to.
    """
    caller: int
    string: str

    def __str__(self) -> str:
        return self.string

    @classmethod
    def polygon(
            cls,
            caller: int,
            exporter: 'CIFExporter',
            points: pc.typing.Poly
            ) -> Self:

        return cls(caller, ''.join((
            '\t' * exporter.indent_depth,
            'P ',
            *(
                f'{int(coordinate * exporter.multiplier)} '
                for point in points
                for coordinate in point
                ),
            ';\n'
            )))

    @classmethod
    def layer_switch(
            cls,
            caller: int,
            exporter: 'CIFExporter',
            layer_name: str
            ) -> Self:

        return cls(caller, ''.join((
            '\t' * exporter.indent_depth,
            f'L {layer_name}',
            ';\n'
            )))

    @classmethod
    def comment(
            cls,
            caller: int,
            exporter: 'CIFExporter',
            comment_text: str
            ) -> Self:

        return cls(caller, ''.join((
            '\t' * exporter.indent_depth,
            f'({comment_text})',
            '\n'
            )))

    @classmethod
    def routine_call(
            cls,
            caller: int,
            exporter: 'CIFExporter',
            routine_num: int
            ) -> Self:

        return cls(caller, ''.join((
            '\t' * exporter.indent_depth,
            f'C {routine_num}',
            ';\n'
            )))

    @classmethod
    def routine_start(
            cls,
            exporter: 'CIFExporter',
            routine_num: int
            ) -> Self:

        return cls(routine_num, ''.join((
            '\t' * exporter.indent_depth,
            f'DS {routine_num}',
            ';\n'
            )))

    @classmethod
    def routine_finish(
            cls,
            exporter: 'CIFExporter',
            routine_num: int
            ) -> Self:

        return cls(routine_num, ''.join((
            '\t' * exporter.indent_depth,
            'DF',
            ';\n'
            )))

    @classmethod
    def end(cls) -> Self:
        return cls(-1, 'E\n')

@dataclass
class DelayedCall():
    """
    A CIF subroutine call, except we haven't defined the
    callee yet, so we don't know it's number.
    During subsequent passes,
    the subroutine gets defined and this gets replaced
    with a real CIFCommand.
    """
    caller: int
    index: int
    proxy: pc.Proxy


Edge = namedtuple('Edge', ("caller", "callee"))

class SubroutineContext:
    """
    Context manager for CIF subroutines.
    It's in charge of incrementing exporter.indent_depth,
    (which is probably a little overkill, since there are only
    two indent levels).
    writing the `DS` and `DF` commands,
    and making sure we don't accidentally open a new subroutine
    definition
    before the previous one is closed
    (if that happens, something has gone horribly wrong).
    """
    exporter: 'CIFExporter'
    rout_num: int

    def __init__(self, exporter: 'CIFExporter') -> None:
        self.exporter = exporter
        self.rout_num = -2

    def __enter__(self) -> Self:
        assert not self.exporter._is_inside_subroutine, \
            "Tried to define a new subroutine before the previous one " \
            "was finished."

        self.exporter._is_inside_subroutine = True
        self.exporter.indent_depth += 1
        self.rout_num = self.exporter.rout_num
        self.exporter.rout_num += 1

        self.exporter.cif_commands.append(
            CIFCommand.routine_start(self.exporter, self.rout_num)
            )

        return self

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_value: BaseException | None,
            exc_tb: TracebackType | None
            ) -> None:

        if exc_value is not None:
            # If there's an exception, raise it immediately.
            return

        assert self.exporter._is_inside_subroutine, \
            "Tried to finish a subroutine definition " \
            "before one was opened...? " \
            "How on earth did that happen!?"

        self.exporter._is_inside_subroutine = False
        self.exporter.indent_depth -= 1
        assert self.exporter.indent_depth >= 0

        self.exporter.cif_commands.append(
            CIFCommand.routine_finish(self.exporter, self.rout_num)
            )

# TODO native_inline must imply cif_native!!
# TODO native_inline is broken?
# TODO stacked proxies lose subcompo names?
class CIFExporter:
    multiplier: float = 1e3
    rot_multiplier: float = 1e3

    compo: pc.typing.Compo
    rout_num: int
    cif_native: bool
    flatten_proxies: bool
    native_inline: bool
    transform_fatal: bool

    ident_depth: int
    _is_inside_subroutine: bool
    cif_commands: list[CIFCommand]
    cif_string: str
    _delayed_call_queue: list[DelayedCall]

    compo2rout: dict[pc.typing.Compo, int]

    def __init__(
            self,
            compo: pc.typing.Compo,
            multiplier: float = 1e3,
            rot_multiplier: float = 1e3,
            cif_native: bool = True,
            flatten_proxies: bool = False,
            native_inline: bool = True,
            transform_fatal: bool = False,
            ) -> None:

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

        self.indent_depth = 0
        self._is_inside_subroutine = False
        self.cif_commands = []
        self.cif_string = ''
        self._delayed_call_queue = []

        # these are used during the export process
        self.compo2rout = {}  # Map proxy/compo to routine numbers

        # these are only for introspection or self.as_dot()
        #self.rout2compo = {}  # Map routine numbers to proxy/compo
        #self.edges = []  # List of `Edge`
        #self.rout2name = {}  # Map routine numbers to names
        #self._rout2cif = {}  # Map routine numbers to corresponding CIF code
        #self.rout2cif = {}
        #self.invalid_transforms = []

        self._export_cif()

        #self.rout2cif = {
        #    rout_num: ''.join(fragments)
        #    for rout_num, fragments in self._rout2cif.items()
        #    }

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
        self._realize_compo(self.compo)

        while self._delayed_call_queue:
            self._do_pass()

        self._finalize()
        self.cif_string = ''.join(map(str, self.cif_commands))

    def _do_pass(self) -> None:
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

        offset = 0
        for delayed_call in self._delayed_call_queue:
            realized = self._realize_delayed_call(delayed_call)
            self.cif_commands.insert(delayed_call.index + offset, realized)
            offset += 1

        self._delayed_call_queue.clear()

    def _realize_delayed_call(self, call: DelayedCall) -> CIFCommand:
        try:
            compiled_transform = self.compile_transform(call.proxy.transform)

        except CannotCompileTransformError as err:
            compiled_transform = None

        flat_lmap = call.proxy.get_flat_lmap()

        # TODO standardized inspection for lmap
        if (
                flat_lmap is None
                and
                compiled_transform is not None
                ):
            # We can represent `above` proxy as a CIF subroutine call

            target_rout = self.compo2rout.get(call.proxy.compo)
            if target_rout is None:
                # We haven't made a subroutine that corresponds to `below` yet,
                # have to do that now.
                target_rout = self._realize_compo(call.proxy.compo)

        else:
            # we can't represent `above` as a CIF
            # subroutine call, so we must steamroll `below`
            target_rout = self._steamroll(call.caller, call.proxy)

        return CIFCommand.routine_call(call.caller, self, target_rout)

    def _realize_compo(self, compo: pc.typing.Compo) -> int:

        if isinstance(compo, pc.Compo):
            return self._realize_real_compo(compo)

        elif isinstance(compo, pc.Proxy):
            return self._realize_proxy(compo)

        else:
            assert False

    def _realize_real_compo(self, compo: pc.typing.RealCompo) -> int:
        with SubroutineContext(self) as this_rout:
            for name, subcompo in compo.subcompos.items():
                # TODO store name
                self._delayed_call_queue.append(
                    DelayedCall(
                        this_rout.rout_num,
                        len(self.cif_commands),
                        subcompo
                        )
                    )

            self._make_geoms(this_rout.rout_num, compo.geoms)

        return this_rout.rout_num

    def _realize_proxy(self, proxy: pc.typing.Proxy) -> int:
        with SubroutineContext(self) as this_rout:
            target_rout = self.compo2rout.get(proxy.compo)
            if target_rout is None:
                target_rout = self._realize_compo(proxy.compo)
        # TODO is this correct? We want to be depth-first here?
        return this_rout.rout_num
        #return CIFCommand.routine_call(this_rout.rout_num, self, target_rout)

    def _steamroll(self, caller: int, compo: pc.typing.Compo) -> int:
        """
        Export a compo into a CIF file with no subroutines.
        This function can be used independently,
        as well as a part of CIFExporter to steamroll
        compos with unCIFable transforms.
        """
        with SubroutineContext(self) as this_rout:
            self.cif_commands.append(
                CIFCommand.comment(this_rout.rout_num, self, 'steamrolled')
                )
            self._make_geoms(this_rout.rout_num, compo.steamroll())
        return this_rout.rout_num

    def _make_geoms(self, caller: int, geoms: pc.typing.Geoms) -> None:
        """
        return the direct geometries of a compo as CIF polygons,
        with the appropriate layer switches.
        """
        for layer_name, layer_geoms in geoms.items():

            self.cif_commands.append(
                CIFCommand.layer_switch(caller, self, f"L{layer_name}")
                )

            for points in layer_geoms:

                self.cif_commands.append(
                    CIFCommand.polygon(caller, self, points)
                    )

    def _finalize(self) -> None:
        """
        This finalizes the CIF file by calling subroutine 1
        (which corresponds to the toplevel compo)
        at the very end of the CIF file.
        """
        self.cif_commands.append(CIFCommand.routine_call(-1, self, 1))
        self.cif_commands.append(CIFCommand.end())

    @pc.join_generator('')
    def compile_transform(
            self,
            transform: pc.typing.Transform,
            ) -> Generator[str, None, None]:

        if transform.does_scale():
            # TODO also possible to mirror in cif
            raise CannotCompileTransformError(
                f"Cannot compile {transform} to CIF "
                "because it scales."
                )

        if transform.does_shear():
            raise CannotCompileTransformError(
                f"Cannot compile {transform} to CIF "
                "because it shears."
                )

        # TODO order matters here! rotation before translation
        # Not a syntax thing, just transform.get_rotation is around
        # origin

        if transform.does_rotate():
            yield from self.compile_rotation(transform.get_rotation())

        if transform.does_translate():
            yield from self.compile_translation(*transform.get_translation())

    def compile_rotation(
            self,
            rotation: float,
            ) -> Generator[str, None, None]:
        yield 'R '
        yield str(int(np.cos(rotation) * self.rot_multiplier))
        yield ' '
        yield str(int(np.sin(rotation) * self.rot_multiplier))
        yield ' '

    def compile_translation(
            self,
            move_x: float,
            move_y: float,
            ) -> Generator[str, None, None]:
        yield 'T '
        yield str(int(move_x * self.multiplier))
        yield ' '
        yield str(int(move_y * self.multiplier))
        yield ' '

def export_cif(
        compo: pc.typing.Compo,
        multiplier: float = 1e3,
        rot_multiplier: float = 1e3,
        cif_native: bool = True,
        flatten_proxies: bool = False,
        native_inline: bool = True,
        transform_fatal: bool = False,
        ) -> str:
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



