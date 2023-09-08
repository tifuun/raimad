import PyCIF as pc
from PyCIF.draw import TransmissionLine as tl

def format_path(path):
    return '\n'.join([repr(conn) for conn in path])

def _render_path_as_svg(svg, path):
    for conn, next_conn in pc.iter.duplets(path):

        if isinstance(conn.to, pc.Point):
            #svg.circle(*conn.to, name=repr(conn))
            svg.circle(*conn.to)

            if isinstance(next_conn.to, pc.Point):

                if isinstance(next_conn, tl.StraightTo):
                    line_style = dict(
                        color='#00f',
                        )
                elif isinstance(next_conn, tl.JumpTo):
                    line_style = dict(
                        color='#888',
                        )
                elif isinstance(next_conn, tl.ElbowTo):
                    line_style = dict(
                        color='#008',
                        dasharray=True,
                        )
                else:
                    line_style = dict()

                svg.line(*conn.to, *next_conn.to, **line_style)

    svg.circle(*next_conn.to)

def render_path_as_svg(path, stream=None):
    """
    Render path as svg, return stream
    """
    svg = pc.viz.SVG(stream=stream)
    _render_path_as_svg(svg, path)
    svg.done()

    return stream or svg.stream

def render_paths_as_svg(paths):
    svgs = []
    for path in paths:
        svg = pc.viz.SVG()
        _render_path_as_svg(svg, path)
        svg.make_frame()
        svgs.append(svg)

    finalsvg = svgs[0]

    for svg in svgs[1:]:
        finalsvg.collage_E(svg)
    #svg = pc.viz.SVG(stream=stream)
    #for path in paths:
    #    _render_path_as_svg(svg, path)
    #    svg.collage_E()
    #svg.done()

    finalsvg.done()

    return svgs[0].stream

