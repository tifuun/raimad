"""noreuse.py: home to the NoReuse CIF exporter."""

from typing import Iterator
from warnings import warn

import raimad as rai

def _compo_to_cifmap(compo: rai.Proxy):
    return {
        lname: annot.cif_name for lname, annot in compo.final().Layers.items()
        }

def _resolve_lname(compo: rai.Proxy, layer, cifmap, lname_policy):

    cif_name = cifmap.get(layer) or layer

    if lname_policy in {'warn', 'err'}:
        text = (
            f"Layer name `{resolved_name}` of component "
            f"`{compo}` is not a valid CIF layer name. "
            "TODO advice"
            )

    if lname in {'warn', 'fallback_klay'}:

    if lname_policy == 'warn':
        pass

    elif lname_policy == 'err':
        pass

    elif lname_policy == 'fallback_klay':
        pass

    elif lname_policy == 'force_klay':
        pass

    else:
        # TODO raise valueerror
        pass


    if not rai.is_lname_valid(resolved_name):
        resolved_name = rai.lname_to_klay(resolved_name)
        warn(
            f"Layer name `{resolved_name}` of component "
            f"`{compo}` is not a valid CIF layer name. "
            "TODO advice",
            CIFLayerNameWarning
            )
        ## TODO Exception type
        #raise Exception(
        #    f"Layer name `{resolved_name}` of component "
        #    f"`{compo}` is not a valid CIF layer name. "
        #    f"TODO links to doc."
        #    )


class CIFLayerNameWarning(UserWarning):
    pass

class NoReuse:
    """CIF Exporter that doesn't reuse subroutines."""

    def __init__(
            self,
            compo: 'rai.typing.CompoLike',
            multiplier: float = 1e3,
            lname_policy = 'warn',
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

            ## Resolve name
            
            ## TODO THIS IS VERY TRICKY HERE!!!
            #try:
            #    cif_name = compo.final().Layers[layer].cif_name
            #except (KeyError, AttributeError):
            #    cif_name = None


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

