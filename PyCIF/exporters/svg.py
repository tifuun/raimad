"""
Scalable Vector Graphics Exporter.
"""

#from PyCIF.draw.Component import Component
#from PyCIF.draw.LayerCategory import Unspecified, Foreground, Background
#from PyCIF.exporters import argparse_utils
#
#CLI_NAME = 'svg'
#
#layer_styles = {
#    Unspecified: 'class="unspecified"',
#    Foreground: 'class="foreground"',
#    Background: 'class="background"',
#    #Background: 'class="background" fill="none" stroke-width="1px" stroke="#000" ',
#    }
#
#
#class SVGExporter(object):
#    def __init__(self, stream, compo: Component):
#        self.stream = stream
#        self.compo = compo
#
#        self.width = self.compo.bbox.width
#        self.height = self.compo.bbox.height
#
#        self._write_header()
#        self._draw_layers()
#        self._draw_marks()
#        self._write_footer()
#
#    def _write_header(self):
#        self.stream.write(
#            '<svg xmlns="http://www.w3.org/2000/svg" '
#            f'width="{self.width}" '
#            f'height="{self.height}">\n',
#            )
#
#    def _write_footer(self):
#        self.stream.write('</svg>\n')
#
#    def _draw_layers(self):
#        layers = self.compo.get_polygons()
#
#        for layer_name, polys in layers.items():
#            layer = self.compo.layerspecs[layer_name]
#            style = layer_styles[layer.category]
#
#            for poly in polys:
#                self._draw_poly(poly, style)
#
#    def _draw_poly(self, poly, style):
#        self.stream.write(f'\t<polygon {style} points="')
#
#        for point in poly.get_xyarray():
#            point_x, point_y = self._transform_point(*point)
#            self.stream.write(f'{point_x},{point_y} ')
#
#        self.stream.write('" />\n')
#
#    def _draw_marks(self):
#        mark_size = min(self.width, self.height) / 50
#
#        for mark_name, mark in self.compo.marks.items():
#            point_x, point_y = self._transform_point(mark.x, mark.y)
#            self._draw_circle(point_x, point_y, mark_size, mark_name)
#
#    def _draw_circle(self, cx, cy, r, name):
#        self.stream.write(
#            '\t<circle class="mark" '
#            f'cx="{cx}" '
#            f'cy="{cy}" '
#            f'r="{r}" '
#            '>\n',
#            )
#        self.stream.write(
#            f'\t\t<title>{name}</title>\n',
#            )
#        self.stream.write('\t</circle>\n')
#
#    def _transform_point(self, x, y):
#        return (
#            x - self.compo.bbox.left,
#            self.compo.bbox.top - y,
#            )
#
#
#def export(stream, component: Component):
#    """
#    Export component to SVG file.
#    """
#    SVGExporter(stream, component)
#
#
#def create_parser_options(parser):
#    """
#    Add options to argparse parser to invoke this exporter
#    """
#    argparse_utils.arg_output_file(parser)
#    argparse_utils.arg_component(parser)
#
#
#def run_cli(args):
#    component = args.component()
#    component.make()
#    export(args.output_file, component)
#
