import ast

class Viol():
    """
    Viol: Checker violation.
    This is a base class that can be used to catch
    all checker violtations.
    """

    def __init__(self, line, col=0, **context):
        if isinstance(line, ast.AST):
            self.line = line.lineno
            self.col = line.col_offset
        else:
            self.line = line
            self.col = col
        self.context = context

    def flake8(self):
        desc = self.desc.format(**self.context)
        name = type(self).__name__
        return f"{name} {desc}"

    def __str__(self):
        desc = self.desc.format(**self.context)
        name = type(self).__name__
        return f"<{name} at line {self.line}: {desc}>"

    def __repr__(self):
        return self.__str__()

class MarksViol(Viol):
    """
    MarksViol: Marks-related Checker violation.
    This is a base class that can be used to catch
    all marks-related checker violtations.
    All marks-related checker violations have
    a code in the form RAI4XX.
    """

class LenientViol(Viol):
    """
    LenientViol: Checker violation in Lenient mode.
    This is a base class that can be used to catch
    all checker violations that are raised in lenient mode
    only.
    Violations that are raised in stricter modes
    do not inherit from this class.
    """

class AuthoritarianViol(Viol):
    """
    """

class RAI412(MarksViol, LenientViol):
    desc = "Mark `{mark}` assigned multiple times at lines {lines}"

class RAI442(MarksViol, AuthoritarianViol):
    desc = "Assignment to undeclared mark `{mark}`"

