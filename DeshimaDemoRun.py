from pathlib import Path

from PyClewinSDC.exporters.CIFExporter import CIFExporter
from PyClewinSDC.exporters.SVGExporter import SVGExporter
from PyClewinSDC.Modulebrowser.Modulebrowser import generate_package_entries

from pc_DeshimaDemo.DeshimaDemo import DeshimaDemo
import pc_Fundamental

if __name__ == '__main__':
    demo = DeshimaDemo()
    demo.make()
    with open('DeshimaDemo.cif', 'w') as f:
        CIFExporter(f, demo)

    with open('DeshimaDemo.svg', 'w') as f:
        SVGExporter(f, demo)

    generate_package_entries(pc_Fundamental, Path('./module_browser'))

