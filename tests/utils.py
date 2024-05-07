from typing import ClassVar
import numpy as np

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
