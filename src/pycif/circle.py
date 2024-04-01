import numpy as np
import pycif as pc

class Circle(pc.Compo):
    def _make(self, radius, num_points=200):

        self.geoms.update({
            'root': [
                np.array([
                    pc.polar(angle, radius)
                    for angle
                    in np.linspace(0, 2 * np.pi, num_points)
                    ])
                ]
            })

        self.marks.center = (0, 0)

