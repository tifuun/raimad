from pprint import pprint
from sys import stderr
from typing import ClassVar
import numpy as np

import raimad as rai
import raimad.typing as rait

class PrettyEqual():
    def assertPrettyEqual(self, actual, expected):
        try:
            self.assertEqual(actual, expected)

        except AssertionError as err:
            pprint("ACTUAL: ", stream=stderr)
            pprint(actual, stream=stderr)
            pprint("EXPECTED: ", stream=stderr)
            pprint(expected, stream=stderr)
            raise err


class ArrayAlmostEqual():
    decimal: ClassVar[float]

    def __init_subclass__(cls, *args, epsilon=0.01, **kwargs) -> None:
        cls.epsilon = epsilon
        super().__init_subclass__(*args, **kwargs)

    def assertArrayAlmostEqual(self, actual, expected, epsilon=None):
        max_deviation = max((abs(a - d) for a, d in zip(actual, expected)))

        try:
            self.assertTrue(max_deviation <= (epsilon or self.epsilon))
        except AssertionError as err:
            print("ACTUAL: ", file=stderr)
            pprint(actual, stream=stderr)
            print("EXPECTED: ", file=stderr)
            pprint(expected, stream=stderr)
            raise err

    def assertAlmostEqual(self, actual, expected, epsilon=None):
        self.assertTrue(abs(actual - expected) <= (epsilon or self.epsilon))

class GeomsEqual():
    """
    Mixin for comparing geoms, regardless
    of the order of polys in each layer,
    or the order of points in each poly
    """

    def __init_subclass__(cls, *args, epsilon=0.001, **kwargs) -> None:
        cls.epsilon = epsilon
        super().__init_subclass__(*args, **kwargs)

    def assertGeomsEqual(
            self,
            actual: rait.Geoms,
            expected: rait.Geoms,
            epsilon: float | None = None):
        self.assertEqual(set(actual.keys()), set(expected.keys()))
        for layer_name in actual.keys():

            # TODO TODO horrible awful no-good dynamic brainrot hack
            # to filter out points that are represented as arrays
            # rather than lists
            # we really need to just grind through everything with mypy
            # to make sure things are always what we expect them to be
            polys_actual = [
                [
                    point.tolist() if isinstance(point, np.ndarray)
                    else point
                    for point in poly
                    ]
                for poly in actual[layer_name]
                ]
            polys_expected = expected[layer_name]

            self.assertEqual(len(polys_actual), len(polys_expected))
            length = len(polys_actual)

            num_equal = 0
            for poly_actual in polys_actual:
                for poly_expected in polys_expected:
                    num_equal += rai.iters.is_rotated(
                            poly_expected,
                            poly_actual,
                            comparison=lambda poly1, poly2:
                                all(
                                    #round(abs(coord1 - coord2), self.decimal)
                                    #    == 0
                                    abs(coord1 - coord2)
                                        <= (epsilon or self.epsilon)
                                    for point1, point2 in
                                    zip(poly1, poly2, strict=True)
                                    for coord1, coord2 in
                                    zip(point1, point2, strict=True)
                                    )
                                # TODO omg this is borderline incomprehensible
                            )

            try:
                self.assertEqual(num_equal, length)
            except AssertionError as err:
                print(f'ON LAYER {layer_name}', file=stderr)
                print("ACTUAL: ", file=stderr)
                pprint(polys_actual, stream=stderr)
                print("expected: ", file=stderr)
                pprint(polys_expected, stream=stderr)
                raise err

        return True

