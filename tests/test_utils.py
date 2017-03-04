import unittest

from jobber.utils import format_ms

class FormatMsTests(unittest.TestCase):
    def test_format_ms(self):
        test_string = '13 second(s) 13 millisecond(s)'
        test_ms = 13013
        self.assertTrue(format_ms(test_ms) == test_string)

        test_string = '1 day(s)'
        test_ms = 86400000
        self.assertTrue(format_ms(test_ms) == test_string)
