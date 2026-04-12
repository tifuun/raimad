"""err.py: All of RAIMAD errors in one conveniet module."""

from raimad.compo import InvalidSubcompoError
from raimad.compo import CompoInsteadOfProxyAsSubcompoError
from raimad.compo import TransformCompoError
from raimad.compo import CopyCompoError
from raimad.compo import ProxyCompoConfusionError

from raimad.ansec import AnSecError
from raimad.ansec import AnSecRadiusError
from raimad.ansec import AnSecRadiusTooManyArgumentsError
from raimad.ansec import AnSecRadiusNotEnoughArgumentsError
from raimad.ansec import AnSecRadiusIncorrectArgumentsError
from raimad.ansec import AnSecThetaError
from raimad.ansec import AnSecThetaTooManyArgumentsError
from raimad.ansec import AnSecThetaNotEnoughArgumentsError
from raimad.ansec import AnSecThetaIncorrectArgumentsError

from raimad.bbox import EmptyBBoxError

from raimad.saveto import InvalidDestinationError

from raimad.string_import import StringImportError

from raimad.transform import EditingArgumentError

from raimad.cif.lname_transformers import InvalidLayerNameTransformerOutput
from raimad.cif.lname_transformers import UntransformableLayerName

# __all__ should contain all re-exported objects
# (checked by mypy and ruff)
# do not edit this definition manually;
# use scripts/patch_dunder_all.py
# to update automatically.

__all__ = [
    "InvalidSubcompoError",
    "CompoInsteadOfProxyAsSubcompoError",
    "TransformCompoError",
    "CopyCompoError",
    "ProxyCompoConfusionError",
    "AnSecError",
    "AnSecRadiusError",
    "AnSecRadiusTooManyArgumentsError",
    "AnSecRadiusNotEnoughArgumentsError",
    "AnSecRadiusIncorrectArgumentsError",
    "AnSecThetaError",
    "AnSecThetaTooManyArgumentsError",
    "AnSecThetaNotEnoughArgumentsError",
    "AnSecThetaIncorrectArgumentsError",
    "EmptyBBoxError",
    "InvalidDestinationError",
    "StringImportError",
    "EditingArgumentError",
    ]

