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
                np.array(actual),
                np.array(desired),
                decimal=self.decimal
                )
            )

        # The explicit `np.array` cast above is very necessary,
        # because if somebody tries to pass an unbound BoundPoint
        # to this method, `np.testing.assert_array_almost_equal`
        # will try to get the `proxy` of the boundpoint,
        # raising an error

    def assertAlmostEqual(self, first, second):
        super().assertAlmostEqual(
            first,
            second,
            places=self.decimal
            )
