from pathlib import Path

from PyClewinSDC.exporters.CIFExporter import CIFExporter
from PyClewinSDC.exporters.SVGExporter import SVGExporter
from PyClewinSDC.Modulebrowser import generate_entries

from pc_DeshimaDemo.DeshimaDemo import DeshimaDemo
from pc_Fundamental.Mesh import Mesh
from pc_Fundamental.Filter import MSFilter, MSFilterParametric

if __name__ == '__main__':
    demo = DeshimaDemo()
    demo.make()
    with open('DeshimaDemo.cif', 'w') as f:
        CIFExporter(f, demo)

    with open('DeshimaDemo.svg', 'w') as f:
        SVGExporter(f, demo)

    generate_entries((Mesh, MSFilter, MSFilterParametric), Path('./module_browser'))

