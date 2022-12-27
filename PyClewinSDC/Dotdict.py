"""
We currently use the addict Dict, same as Quiskit Metal

I actually started implementing my own dotdict and
realized the addict.Dict has all the features I wanted.
"""

from addict import Dict as Dotdict


#class Dotdict(dict):
#    """
#    It's like a python dictionary, but allows access to its elements
#    via object dot notation.
#    """
#    def __init__(self, *args, **kwargs):
#        """
#        All args are interpreted as "initializers" of this doctdict.
#        i.e. every arg will be converted to a dict, and its
#        contents will be used to initialize the new Dotdict.
#        In case of colliding names in the intializers,
#        later initializer will take priprity.
#
#        keyword arguments are interpreted as key-value pairs,
#        like in a regular dict. They take priority over initializers
#        """
#        super().__init__()
#        for initializer in args:
#            try:
#                self.update(dict(initializer))
#            except TypeError as super_exception:
#                raise Exception(
#                    f"Could not interpret {initializer} "
#                    "as a dict. "
#                    "You may only pass things that can be interpreted "
#                    "as dicts into the arguments of Dotdict.__init__"
#                    ) from super_exception
#        self.update(kwargs)
#    
#    def __getattr__(self, attr):
#        if attr in self.keys():
#            return self[attr]
#
#        else:
#            return super().__getattr__(attr)
#
#    __setattr__ = dict.__setitem__
#    __delattr__ = dict.__delitem__
#
