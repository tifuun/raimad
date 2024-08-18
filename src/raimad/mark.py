"""mark.py: home to the Mark class."""
import raimad as rai

class Mark(rai.Annotation):
    """
    Mark annotation.

    Mark objects are meant to exist inside the `Marks` nested
    class of Compos,
    and serve as annotations that better explain what are the
    marks that this compo defines.

    TODO reference boundpoint
    """

    def __init__(self, desc: str):
        self.desc = desc
        self.name = 'this should be set in compo.__init_subclass_'


