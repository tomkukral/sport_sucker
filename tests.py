from unittest import main
from unittest import TestCase


class DummyTest(TestCase):
    """Check testing framework is working"""

    def test_dummy(self):
        self.assertTrue(True)


if __name__ == '__main__':
    main()
