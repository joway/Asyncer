import logging

from .asyncer import Asyncer
from .calendar import Calendar

asyncer = Asyncer()
calendar = Calendar()

logging = logging.basicConfig(level=logging.WARN)
