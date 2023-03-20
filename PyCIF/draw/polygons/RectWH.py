"""
width-height Rectangle
"""

import numpy as np

import PyCIF as pc


class RectWH(pc.Polygon):

    def __init__(self, width: float, height: float):
        super().__init__()
        self.width = width
        self.height = height

        self._add_mark(
            'top_left',
            pc.point(
                self.width * 0,
                self.height * 1,
                ),
            'X-.-.  \n'
            '| | |  \n'
            '. . .  \n'
            '| | |  \n'
            '.-.-.  '
            )

        self._add_mark(
            'top_mid',
            pc.point(
                self.width * 0.5,
                self.height * 1,
                ),
            '.-X-.  \n'
            '| | |  \n'
            '. . .  \n'
            '| | |  \n'
            '.-.-.  '
            )

        self._add_mark(
            'top_right',
            pc.point(
                self.width * 1,
                self.height * 1,
                ),
            '.-.-X  \n'
            '| | |  \n'
            '. . .  \n'
            '| | |  \n'
            '.-.-.  '
            )

        self._add_mark(
            'mid_left',
            pc.point(
                self.width * 0,
                self.height * 0.5,
                ),
            '.-.-.  \n'
            '| | |  \n'
            'X . .  \n'
            '| | |  \n'
            '.-.-.  '
            )

        self._add_mark(
            'mid',
            pc.point(
                self.width * 0.5,
                self.height * 0.5,
                ),
            '.-.-.  \n'
            '| | |  \n'
            '. X .  \n'
            '| | |  \n'
            '.-.-.  '
            )

        self._add_mark(
            'mid_right',
            pc.point(
                self.width * 1,
                self.height * 0.5,
                ),
            '.-.-.  \n'
            '| | |  \n'
            '. . X  \n'
            '| | |  \n'
            '.-.-.  '
            )

        self._add_mark(
            'bottom_left',
            pc.point(
                self.width * 0,
                self.height * 0,
                ),
            '.-.-.  \n'
            '| | |  \n'
            '. . .  \n'
            '| | |  \n'
            'X-.-.  '
            )

        self._add_mark(
            'bottom_mid',
            pc.point(
                self.width * 0.5,
                self.height * 0,
                ),
            '.-.-.  \n'
            '| | |  \n'
            '. . .  \n'
            '| | |  \n'
            '.-X-.  '
            )

        self._add_mark(
            'bottom_right',
            pc.point(
                self.width * 1,
                self.height * 0,
                ),
            '.-.-.  \n'
            '| | |  \n'
            '. . .  \n'
            '| | |  \n'
            '.-.-X  '
            )

    def _get_xyarray(self) -> np.ndarray:
        return np.array(
            (
                (0, 0),
                (self.width, 0),
                (self.width, self.height),
                (0, self.height),
                ),
            dtype=np.float64,
            )


