"""noreuse.py: home to the NoReuse CIF exporter."""

from typing import Iterator
from warnings import warn
from typing import TypeAlias, Literal

import raimad as rai

Cifmap: TypeAlias = dict[str, str | None]
LnamePolicy: TypeAlias = Literal[
    "fallback-klay-warn",
    "fallback-klay",
    "force-klay",
    "strict",
    ]

def _compo_to_cifmap(compo: rai.typing.CompoLike) -> Cifmap:
    return {
        lname: annot.cif_name for lname, annot in compo.final().Layers.items()
        if isinstance(lname, str)
        # TODO this `if` is some mypy trickery
        # because dictlist keys CAN be ints
        # but for Layers annotation that should never happen
        # but we still need a way to enforce that
        # both at runtime and with type hints
        }

def _resolve_lname(
        compo: rai.typing.CompoLike,
        layer: str,
        cifmap: Cifmap,
        lname_policy: LnamePolicy
        ) -> str:

    resolved = cifmap.get(layer) or layer
    converted = rai.lname_to_klay(layer)

    if lname_policy == 'fallback-klay-warn':
        if rai.is_lname_valid(resolved):
            return resolved

        warn(
            f"Layer name `{resolved}` of component "
            f"`{compo}` is not a valid CIF layer name. "
            f"It is automatically converted to `{converted}`. "
            "Either add a CIF-compatible layer name using the `Layers` "
            "annotation class of your compo, or mute this warning "
            "by passing `lname_policy='fallback-klay'` to the "
            "CIF exporter."
            ,
            CIFLayerNameWarning
            )

        return converted

    elif lname_policy == 'strict':
        if rai.is_lname_valid(resolved):
            return resolved

        raise CIFLayerNameWarning(
            f"Layer name `{resolved}` of component "
            f"`{compo}` is not a valid CIF layer name. "
            "Either add a CIF-compatible layer name using the `Layers` "
            "annotation class of your compo, or change the "
            "`lname_policy` of the CIF exporter to skip this error. "
            ,
            CIFLayerNameWarning
            )

    elif lname_policy == 'fallback-klay':
        if rai.is_lname_valid(resolved):
            return resolved
        return converted

    elif lname_policy == 'force-klay':
        return converted

    else:
        raise ValueError(
            "`lname_policy` must be one of "
            "'force-klay', 'fallback-klay', 'strict', 'fallback-klay-warn'."
            )
    
    assert False

class CIFLayerNameWarning(UserWarning):
    """Warning about layer names that are not compatible with CIF."""

class NoReuse:
    """CIF Exporter that doesn't reuse subroutines."""

    def __init__(
            self,
            compo: 'rai.typing.CompoLike',
            multiplier: float = 1e2,
            lname_policy: LnamePolicy = 'fallback-klay-warn',
            ) -> None:

        self.compo = compo
        self.rout_num = 1
        self.multiplier = multiplier
        self.lname_policy = lname_policy

        self.cifmap: Cifmap = {}

        self.cif_string = self._export_cif()

        # TODO validate lname policy

    def _export_cif(self) -> str:
        return ''.join(self._yield_cif())

    def _yield_cif(self) -> Iterator[str]:
        """Yield lines of cif file."""
        first_rout = self.rout_num
        yield from self.yield_cif_bare(
            self.compo,
            {},
            nickname=type(self.compo.final()).__name__
            )
        yield f'C {first_rout};\n'
        yield 'E'

    def yield_cif_bare(
            self,
            compo: 'rai.typing.CompoLike',
            cifmap: Cifmap,
            nickname: str | None = None,
            #subcompo_name_stack = None
            ) -> Iterator[str]:
        """Yield lines of CIF of a particular component, without calling it."""

        # This clones cifmap and appends
        # values in new cifmap without overriding
        # existing ones
        cifmap = {**_compo_to_cifmap(compo), **cifmap}

        # Opening line, define the routine
        yield f'DS {self.rout_num} 1 1;\n'

        if nickname is not None:
            #assert bool(nickname)
            if not nickname:
                warn(
                        "Empty cell nicname????",
                        UserWarning
                        )
                nickname = 'EMPTY'
            # TODO L-name doc says no duplicate cell names
            # but klayout supports it (adds `$1`, `$2`, `$3` and so on
            # to differentiate between them)
            # TODO what are the bounds on layer names?
            # no spaces it seems, but what else?
            yield f'9 {nickname};\n'

        # advance to next routine number
        self.rout_num += 1

        # Export all geometries
        for layer, geom in compo.geoms.items():

            # If a layer has been LMapp'ed to None,
            # that means the user wants it discarded. Skip.
            if layer is None:
                continue

            resolved_name = _resolve_lname(
                compo, layer, cifmap, self.lname_policy)

            yield f'\tL {resolved_name};\n'
            for poly in geom:
                yield '\tP '
                for point in poly:
                    yield (
                        f'{int(point[0] * self.multiplier)} '
                        f'{int(point[1] * self.multiplier)} '
                        )
                yield ';\n'

        for mark_name, mark in compo.marks.items():
            yield (
                'L MARK;\n'
                f'94 {mark_name} '
                f'{int(mark[0] * self.multiplier)} '
                f'{int(mark[1] * self.multiplier)};\n'
                )

        # Precompute a list of [routine number, subcomponent]
        # Remember, subcomponents can also have subcomponents,
        # so the subroutine numbers won't always be consecutive.
        # There's no way to know ahead of time,
        # you just have to generate each subcompo and keep track of
        # the routine number
        subcompos = []
        for subcompo_name, subcompo in compo.subcompos.items():

            if isinstance(subcompo_name, int):
                instance_name = f'{subcompo_name}-ANON'
            elif isinstance(subcompo_name, str):
                instance_name = subcompo_name
            else:
                assert False

            #if subcompo_name_stack is None:
            #    subcompo_name_stack = ()

            #subcompo_name_stack = (*subcompo_name_stack, instance_name)
            #instance_name = '.'.join((*subcompo_name_stack, instance_name))

            type_name = type(subcompo.final()).__name__

            subcompos.append((
                self.rout_num,
                list(
                    self.yield_cif_bare(
                        subcompo,
                        cifmap,
                        #nickname=f"{type_name}::{'.'.join(subcompo_name_stack)}{'.' * bool(subcompo_name_stack)}{instance_name}",
                        nickname=f"{type_name}::{instance_name}",
                        #subcompo_name_stack=(*subcompo_name_stack, instance_name),
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

