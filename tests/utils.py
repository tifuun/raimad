from pprint import pprint
from sys import stderr
from typing import ClassVar, Sequence, Protocol, Any, Iterator, Self
from contextlib import contextmanager
import warnings

from io import StringIO
import raimad as rai
from raimad.types import GeomsS, Poly
from raimad.typing import CompoLike

from unittest import TestCase

class XmlComparisonMixin:
    def assertXmlEqual(self, xml1: str, xml2: str) -> None:
        if xml1 != xml2:
            warnings.warn(
                'assertXmlEqual is currently implemented '
                'with raw string comparison, FIXME!!'
                ,
                UserWarning
                )
        self.assertEqual(xml1, xml2)

### BGEIN CHATGPT CODE ###

class AssertDoesntWarn:
    """
    Mixin for unittest.TestCaseProto that adds `assertDoesntWarn` context manager.
    
    Works like `assertWarns`, but asserts that no warnings are emitted.
    """

    @contextmanager
    def assertDoesntWarn(self, msg: str | None = None) -> Iterator[None]:
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
    def assertPrettyEqual(self, actual: Any, expected: Any) -> None:
        try:
            self.assertEqual(actual, expected)

        except AssertionError as err:
            pprint("ACTUAL: ", stream=stderr)
            pprint(actual, stream=stderr)
            pprint("EXPECTED: ", stream=stderr)
            pprint(expected, stream=stderr)
            raise err

class ArrayApproxEqual():
    decimal: ClassVar[float]
    epsilon: ClassVar[float]

    def __init_subclass__(cls, *args: Any, epsilon: float = 0.01, **kwargs: Any) -> None:
        cls.epsilon = epsilon
        super().__init_subclass__(*args, **kwargs)

    def assertArrayApproxEqual(
            self,
            actual: Sequence[float],
            expected: Sequence[float],
            epsilon: float | None = None
            ) -> None:
        max_deviation = max((abs(a - d) for a, d in zip(actual, expected)))

        try:
            self.assertTrue(max_deviation <= (epsilon or self.epsilon))
        except AssertionError as err:
            print("ACTUAL: ", file=stderr)
            pprint(actual, stream=stderr)
            print("EXPECTED: ", file=stderr)
            pprint(expected, stream=stderr)
            raise err

    def assertApproxEqual(
            self,
            actual: Any,
            expected: Any,
            epsilon: float | None = None
            ) -> None:
        self.assertTrue(abs(actual - expected) <= (epsilon or self.epsilon))

class TestCaseGeomsProto(Protocol):
    """
    TODO docstring
    """
    def assertEqual(self, a: Any, b: Any) -> None: ...
    def assertTrue(self, a: Any) -> None: ...
    def fail(self, msg: str) -> None: ...
    def _formatMessage(self, a: str | None, b: str) -> str: ...
    epsilon: ClassVar[float]
    def assertManyGeomsEqual(
            self,
            geomses: Sequence[GeomsS | CompoLike],
            epsilon: float | None = None) -> None: ...

    def assertGeomsEqual(
            self,
            actual: GeomsS | CompoLike,
            expected: GeomsS | CompoLike,
            epsilon: float | None = None) -> None: ...

    def assertGeomsEqualButAllowDifferentNames(
            self,
            actual: GeomsS,
            expected: GeomsS,
            epsilon: float | None = None) -> None: ...

    def checkPolysEqual(
            self,
            actual: Poly,
            expected: Poly,
            epsilon: float | None = None
            ) -> bool: ...

class GeomsEqual():
    """
    Mixin for comparing geoms, regardless
    of the order of polys in each layer,
    or the order of points in each poly
    """
    epsilon: float

    def __init_subclass__(cls, *args: Any, epsilon: float = 0.001, **kwargs: Any) -> None:
        cls.epsilon = epsilon
        super().__init_subclass__(*args, **kwargs)

    def checkPolysEqual(
            self,
            actual: Poly,
            expected: Poly,
            epsilon: float | None = None
            ) -> bool:

        return all(
            rai.distance_between(point1, point2) <= (epsilon or self.epsilon)
            for point1, point2 in
            zip(actual, expected, strict=True)
            )

    def assertManyGeomsEqual(
            self,
            geomses: Sequence[GeomsS | CompoLike],
            epsilon: float | None = None) -> None:

        for a, b in rai.duplets(geomses):
            self.assertGeomsEqual(a, b)

    def assertGeomsEqual(
            self,
            actual: GeomsS | CompoLike,
            expected: GeomsS | CompoLike,
            epsilon: float | None = None) -> None:

        if isinstance(actual, CompoLike):
            actual = actual.steamroll()

        if isinstance(expected, CompoLike):
            expected = expected.steamroll()

        self.assertTrue(rai.geom.geoms_equal(
            (expected, actual),
            canon_geoms=rai.geom.canon_layer_order,
            canon_polys=rai.geom.canon_order,
            canon_poly=rai.geom.canon_rot_or,
            canon_vec2=rai.geom.canon_micron,
            ))

    def assertGeomsEqualButAllowDifferentNames(
            self,
            actual: GeomsS,
            expected: GeomsS,
            epsilon: float | None = None) -> None:

        if isinstance(actual, CompoLike):
            actual = actual.steamroll()

        if isinstance(expected, CompoLike):
            expected = expected.steamroll()

        self.assertTrue(rai.geom.geoms_equal(
            (expected, actual),
            canon_geoms=rai.geom.canon_no_layer_names,
            canon_polys=rai.geom.canon_order,
            canon_poly=rai.geom.canon_rot_or,
            canon_vec2=rai.geom.canon_micron,
            ))

