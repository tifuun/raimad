class Option:
    def __init__(self, desc: str):
        self.desc = desc
        self.category = type(self)
        self.name = 'this should be set in compo.__init_subclass_'
        self.default = 'this should be set in compo.__init_subclass_'
        self.annot = 'this should be set in compo.__init_subclass_'

class Geometric(Option):
    pass

class Functional(Option):
    pass

class Debug(Option):
    pass

class Environmental(Option):
    pass


Option.Functional = Functional
Option.Geometric = Geometric
Option.Debug = Debug
Option.Environmental = Environmental

