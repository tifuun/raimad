"""partial.py: home to the Partial class."""

from typing import Any
from copy import copy
import raimad as rai

class Partial:
    """
    Partial: a halfway-created Compo.

    Much like Pythons `functools.partial`,
    which allows partially calling a function,
    a Partial allows partially creating a Compo.
    A Partial points to a CompoType and holds a set of
    pre-determined options for that CompoType.
    When the Partial is __call__'ed,
    it creates a new Compo based on the held options,
    as well as any options passed to __call__.
    The options passed to __call__ take precedence
    over the held options.
    """

    compo_cls: 'rai.typing.CompoType'

    def __init__(
            self,
            compo_cls: 'rai.typing.CompoType',
            **kwargs: Any
            ) -> None:

        self.kwargs = kwargs
        self.compo_cls = compo_cls

    def __call__(self, **kwargs: Any) -> 'rai.typing.Compo':
        """Finish creating the partially created Compo."""
        kwargs2 = copy(self.kwargs)
        kwargs2.update(kwargs)
        return self.compo_cls(**kwargs2)

