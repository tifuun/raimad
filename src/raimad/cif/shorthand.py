"""
shorthand.py: defines `export_cif` function.

The `export_cif` function is a more convenient way
of exporting components to CIF than using an exporter
directly.
"""

from typing import Protocol, Any

import raimad as rai

class ExporterProto(Protocol):
    """
    Protocol for CIF exporters.

    Currently, there is only one CIF exporter in RAIMAD: NoReuse.
    Future exporters (and user-defined exporters) must
    conform to this Protocol.

    If you don't know what Protocols are,
    they're like a "shell" of a class that specifies what features must
    be present in an actual class in order for it to comply
    (in this case, an __init__ method with certain paramters,
    and a `cif_string` attribute).

    Just like all othr type annotation,
    protocols do nothing at runtime.
    They're checked statically by mypy.
    """

    def __init__(
            self,
            compo: 'rai.typing.CompoLike',
            *args: Any,
            **kwargs: Any
            ) -> None:
        ...

    cif_string: str

def export_cif(
        compo: 'rai.typing.CompoLike',
        dest: rai.saveto.Destination = None,
        exporter: type[ExporterProto] | None = None,
        *args: Any,
        **kwargs: Any,
        ) -> str:
    """
    Export component to CIF.

    Parameters
    ----------
    compo: rai.typing.CompoLike
        The compo or proxy to export

    dest: str | Path | TextIO | None
        A path to a file or an already open file for saving the CIF
        output.
        If, instead of saving to disk, you want to have the CIF code
        as a string, set `dest` to None (or leave unset)
        and use this functions return value.

    exporter: ExporterProto
        The exporter to use. Currently, there is only one CIF exporter
        in RAIMAD.

    *args: Any
        Additional arguments will be passed to the the Exporter's __init__.

    *args: Any
        Additional keyword arguments will be passed
        to the the Exporter's __init__.

    Returns
    -------
        The generated CIF code is always returned as a string,
        regardless of what `dest` is set to.
    """
    exporter_instance = (exporter or rai.cif.NoReuse)(compo, *args, **kwargs)
    cif_string = exporter_instance.cif_string

    return rai.saveto._saveto(cif_string, dest)

def export_lyp(
        compo: 'rai.typing.CompoLike',
        dest: rai.saveto.Destination = None,
        exporter: type[ExporterProto] | None = None,
        *args: Any,
        **kwargs: Any,
        ) -> str:

    exporter_instance = (
            (exporter or rai.cif.lyp.LypExporter)
            (compo, *args, **kwargs)
            )
    # TODO names
    return rai.saveto._saveto(exporter_instance.cif_string, dest)


