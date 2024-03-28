class Viol(Exception):
    """
    Viol: Checker violation.
    This is a base class that can be used to catch
    all checker violtations.
    """

    def __init__(self, line, **context):
        self.line = line
        self.context = context

    def __str__(self):
        return self.desc.format(**self.context)

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
    desc = "Mark {mark} assigned multiple times at lines {lines}."

class RAI442(MarksViol, AuthoritarianViol):
    desc = "Assignment to undeclared mark {mark}."

