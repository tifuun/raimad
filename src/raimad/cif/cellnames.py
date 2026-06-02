import raimad as rai
from typing import Literal

def digits_needed(subcompos):
    return len(str(sum(map(lambda x: isinstance(x, int), subcompos.keys()))))

def compo_to_cell_name(
        subcompo_name: str | int,
        subcompo: 'rai.typing.CompoLike',
        digits: int | None,
        ) -> str:
    if isinstance(subcompo_name, int):
        if digits is None:
            instance_name = f'{subcompo_name}-ANON'
        else:
            padded = str(subcompo_name).zfill(digits)
            instance_name = f'{padded}-ANON'
    elif isinstance(subcompo_name, str):
        instance_name = subcompo_name
    else:
        assert False

    type_name = type(subcompo.final()).__name__

    return f"{type_name}::{instance_name}"


