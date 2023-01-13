from pathlib import Path

from PyClewinSDC.exporters.CIFExporter import CIFExporter
from PyClewinSDC.exporters.SVGExporter import SVGExporter
from PyClewinSDC.Modulebrowser.Modulebrowser import generate_multi_package_entries

from pc_DeshimaDemo2.DeshimaDemo2 import DeshimaDemo2
import pc_DeshimaPort
import pc_Fundamental
import pc_LeakyAntenna

if __name__ == '__main__':
    demo = DeshimaDemo2()
    demo.make()
    with open('DeshimaDemo.cif', 'w') as f:
        CIFExporter(f, demo)

    with open('DeshimaDemo.svg', 'w') as f:
        SVGExporter(f, demo)

    #generate_package_entries(pc_DeshimaPort, Path('./module_browser'))
    #generate_multi_package_entries(
    #    [
    #        pc_Fundamental,
    #        pc_DeshimaPort,
    #        pc_LeakyAntenna,
    #        ],
    #    Path('./module_browser')
    #    )

