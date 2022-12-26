from PyClewinSDC.exporters.CIFExporter import CIFExporter
from pc_DeshimaDemo.DeshimaDemo import DeshimaDemo

if __name__ == '__main__':
    demo = DeshimaDemo()
    demo.make()
    CIFExporter.export_component('./DeshimaDemo.cif', demo)

