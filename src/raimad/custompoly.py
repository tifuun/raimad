import raimad as rai

class CustomPolyException(Exception):
    pass

# TODO tests
class CustomPoly(rai.Compo):
    """
    Custom Polygon

    A polygon that you can defined on-the fly!
    #TODO add example
    """
    browser_tags = ["builtin", "polygon"]

    class Options:
        points = rai.Option(
            "A list of points for the polygon",
            browser_default=[
                [0, 0],
                [10, 0],
                [10, 20],
                [20, -20],
                ]
            )

    def _make(self, points):
        processed_points = []
        for point in points:
            match point:
                case (
                        str() as mark_name,
                        (float() | int(), float() | int()) as point
                        ):
                    self.marks[mark_name] = point

                case (float() | int(), float() | int()) as point:
                    # Very confusing,
                    # when it comes to type annotations,
                    # `int` is treated as a subset of `float`,
                    # but in structural pattern matching,
                    # an `int` is not a `float`.
                    pass

                case _:
                    raise CustomPolyException(
                        "I have no clue what you want me to do with "
                        f"`{point}`"
                        )
            processed_points.append(point)
            # TODO would be cool to make it possible to
            # specify coordinates relative to the previous
            # point as opposed to absolute.

        self.geoms.update({'root': [processed_points]})

