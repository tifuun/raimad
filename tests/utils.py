from pprint import pprint
from sys import stderr
from typing import ClassVar

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

    def checkPolysEqual(
            self,
            actual: rait.Poly,
            expected: rait.Poly,
            epsilon: float | None = None
            ):

        return all(
            rai.distance_between(point1, point2) <= (epsilon or self.epsilon)
            for point1, point2 in
            zip(actual, expected, strict=True)
            )

    def assertGeomsEqual(
            self,
            actual: rait.Geoms,
            expected: rait.Geoms,
            epsilon: float | None = None):
        self.assertEqual(set(actual.keys()), set(expected.keys()))
        for layer_name in actual.keys():

            polys_actual = actual[layer_name]
            polys_expected = expected[layer_name]

            self.assertEqual(len(polys_actual), len(polys_expected))
            length = len(polys_actual)

            num_equal_actual = sum(
                self.checkPolysEqual(poly1, poly2)
                for poly1 in polys_actual
                for poly2 in polys_actual
                )

            num_equal_expected = sum(
                self.checkPolysEqual(poly1, poly2)
                for poly1 in polys_expected
                for poly2 in polys_expected
                )

            num_equal = 0
            for poly_actual in polys_actual:
                for poly_expected in polys_expected:
                    num_equal += rai.iters.is_rotated(
                            poly_expected,
                            poly_actual,
                            comparison=self.checkPolysEqual
                            # TODO omg this is borderline incomprehensible
                            # TODO pass epsilon
                            )

            try:
                self.assertEqual(num_equal_expected, num_equal_actual)
                self.assertEqual(num_equal + num_equal_actual, length * 2)
                # TODO What on earth!?
            except AssertionError as err:
                print(f'ON LAYER {layer_name}', file=stderr)
                print("ACTUAL: ", file=stderr)
                pprint(polys_actual, stream=stderr)
                print("expected: ", file=stderr)
                pprint(polys_expected, stream=stderr)
                raise err

        return True

