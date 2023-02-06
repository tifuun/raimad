# PyCif

## Key Code Guidelines for PyCIF:

1. **Never parse python code manually.**
This is difficult to do, and even more difficult to do well,
because there is quite a lot of freedom in Python's syntax.
Luckily, we're writing Python, not C, which means we have a wide array
of introspection tools available to us.
For example, the module browser can access docstrings of live objects
directly, instead of parsing their source code to extract comments.

1. **Work with modules, not files.**
Same logic as the previous guideline.

1. **Don't use asterisk imports or conditional imports**
Difficult to figure out where a name comes from,
even for linters.

1. Only import statements in `__init__.py`
to make importing faster.
Read more: https://web.archive.org/web/20200721150953/http://effbot.org/pyfaq/what-is-init-py-used-for.htm

1. Files containing class definitions should have same name as call
e.g. `Layer.py` defines class `Layer`.
Directories always lowercase

1. Internal modules should use full import path
(i.e. no local import and no relying on import shorthands
from `__init__` files)

## Additional Reading:
1. https://docs.python-guide.org/writing/structure/

## WPS/Pylint rules

1. WPS305
I like f-strings.
The rules regulating their complexity are good tho

1. D200
Always use multiline docstrings for ease of adding code

1. W391
Always have one empty line at end of file.
Other rules ensure there's not too many.

1. E123
WTF?
