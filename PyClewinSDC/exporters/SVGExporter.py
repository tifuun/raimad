"""
Scalable Vector Graphics Exporter
"""

from PyClewinSDC.Component import Component


def SVGExporter(stream, component: Component):
    stream.write('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">\n')

    for layer_name, polys in component.get_polygons().items():
        for poly in polys:
            stream.write('\t<polygon points="')
            for point in poly.xyarray:
                ##point2 = point // 1000
                stream.write(f"{point[0]},{point[1]} ")
            stream.write('" />\n')

    stream.write('</svg>\n')

