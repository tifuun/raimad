import os
import pycif as pc

def show(compo: pc.Compo):
    with open('/tmp/pycif_debug.cif', 'w') as f:
        f.write(pc.export_cif(compo))
    #os.system('flatpak run de.klayout.KLayout /tmp/pycif_debug.cif')

