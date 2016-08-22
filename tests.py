import unittest

from asyncer.asyncer import Asyncer


def func_add(a, b):
    return a + b


def func_b():
    print('No data')


def func_c():
    pass


class AysncerTest(unittest.TestCase):
    def callback(self, func_return):
        print(func_return)

    def setUp(self):
        self.asyncer = Asyncer()
        self._func_add = func_add
        self._func_b = func_b

    def setDown(self):
        while self.asyncer.size() > 0:
            pass

    def test_with_callback_and_return(self):
        self.asyncer.task(self._func_add, self.callback, 1, 2)

        # def test_with_no_args(self):
        #     self.asyncer.task(self._func_b, self.callback)
