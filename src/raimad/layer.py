"""layer.py: home to the Layer class."""
import raimad as rai

class Layer(rai.Annotation):
    """
    Layer annotation.

    Layer objects are meant to exist in the `Layers` nested
    class of compos.
    They act as annotations that better explain what each
    layer is.
    """

    def __init__(self, desc: str):
        self.desc = desc
        self.name = 'this should be set in compo.__init_subclass_'

