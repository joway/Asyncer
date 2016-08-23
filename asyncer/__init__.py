import logging

from .asyncer import Asyncer
from .timer import Timer

asyncer = Asyncer()
timer = Timer()

logging = logging.basicConfig(level=logging.WARN)
