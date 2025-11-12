"""noreuse.py: home to the NoReuse CIF exporter."""

from typing import Iterator
from warnings import warn

import raimad as rai

def _compo_to_cifmap(compo: rai.Proxy):
    return {
        lname: annot.cif_name for lname, annot in compo.final().Layers.items()
        }

def _resolve_lname(compo: rai.Proxy, layer, cifmap, lname_policy):

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
    pass

class NoReuse:
    """CIF Exporter that doesn't reuse subroutines."""

    def __init__(
            self,
            compo: 'rai.typing.CompoLike',
            multiplier: float = 1e3,
            lname_policy = 'fallback-klay-warn',
            ) -> None:

        self.compo = compo
        self.rout_num = 1
        self.multiplier = multiplier
        self.lname_policy = lname_policy

        self.cifmap = {}

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
            )
        yield f'C {first_rout};\n'
        yield 'E'

    def yield_cif_bare(
            self,
            compo: 'rai.typing.CompoLike',
            cifmap: dict,
            ) -> Iterator[str]:
        """Yield lines of CIF of a particular component, without calling it."""

        # This clones cifmap and appends
        # values in new cifmap without overriding
        # existing ones
        cifmap = {**_compo_to_cifmap(compo), **cifmap}

        # Opening line, define the routine
        yield f'DS {self.rout_num} 1 1;\n'

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

        # Precompute a list of [routine number, subcomponent]
        # Remember, subcomponents can also have subcomponents,
        # so the subroutine numbers won't always be consecutive.
        # There's no way to know ahead of time,
        # you just have to generate each subcompo and keep track of
        # the routine number
        subcompos = []
        for subcompo in compo.subcompos.values():
            subcompos.append((
                self.rout_num,
                list(self.yield_cif_bare(subcompo, cifmap))
                ))

        # Call subcomponent procedures
        for i, _ in subcompos:
            yield f'\tC {i};\n'
        yield 'DF;\n'

        # Define those procedures
        for _, this_subcompo in subcompos:
            yield from this_subcompo

