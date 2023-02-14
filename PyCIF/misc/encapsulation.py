"""
Some fairly cursed encapsulation-related hijinks.

Decorate a method inside a class with `@exposable` to make it 'exposable'.
The class also needs to be decorated with `@expose_class`.
What can you do with exposable methods?
Well, now if you have a second class
that *encapsulates* the exposable class
(i.e. creates instances of exposable class in __init__),
you can now directly expose those exposable methods throught the exposing class.
So instead of `exposing.encapsulated_instance.exposed()`,
you can just `exposing.exposed()`
"""

def exposable(method):
    method._expose_me = True
    return method


def expose_class(cls):
    cls._exposable_methods = []
    for name, attr in cls.__dict__.items():
        if not hasattr(attr, '_expose_me'):
            continue

        cls._exposable_methods.append(attr)

    return cls


def expose_encapsulated(
        exposable_class: type,
        exposable_instance_name: str,
        chaining=True):
    def decorator(exposing_class: type):
        def inject_wrapper(method):
            def wrapper(self, *args, **kwargs):
                method(
                    getattr(self, exposable_instance_name),
                    *args,
                    **kwargs,
                    )

                if chaining:
                    return self

            wrapper.__name__ = method.__name__
            wrapper.__doc__ = method.__doc__
            setattr(exposing_class, method.__name__, wrapper)

        for method in exposable_class._exposable_methods:
            inject_wrapper(method)

        return exposing_class
    return decorator


