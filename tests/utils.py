from pprint import pprint
from sys import stderr
from typing import ClassVar
import numpy as np

class PrettyEqual():
    def assertPrettyEqual(self, actual, desired):
        try:
            self.assertEqual(actual, desired)

        except AssertionError as err:
            pprint("ACTUAL: ", stream=stderr)
            pprint(actual, stream=stderr)
            pprint("DESIRED: ", stream=stderr)
            pprint(desired, stream=stderr)
            raise err


class ArrayAlmostEqual():
    decimal: ClassVar[float]

    def __init_subclass__(cls, *args, decimal=7, **kwargs) -> None:
        cls.decimal = decimal
        super().__init_subclass__(*args, **kwargs)

    def assertArrayAlmostEqual(self, actual, desired):
        self.assertIsNone(
            np.testing.assert_array_almost_equal(
                actual,
                desired,
                decimal=self.decimal
                )
            )

    def assertAlmostEqual(self, first, second):
        super().assertAlmostEqual(
            first,
            second,
            places=self.decimal
            )
