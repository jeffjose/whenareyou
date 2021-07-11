import unittest

from zoneinfo import ZoneInfo
from whenareyou import whenareyou, whenareyou_IATA



class TestWhenareyou(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # to run before all tests
        print("\ntesting whenareyou.whenareyou...")

    @classmethod
    def tearDownClass(cls):
        # to run after all tests
        pass

    def setUp(self):
        # to run before each test
        pass
    def tearDown(self):
        # to run after each test
        pass

    def test_whenareyou(self):
        expected = ZoneInfo("Europe/Brussels")
        actual = whenareyou("Brussels, Europe")
        self.assertEqual(expected, actual)

        expected = ZoneInfo("Asia/Taipei")
        actual = whenareyou("Tainan")
        self.assertEqual(expected, actual)

        expected = ZoneInfo("America/Chicago")
        actual = whenareyou("Springfield")
        self.assertEqual(expected, actual)


    def test_whenareyou_IATA(self):
        expect = ZoneInfo("Asia/Novosibirsk")
        actual = whenareyou_IATA("OVB")
        self.assertEqual(expect, actual)





if __name__ == '__main__':
    unittest.main()