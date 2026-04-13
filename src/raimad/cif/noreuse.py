"""noreuse.py: home to the NoReuse CIF exporter."""

from typing import Iterator
from warnings import warn

import raimad as rai
from raimad.types import LNameTransformers
from raimad.cif.lname_transformers import (
    Enumerator,
    InvalidLayerNameTransformerCallable,
    InvalidLayerNameTransformerOutput,
    UntransformableLayerName,
    capitalise,
    noop,
    root,
    )

class NoReuse:
    """CIF Exporter that doesn't reuse subroutines."""

    def __init__(
            self,
            compo: 'rai.typing.CompoLike',
            multiplier: float = 1e2,
            ) -> None:

        self.compo = compo
        self.rout_num = 1
        self.multiplier = multiplier

        self.enable_cell_names = True  # TODO param

        # TODO DOCUMENT THE LAMBDA THING SOMEWHERE!!
        # TODO propagate these properties thru proxy??
        if hasattr(compo, '_experimental_lname_transformers'):
            if hasattr(compo._experimental_lname_transformers, '__call__'):
                self.lname_transformers = (
                    compo._experimental_lname_transformers()
                    )
            else:
                self.lname_transformers = (
                    compo._experimental_lname_transformers
                    )
        else:
            if hasattr(compo, '_experimental_extra_lname_transformers'):
                if hasattr(
                        compo._experimental_extra_lname_transformers,
                        '__call__'
                        ):
                    extras = compo._experimental_extra_lname_transformers()
                else:
                    extras = compo._experimental_extra_lname_transformers
            else:
                extras = []

            self.lname_transformers = (
                *extras,
                root,
                noop,
                capitalise,
                Enumerator(
                    warning=(
                        "RAIMAD Layer name `{name}` converted to numeric CIF "
                        "name `{result}.` For custom CIF layer names, specify "
                        "a layer name transformer. To silence this warning "
                        "while keeping the behavior, specify the "
                        "rai.cif.lname_transformers.Enumerator() transformer "
                        "manually. "
                        )
                    )
                )
            

        self.cif_string = self._export_cif()

    def _export_cif(self) -> str:
        return ''.join(self._yield_cif())

    def _yield_cif(self) -> Iterator[str]:
        """Yield lines of cif file."""
        first_rout = self.rout_num
        yield from self.yield_cif_bare(
            self.compo,
            cell_name=type(self.compo.final()).__name__
            )
        yield f'C {first_rout};\n'
        yield 'E'

    def yield_cif_bare(
            self,
            compo: 'rai.typing.CompoLike',
            cell_name: str | None,
            ) -> Iterator[str]:
        """Yield lines of CIF of a particular component, without calling it."""

        # Opening line, define the routine
        yield f'DS {self.rout_num} 1 1;\n'

        if self.enable_cell_names:

            if cell_name:
                yield f'9 {cell_name};\n'

            else:
                if cell_name is not None:
                    warn(
                        "Cell name is falsy but not None??? "
                        "How did this happen!?",
                        UserWarning
                        )

            # TODO L-name doc says no duplicate cell names
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

            transformed_layer = _transform_lname(
                self.lname_transformers,
                layer
                )

            yield f'\tL {transformed_layer};\n'
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

            subcompos.append((
                self.rout_num,
                list(self.yield_cif_bare(
                    subcompo,
                    cell_name=
                        _compo_to_cell_name(subcompo_name, subcompo)
                        if self.enable_cell_names
                        else None
                    ))
                ))

        # Call subcomponent procedures
        for i, _ in subcompos:
            yield f'\tC {i};\n'
        yield 'DF;\n'

        # Define those procedures
        for _, this_subcompo in subcompos:
            yield from this_subcompo

def _compo_to_cell_name(
        subcompo_name: str | int,
        subcompo: 'rai.typing.CompoLike',
        ) -> str:
    if isinstance(subcompo_name, int):
        instance_name = f'{subcompo_name}-ANON'
    elif isinstance(subcompo_name, str):
        instance_name = subcompo_name
    else:
        assert False

    type_name = type(subcompo.final()).__name__

    return f"{type_name}::{instance_name}"

def _transform_lname(lname_transformers: LNameTransformers, name: str) -> str:
    for transformer in lname_transformers:
        if hasattr(transformer, '__getitem__'):
            try:
                transformed = transformer[name]
            except KeyError:
                transformed = None

        #elif isinstance(transformer, rai.types.LNameTransformerCallable):
        elif hasattr(transformer, '__call__'):
            try:
                transformed = transformer(name)
            # TODO custom err type?
            except TypeError as err:
                raise InvalidLayerNameTransformerCallable(
                    "Could not call lname transformer {transformer}."
                    ) from err

        if transformed is not None:
            if not rai.is_lname_valid(transformed):
                raise InvalidLayerNameTransformerOutput(
                    f"Layer name `{name}` was transformed to `transformed` "
                    f"by transformer `{transformer}`, which is not a valid "
                    f"CIF layer name. Fix your layer name transformer!"
                    )
            break

    if transformed is None:
        raise UntransformableLayerName(
            f"RAIMAD Layer name `{name}` could not be transformed to "
            "a valid CIF layer name by any of the specified transformers "
            f"( {lname_transformers} ). "
            "Change the layer name or add a transformer that understands it. "
            )

    return transformed


