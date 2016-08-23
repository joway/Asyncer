import logging
import threading


class DaemonThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self._running = True
        self.start()

    def terminate(self):
        self._running = False

    def global_callback(self, func, func_return):
        logging.info('Task ' + func.__name__ + ' returns : ' + str(func_return))
