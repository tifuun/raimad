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

from raimad.rectwire import RectWireError
from raimad.rectwire import RectWireTooManyArgumentsError
from raimad.rectwire import RectWireNotEnoughArgumentsError
from raimad.rectwire import RectWireIncorrectArgumentsError

from raimad.bbox import EmptyBBoxError

from raimad.cif.shorthand import InvalidDestinationError

from raimad.string_import import StringImportError

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
    "RectWireError",
    "RectWireTooManyArgumentsError",
    "RectWireNotEnoughArgumentsError",
    "RectWireIncorrectArgumentsError",
    "EmptyBBoxError",
    "InvalidDestinationError",
    "StringImportError",
    ]

