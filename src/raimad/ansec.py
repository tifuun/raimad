from math import radians

try:
    from typing import Self
except ImportError:
    # py3.10 and lower
    from typing_extensions import Self

import raimad as rai

class AnSecError(Exception):
    pass

class AnSecRadiusError(AnSecError):
    pass

class AnSecRadiusTooManyArgumentsError(AnSecRadiusError):
    pass

class AnSecRadiusNotEnoughArgumentsError(AnSecRadiusError):
    pass

class AnSecRadiusIncorrectArgumentsError(AnSecRadiusError):
    pass

class AnSecThetaError(AnSecError):
    pass

class AnSecThetaTooManyArgumentsError(AnSecThetaError):
    pass

class AnSecThetaNotEnoughArgumentsError(AnSecThetaError):
    pass

class AnSecThetaIncorrectArgumentsError(AnSecThetaError):
    pass

class AnSec(rai.Compo):
    """
    Annular Sector

    A polygon approximating an annular sector,
    or, in working men's terms, a "pizza crust".
    There are many possible ways to define an AnSec;
    # TODO examples
    """

    browser_tags = ["builtin", "polygon"]

    class Options:
        r1 = rai.Option("Inner radius", browser_default=18)
        r2 = rai.Option("Outter radius", browser_default=20)
        theta1 = rai.Option("Angle 1", browser_default=radians(45))
        theta2 = rai.Option("Angle 2", browser_default=radians(90))

    def _make(
            self,
            r1: float,
            r2: float,
            theta1: float,
            theta2: float,
            num_points: int = 100,
            ) -> None:

        if abs(r1 - r2) < rai.epsilon:
            self.geoms.update({'root': [[]]})
            return

        theta_step = (theta2 - theta1) / num_points
        angles = tuple(theta1 + theta_step * i for i in range(num_points + 1))

        self.geoms.update({
            'root': [
                [
                    rai.polar(arg=angle, mod=radius)
                    for radius, angles in (
                        (r1, angles),
                        (r2, angles[::-1]),
                        # Fun exercise: change the above two tuples to lists
                        # and see what mypy has to say about that
                        )
                    for angle in angles
                    ]
                ]
            })

    @classmethod
    def from_auto(
            cls,
            r1: float | None = None,
            r2: float | None = None,
            rmid: float | None = None,
            dr: float | None = None,
            theta1: float | None = None,
            theta2: float | None = None,
            thetamid: float | None = None,
            dtheta: float | None = None,
            num_points: int = 100,
            ) -> Self:

        r1, r2 = cls.interpret_radius(r1, r2, rmid, dr)
        theta1, theta2 = cls.interpret_theta(
            theta1,
            theta2,
            thetamid,
            dtheta,
            )

        return cls(r1, r2, theta1, theta2, num_points)

    @staticmethod
    def interpret_radius(
            r1: float | None,
            r2: float | None,
            rmid: float | None,
            dr: float | None,
            ) -> tuple[float, float]:

        if r1 is None and r2 is None and rmid is None and dr is None:
            raise AnSecRadiusNotEnoughArgumentsError(
                "No radius specified"
                )

        if r1 is None and r2 is None and rmid is None and dr is not None:
            raise AnSecRadiusNotEnoughArgumentsError(
                "Radius delta specified, but no r1 or r2"
                )

        if r1 is None and r2 is None and rmid is not None and dr is None:
            raise AnSecRadiusNotEnoughArgumentsError(
                "Midradius specified, but no radius delta"
                )

        if r1 is None and r2 is None and rmid is not None and dr is not None:
            return rmid - dr / 2, rmid + dr / 2

        if r1 is None and r2 is not None and rmid is None and dr is None:
            raise AnSecRadiusNotEnoughArgumentsError(
                "r2 specified, but no r1 or radius delta"
                )

        if r1 is None and r2 is not None and rmid is None and dr is not None:
            return r2 - dr, r2

        if r1 is None and r2 is not None and rmid is not None and dr is None:
            raise AnSecRadiusIncorrectArgumentsError(
                "r2 and midradius specified. "
                "What do you want me to do??"
                )

        if r1 is None and r2 is not None and rmid is not None and \
                dr is not None:
            raise AnSecRadiusTooManyArgumentsError(
                "r2, midradius, and radius delta specified. "
                "You need only two of these!"
                )

        if r1 is not None and r2 is None and rmid is None and dr is None:
            raise AnSecRadiusNotEnoughArgumentsError(
                "Only r1 specified. "
                "Specify radius delta or r2."
                )

        if r1 is not None and r2 is None and rmid is None and dr is not None:
            return r1, r1 + dr

        if r1 is not None and r2 is None and rmid is not None and dr is None:
            raise AnSecRadiusIncorrectArgumentsError(
                "R1 and midradius specified. "
                "What do you want me to do??"
                )

        if r1 is not None and r2 is None and rmid is not None and \
                dr is not None:
            raise AnSecRadiusTooManyArgumentsError(
                "r1, midradius, and radius delta specified. "
                "You need only two of these!"
                )

        if r1 is not None and r2 is not None and rmid is None and dr is None:
            return r1, r2

        if r1 is not None and r2 is not None and rmid is None and dr \
                is not None:
            raise AnSecRadiusTooManyArgumentsError(
                "r1, r2, and radius delta specified. "
                "What do you want me to do??"
                )

        if r1 is not None and r2 is not None and rmid is not None and \
                dr is None:
            raise AnSecRadiusTooManyArgumentsError(
                "r1, r2, and midradius specified. "
                "What do you want me to do??"
                )

        raise AnSecRadiusTooManyArgumentsError(
                "What do you want me to do??"
                )

    @staticmethod
    def interpret_theta(
            t1: float | None,
            t2: float | None,
            tmid: float | None,
            dt: float | None,
            ) -> tuple[float, float]:

        if t1 is None and t2 is None and tmid is None and dt is None:
            raise AnSecThetaNotEnoughArgumentsError(
                "No Theta specified"
                )

        if t1 is None and t2 is None and tmid is None and dt is not None:
            raise AnSecThetaNotEnoughArgumentsError(
                "Theta delta specified, but no t1 or t2"
                )

        if t1 is None and t2 is None and tmid is not None and dt is None:
            raise AnSecThetaNotEnoughArgumentsError(
                "MidTheta specified, but no Theta delta"
                )

        if t1 is None and t2 is None and tmid is not None and dt is not None:
            return tmid - dt / 2, tmid + dt / 2

        if t1 is None and t2 is not None and tmid is None and dt is None:
            raise AnSecThetaNotEnoughArgumentsError(
                "t2 specified, but no t1 or Theta delta"
                )

        if t1 is None and t2 is not None and tmid is None and dt is not None:
            return t2 - dt, t2

        if t1 is None and t2 is not None and tmid is not None and dt is None:
            raise AnSecThetaIncorrectArgumentsError(
                "t2 and midTheta specified. "
                "What do you want me to do??"
                )

        if t1 is None and t2 is not None and tmid is not None and \
                dt is not None:
            raise AnSecThetaTooManyArgumentsError(
                "t2, midTheta, and Theta delta specified. "
                "You need only two of these!"
                )

        if t1 is not None and t2 is None and tmid is None and dt is None:
            raise AnSecThetaNotEnoughArgumentsError(
                "Only t1 specified. "
                "Specify Theta delta or t2."
                )

        if t1 is not None and t2 is None and tmid is None and dt is not None:
            return t1, t1 + dt

        if t1 is not None and t2 is None and tmid is not None and dt is None:
            raise AnSecThetaIncorrectArgumentsError(
                "t1 and midTheta specified. "
                "What do you want me to do??"
                )

        if t1 is not None and t2 is None and tmid is not None and \
                dt is not None:
            raise AnSecThetaTooManyArgumentsError(
                "t1, midTheta, and Theta delta specified. "
                "You need only two of these!"
                )

        if t1 is not None and t2 is not None and tmid is None and dt is None:
            return t1, t2

        if t1 is not None and t2 is not None and tmid is None and \
                dt is not None:
            raise AnSecThetaTooManyArgumentsError(
                "t1, t2, and Theta delta specified. "
                "What do you want me to do??"
                )

        if t1 is not None and t2 is not None and tmid is not None and \
                dt is None:
            raise AnSecThetaTooManyArgumentsError(
                "t1, t2, and midTheta specified. "
                "What do you want me to do??"
                )

        raise AnSecThetaTooManyArgumentsError(
                "What do you want me to do??"
                )

