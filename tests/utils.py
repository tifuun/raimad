from pprint import pprint
from sys import stderr
from typing import ClassVar
import numpy as np

import raimad as rai
import raimad.typing as rait

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

class GeomsEqual():
    """
    Mixing for comparing geoms, regardless
    of the order of polys in each layer,
    or the order of points in each poly
    """
    def assertGeomsEqual(self, actual: rait.Geoms, desired: rait.Geoms):
        self.assertEqual(set(actual.keys()), set(desired.keys()))
        for layer_name in actual.keys():

            polys_actual = actual[layer_name]
            polys_desired = desired[layer_name]

            self.assertEqual(len(polys_actual), len(polys_desired))
            length = len(polys_actual)

            num_equal = 0
            for poly_actual in polys_actual:
                for poly_desired in polys_desired:
                    num_equal += rai.iters.is_rotated(
                            poly_desired,
                            poly_actual,
                            )

            try:
                self.assertEqual(num_equal, length)
            except AssertionError as err:
                print(f'ON LAYER {layer_name}', file=stderr)
                print("ACTUAL: ", file=stderr)
                pprint(polys_actual, stream=stderr)
                print("DESIRED: ", file=stderr)
                pprint(polys_desired, stream=stderr)
                raise err

        return True

