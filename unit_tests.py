import unittest
from qrandom import QRandom


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.rng_obj = QRandom()

    def test_something(self):
        rng_range = 3
        min = 65535*rng_range
        max = 0

        for i in range(int(self.rng_obj)):
            tmp = self.rng_obj.get(max=(rng_range*65535))
            if tmp < min:
                min = tmp
            if tmp > max:
                max = tmp
            self.assertTrue(0 <= tmp <= (rng_range*65535))  # add assertion here
        print(f"0 <= {min} <= {max} <= {rng_range*65535}")


if __name__ == '__main__':
    unittest.main()
