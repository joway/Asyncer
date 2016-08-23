import unittest
from time import sleep

from asyncer import asyncer
from asyncer import calendar
from asyncer.decorator import calendar_task


def func_add(a, b):
    return a + b


def callback(func_return):
    print('callback: ' + str(func_return))


@calendar_task(callback, 1)
def func_dec(a, b):
    return a + b


@calendar_task(callback, 2)
def func_dec2(a, b):
    return a - b


class AysncerTest(unittest.TestCase):
    def callback(self, func_return):
        print(func_return)

    def setUp(self):
        self.asyncer = asyncer
        self.calendar = calendar
        self._func_add = func_add

    def wait_for_asyncer(self):
        while self.asyncer.size() > 0:
            pass

    def wait_for_calendar(self):
        count = 1
        while count <= 10:
            sleep(1)
            print('第%s秒' % count)
            count += 1

    def test_with_callback_and_return(self):
        self.asyncer.task(self._func_add, self.callback, 1, 2)
        self.wait_for_asyncer()

    def test_with_decorator(self):
        func_dec(3, 5)
        func_dec2(3, 5)
        self.wait_for_calendar()

    def test_calendar(self):
        self.calendar.task(self._func_add, self.callback, 1, 4, 6)
        self.calendar.task(self._func_add, self.callback, 2, 3, 9)
        self.calendar.task(self._func_add, self.callback, 3, 5, 19)
        self.wait_for_calendar()
