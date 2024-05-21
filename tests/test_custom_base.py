"""
Test the custom_base helper
"""

import unittest
import re

import raimad as rai

class TestCustomBase(unittest.TestCase):

    def test_custom_base(self):
        self.assertEqual(
            rai.custom_base(69420, ['0', '1']),
            bin(69420).lstrip('0b')
            )

        self.assertEqual(
            rai.custom_base(10, list('0123456789abcdef')),
            hex(10).lstrip('0x')
            )

        self.assertEqual(
            rai.custom_base(16, list('0123456789abcdef')),
            hex(16).lstrip('0x')
            )

        self.assertEqual(
            rai.custom_base(69420, list('0123456789abcdef')),
            hex(69420).lstrip('0x')
            )


if __name__ == '__main__':
    unittest.main()

