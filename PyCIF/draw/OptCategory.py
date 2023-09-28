"""
OptCategory -- Option categories
"""

raise NotImplementedError

from dataclasses import dataclass


@dataclass
class OptCategory(object):
    """
    Option Category Specification.
    There exist a couple pre-defined ones,
    and package developers may include their own.
    """
    fancy_name: str = ''
    desc: str = ''


Unspecified = OptCategory(
    'Unspecified',
    'Unspecified option. The developer of this component should specify '
    'an option category for this option.',
    )


Geometric = OptCategory(
    'Geometric',
    'Geometric parameters of the design. '
    'Widths, lengths, thicknesses, etc. '
    'This is also the default option category.',
    )

Functional = OptCategory(
    'Functional',
    'Functional parameters. Wavelengths, frequencies, etc.',
    )

Environmental = OptCategory(
    'Environmental',
    'Physical constants / effects that influence the design.',
    )

Manufacture = OptCategory(
    'Manufacture',
    'geometric options that regard the manufacturing process.'
    )

DevDebug = OptCategory(
    'Developer Debug',
    'Options used for debugging by the component developer.',
    )

