import raimad as rai

class Mark(rai.Annotation):
    def __init__(self, desc: str):
        self.desc = desc
        self.name = 'this should be set in compo.__init_subclass_'


