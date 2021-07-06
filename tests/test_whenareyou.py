import unittest

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
        # tbd
        pass
        
    def test_whenareyou_IATA(self):
        # tbd
        pass



if __name__ == '__main__':
    unittest.main()
