"""layer.py: home to the Layer class."""
import raimad as rai
from warnings import warn

class Layer(rai.Annotation):
    """
    Layer annotation.

    Layer objects are meant to exist in the `Layers` nested
    class of compos.
    They act as annotations that better explain what each
    layer is.
    """

    def __init__(
            self,
            desc: str,
            cif_name: str | None = None,
            lyp_expanded: None = None,
            lyp_frame_color: None = None,
            lyp_fill_color: None = None,
            lyp_frame_brightness: None = None,
            lyp_fill_brightness: None = None,
            lyp_dither_pattern: None = None,
            lyp_line_style: None = None,
            lyp_valid: None = None,
            lyp_visible: None = None,
            lyp_transparent: None = None,
            lyp_width: None = None,
            lyp_marked: None = None,
            lyp_xfill: None = None,
            lyp_animation: None = None,
            lyp_name: None = None,
            ):
        self.name = 'this should be set in compo.__init_subclass_'
        self.desc = desc
        self.cif_name = cif_name

        if lyp_expanded is not None:
            warn('Property lyp_expanded is not yet implemented.')

        if lyp_frame_color is not None:
            warn('Property lyp_frame_color is experimental.')
            #TODO validate that it is a color.

        if lyp_fill_color is not None:
            warn('Property lyp_fill_color is experimental.')
            #TODO validate that it is a color.

        if lyp_frame_brightness is not None:
            warn('Property lyp_frame_brightness is not yet implemented.')

        if lyp_fill_brightness is not None:
            warn('Property lyp_fill_brightness is not yet implemented.')

        if lyp_dither_pattern is not None:
            warn('Property lyp_dither_pattern is not yet implemented.')

        if lyp_line_style is not None:
            warn('Property lyp_line_style is not yet implemented.')

        if lyp_valid is not None:
            warn('Property lyp_valid is not yet implemented.')

        if lyp_visible is not None:
            warn('Property lyp_visible is not yet implemented.')

        if lyp_transparent is not None:
            warn('Property lyp_transparent is not yet implemented.')

        if lyp_width is not None:
            warn('Property lyp_width is not yet implemented.')

        if lyp_marked is not None:
            warn('Property lyp_marked is not yet implemented.')

        if lyp_xfill is not None:
            warn('Property lyp_xfill is not yet implemented.')

        if lyp_animation is not None:
            warn('Property lyp_animation is not yet implemented.')

        if lyp_name is not None:
            warn('Property lyp_name is not yet implemented.')

        self.lyp_fill_color = lyp_fill_color
        self.lyp_frame_color = lyp_frame_color

_root = Layer("Root layer.", "ROOT")
_root.name = 'root'

