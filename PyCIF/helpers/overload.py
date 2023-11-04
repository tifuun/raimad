"""
Support for keyword-based overloading
"""

import inspect

def get_default_kwonly(func):
    return frozenset(
        p.name for p in inspect.signature(func).parameters.values()
        if p.kind == inspect.Parameter.KEYWORD_ONLY
        #    and p.default != inspect.Parameter.empty
        )

def kwoverload(func):
    def overload_dispatcher(*args, **kwargs):
        for overload_args, target in overload_dispatcher._pc_overload_map.items():
            if overload_args.issubset(kwargs.keys()):
                return target(*args, **kwargs)
        raise Exception("Could not resolve overload")

    overload_dispatcher._pc_overload_map = {}

    def register(func):
        kwsig = get_default_kwonly(func)
        if kwsig in overload_dispatcher._pc_overload_map.keys():
            raise Exception("Identical kwsig")

        overload_dispatcher._pc_overload_map[kwsig] = func

    overload_dispatcher.register = register
    register(func)

    return overload_dispatcher

