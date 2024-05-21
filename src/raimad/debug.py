import os
import raimad as rai

def show(compo: rai.Compo):
    with open('/tmp/raimad_debug.cif', 'w') as f:
        f.write(rai.export_cif(compo))
    #os.system('flatpak run de.klayout.KLayout /tmp/raimad_debug.cif')

