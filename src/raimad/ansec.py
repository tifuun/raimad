import numpy as np
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
        theta1 = rai.Option("Angle 1", browser_default=np.deg2rad(45))
        theta2 = rai.Option("Angle 2", browser_default=np.deg2rad(90))

    def _make(
            self,
            r1=None,
            r2=None,
            rmid=None,
            dr=None,
            theta1=None,
            theta2=None,
            thetamid=None,
            dtheta=None,
            orientation=None,
            ):

        r1, r2 = self.interpret_radius(r1, r2, rmid, dr)
        theta1, theta2 = self.interpret_theta(
            theta1,
            theta2,
            thetamid,
            dtheta,
            )

        if r1 == r2:  # TODO epsilon
            self.geoms.update({'root': [[]]})
            return

        angspace = rai.angspace(theta1, theta2, orientation=orientation)

        self.geoms.update({
            'root': [
                np.array([
                    rai.polar(arg=angle, mod=radius)
                    for radius, angles in [
                        [r1, angspace],
                        [r2, reversed(angspace)],
                        ]
                    for angle in angles
                    ])
                ]
            })

    @staticmethod
    def interpret_radius(r1, r2, rmid, dr):
        passed = (
            (r1 is not None) << 3 |
            (r2 is not None) << 2 |
            (rmid is not None) << 1 |
            (dr is not None) << 0
            )

        if passed == 0b0000:
            raise AnSecRadiusNotEnoughArgumentsError(
                "No radius specified"
                )

        if passed == 0b0001:
            raise AnSecRadiusNotEnoughArgumentsError(
                "Radius delta specified, but no r1 or r2"
                )

        if passed == 0b0010:
            raise AnSecRadiusNotEnoughArgumentsError(
                "Midradius specified, but no radius delta"
                )

        if passed == 0b0011:
            return rmid - dr / 2, rmid + dr / 2

        if passed == 0b0100:
            raise AnSecRadiusNotEnoughArgumentsError(
                "r2 specified, but no r1 or radius delta"
                )

        if passed == 0b0101:
            return r2 - dr, r2

        if passed == 0b0110:
            raise AnSecRadiusIncorrectArgumentsError(
                "r2 and midradius specified. "
                "What do you want me to do??"
                )

        if passed == 0b0111:
            raise AnSecRadiusTooManyArgumentsError(
                "r2, midradius, and radius delta specified. "
                "You need only two of these!"
                )

        if passed == 0b1000:
            raise AnSecRadiusNotEnoughArgumentsError(
                "Only r1 specified. "
                "Specify radius delta or r2."
                )

        if passed == 0b1001:
            return r1, r1 + dr

        if passed == 0b1010:
            raise AnSecRadiusIncorrectArgumentsError(
                "R1 and midradius specified. "
                "What do you want me to do??"
                )

        if passed == 0b1011:
            raise AnSecRadiusTooManyArgumentsError(
                "r1, midradius, and radius delta specified. "
                "You need only two of these!"
                )

        if passed == 0b1100:
            return r1, r2

        if passed == 0b1101:
            raise AnSecRadiusTooManyArgumentsError(
                "r1, r2, and radius delta specified. "
                "What do you want me to do??"
                )

        if passed == 0b1110:
            raise AnSecRadiusTooManyArgumentsError(
                "r1, r2, and midradius specified. "
                "What do you want me to do??"
                )

        if passed == 0b1111:
            raise AnSecRadiusTooManyArgumentsError(
                "What do you want me to do??"
                )

    @staticmethod
    def interpret_theta(t1, t2, tmid, dt):
        passed = (
            (t1 is not None) << 3 |
            (t2 is not None) << 2 |
            (tmid is not None) << 1 |
            (dt is not None) << 0
            )

        if passed == 0b0000:
            raise AnSecThetaNotEnoughArgumentsError(
                "No Theta specified"
                )

        if passed == 0b0001:
            raise AnSecThetaNotEnoughArgumentsError(
                "Theta delta specified, but no t1 or t2"
                )

        if passed == 0b0010:
            raise AnSecThetaNotEnoughArgumentsError(
                "MidTheta specified, but no Theta delta"
                )

        if passed == 0b0011:
            return tmid - dt / 2, tmid + dt / 2

        if passed == 0b0100:
            raise AnSecThetaNotEnoughArgumentsError(
                "t2 specified, but no t1 or Theta delta"
                )

        if passed == 0b0101:
            return t2 - dt, t2

        if passed == 0b0110:
            raise AnSecThetaIncorrectArgumentsError(
                "t2 and midTheta specified. "
                "What do you want me to do??"
                )

        if passed == 0b0111:
            raise AnSecThetaTooManyArgumentsError(
                "t2, midTheta, and Theta delta specified. "
                "You need only two of these!"
                )

        if passed == 0b1000:
            raise AnSecThetaNotEnoughArgumentsError(
                "Only t1 specified. "
                "Specify Theta delta or t2."
                )

        if passed == 0b1001:
            return t1, t1 + dt

        if passed == 0b1010:
            raise AnSecThetaIncorrectArgumentsError(
                "t1 and midTheta specified. "
                "What do you want me to do??"
                )

        if passed == 0b1011:
            raise AnSecThetaTooManyArgumentsError(
                "t1, midTheta, and Theta delta specified. "
                "You need only two of these!"
                )

        if passed == 0b1100:
            return t1, t2

        if passed == 0b1101:
            raise AnSecThetaTooManyArgumentsError(
                "t1, t2, and Theta delta specified. "
                "What do you want me to do??"
                )

        if passed == 0b1110:
            raise AnSecThetaTooManyArgumentsError(
                "t1, t2, and midTheta specified. "
                "What do you want me to do??"
                )

        if passed == 0b1111:
            raise AnSecThetaTooManyArgumentsError(
                "What do you want me to do??"
                )
