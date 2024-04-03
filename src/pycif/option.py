import pycif as pc

class Option:
    def __init__(self, desc: str, browser_default = pc.Empty):
        self.desc = desc
        self.category = type(self)
        self.name = 'this should be set in compo.__init_subclass_'
        self.default = 'this should be set in compo.__init_subclass_'
        self.browser_default = browser_default
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

