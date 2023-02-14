"""
Circle polygon
"""

import numpy as np

from PyCIF.draw.Polygon import Polygon

# TODO remove these methods from Polygon class


class Circle(Polygon):
    @classmethod
    def create_radius(cls, radius):
        """
        Make circle from radius
        """
        points = 100
        circle = 2 * np.pi
        increment = circle / points

        return cls(np.array([
            (
                np.cos(angle) * radius,
                np.sin(angle) * radius,
            )
            for angle in np.arange(0, circle, increment)
            ]))

    @classmethod
    def create_sector(cls, radius, initial_angle, final_angle):
        """
        Make circle from radius
        """
        points = 100
        arclength = final_angle - initial_angle
        increment = arclength / points

        return cls(np.array([
            (
                np.cos(angle) * radius,
                np.sin(angle) * radius,
            )
            for angle in np.arange(initial_angle, final_angle, increment)
            ]))

    @classmethod
    def create_arc(cls, radius1, radius2, initial_angle, final_angle):
        """
        Make circle from radius
        """
        points = 200
        arclength = final_angle - initial_angle
        increment = arclength / (points / 2)

        print(initial_angle, final_angle)
        points = np.arange(initial_angle, final_angle, increment)

        return cls(np.array([
            (
                np.cos(-angle + 0.5 * np.pi) * radius,
                np.sin(-angle + 0.5 * np.pi) * radius,
            )
            for radius in (radius1, radius2)
            for angle in [points, reversed(points)][radius is radius1]
            ]))

