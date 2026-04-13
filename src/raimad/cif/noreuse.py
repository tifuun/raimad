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
from raimad.saveto import SavetoDest

def noreuse(
        compo: 'rai.typing.CompoLike',
        dest: SavetoDest = None,
        *,
        multiplier: float = 1e2,
        enable_cell_names: bool = False,
        ) -> str:

    def _yield_cif_bare(
            compo: 'rai.typing.CompoLike',
            cell_name: str | None,
            ) -> Iterator[str]:
        """Yield lines of CIF of a particular component, without calling it."""

        nonlocal rout_num

        # Opening line, define the routine
        yield f'DS {rout_num} 1 1;\n'

        if enable_cell_names:

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

        # Advance to next routine number
        rout_num += 1

        # Export all geometries
        for layer, geom in compo.geoms.items():

            # If a layer has been LMapp'ed to None,
            # that means the user wants it discarded. Skip.
            if layer is None:
                continue

            transformed_layer = _transform_lname(
                lname_transformers,
                layer
                )

            yield f'\tL {transformed_layer};\n'
            for poly in geom:
                yield '\tP '
                for point in poly:
                    yield (
                        f'{int(point[0] * multiplier)} '
                        f'{int(point[1] * multiplier)} '
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
                rout_num,
                list(_yield_cif_bare(
                    subcompo,
                    cell_name=
                        _compo_to_cell_name(subcompo_name, subcompo)
                        if enable_cell_names
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

    def _yield_cif() -> Iterator[str]:
        """Yield lines of cif file."""

        first_rout = rout_num

        yield from _yield_cif_bare(
            compo=compo,
            cell_name=type(compo.final()).__name__
            )
        yield f'C {first_rout};\n'
        yield 'E'

    lname_transformers = _compute_lname_transformers(compo)

    rout_num = 1
    cif_string = ''.join(_yield_cif())

    return rai.saveto._saveto(cif_string, dest)

def _compute_lname_transformers(compo):
    # TODO DOCUMENT THE LAMBDA THING SOMEWHERE!!
    # TODO defaults in compo class!!
    if hasattr(compo, '_experimental_lname_transformers'):
        if hasattr(compo._experimental_lname_transformers, '__call__'):
            return (
                compo._experimental_lname_transformers()
                )
        else:
            return (
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

        return (
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


class NoReuse():
    """For backwards compat."""
    def __init__(
            self,
            compo: 'rai.typing.CompoLike',
            multiplier: float = 1e2,
            ) -> None:
        self.cif_string = noreuse(compo, dest, multiplier=multiplier)

