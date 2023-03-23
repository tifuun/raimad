from dataclasses import dataclass
import simple_parsing

class Test:
    """
    Test docstring
    """

    size: int = 5
    """Size of object"""

    name: str = "hello"
    """Name of object"""

Test = dataclass(Test)

print(simple_parsing.docstring.get_attribute_docstring(Test, 'size'))

