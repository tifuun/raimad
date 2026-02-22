from pprint import pprint
from sys import stderr
from typing import ClassVar, Sequence
from contextlib import contextmanager
import warnings

from io import StringIO
import raimad as rai
from raimad.types import Geoms, Poly
from raimad.typing import CompoLike

class XmlComparisonMixin:
    def assertXmlEqual(self, xml1, xml2):
        if xml1 != xml2:
            warnings.warn(
                'assertXmlEqual is currently implemented '
                'with raw string comparison, FIXME!!'
                ,
                warnings.UserWarning
                )
        self.assertEqual(xml1, xml2)

class AssertDoesntWarn:
    """
    Mixin for unittest.TestCase that adds `assertDoesntWarn` context manager.
    
    Works like `assertWarns`, but asserts that no warnings are emitted.
    """

    @contextmanager
    def assertDoesntWarn(self, msg=None):
        """
        Context manager that fails if any warnings are raised within its block.
        
        Example:
            with self.assertDoesntWarn():
                do_something()
        """
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            yield  # Run the code under test
        if caught:
            formatted = "\n".join(
                f"{w.category.__name__}: {w.message}" for w in caught
            )
            standard_msg = f"Unexpected warnings raised:\n{formatted}"
            self.fail(self._formatMessage(msg, standard_msg))

### END CHATGPT CODE ###

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
            actual: Poly,
            expected: Poly,
            epsilon: float | None = None
            ):

        return all(
            rai.distance_between(point1, point2) <= (epsilon or self.epsilon)
            for point1, point2 in
            zip(actual, expected, strict=True)
            )

    def assertManyGeomsEqual(
            self,
            geomses: Sequence[Geoms | CompoLike],
            epsilon: float | None = None):

        for a, b in rai.duplets(geomses):
            self.assertGeomsEqual(a, b)

    def assertGeomsEqual(
            self,
            actual: Geoms | CompoLike,
            expected: Geoms | CompoLike,
            epsilon: float | None = None):

        if isinstance(actual, CompoLike):
            actual = actual.steamroll()

        if isinstance(expected, CompoLike):
            expected = expected.steamroll()

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
                stream = StringIO()
                print(f'ON LAYER {layer_name}', file=stream)
                print("ACTUAL: ", file=stream)
                pprint(polys_actual, stream=stream)
                print("expected: ", file=stream)
                pprint(polys_expected, stream=stream)
                raise AssertionError(stream.getvalue()) from err

        return True

    def assertGeomsEqualButAllowDifferentNames(
            self,
            actual: Geoms,
            expected: Geoms,
            epsilon: float | None = None):

        # TODO this is a hack
        # TODO FIXME FIXME this breaks if layer order is different FIXME
        return self.assertGeomsEqual(
            {f"layer{i}": geoms for i, geoms in enumerate(actual.values())},
            {f"layer{i}": geoms for i, geoms in enumerate(expected.values())},
            epsilon
            )

