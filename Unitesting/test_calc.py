import unittest
import calc


class Test(unittest.TestCase):

    # Every time before every test
    def setUp(self):
        pass

    # Every time after every test
    def tearDown(self):
        pass

    def test_add(self):
        self.assertEqual(calc.add(10, 5), 15)
        self.assertEqual(calc.add(-1, 1), 0)
        self.assertEqual(calc.add(-1, -1), -2)

    def test_sub(self):
        self.assertEqual(calc.sub(10, 5), 5)
        self.assertEqual(calc.sub(-1, 1), -2)
        self.assertEqual(calc.sub(-1, -1), -0 )

    def test_mupliply(self):
        self.assertEqual(calc.multiply(2, 1), 2)
        self.assertEqual(calc.multiply(-1, 1), -1)
        self.assertEqual(calc.multiply(-1, -1), 1)


if __name__ == '__main__':
    unittest.main()
