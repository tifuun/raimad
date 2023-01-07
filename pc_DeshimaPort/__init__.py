"""
Port of DESHIMA2 components to PyClewinSDC.

So far, code is Written by Nikita,
based off the original codebase by Kenichi
"""

__author__ = "MaybE_Tree"
#__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = [
    "Kenichi Karatsu",
    ]
#__license__ = "GPL"
#__version__ = "1.0.1"
__maintainer__ = "MaybE_Tree"
#__email__ = "rob@spot.colorado.edu"
#__status__ = "Production"

# Module header example:
# https://stackoverflow.com/a/1523456

from pc_DeshimaPort.Filter import Filter

# Yes, (most) imports go AFTER dunders, this is pep8.

pc_export_components = [
    Filter,
    ]

