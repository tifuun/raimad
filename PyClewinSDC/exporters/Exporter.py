"""
Exporter.py -- base class for exporters
"""
from pathlib import Path

from PyClewinSDC.Component import Component


class Exporter(object):
    def __init__(self, output):
        pass

    def write_header(self):
        pass

    def write_polygon(self, polygon):
        pass

    def write_layer(self, layer):
        pass

    def write_footer(self):
        pass

    def write_component(self, component):
        for layer_name, polys in component.get_polygons().items():
            self.write_layer(component.layer_params[layer_name])
            for poly in polys:
                self.write_polygon(poly)

    @classmethod
    def export_component(cls, path: Path | str, component: Component):
        if isinstance(path, str):
            path = Path(path)

        with path.open('w') as f:
            exporter = cls(f)
            exporter.write_header()
            exporter.write_component(component)
            exporter.write_footer()
