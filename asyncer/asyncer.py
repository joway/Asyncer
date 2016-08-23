import logging
import queue
from asyncer.thread import DaemonThread


class Asyncer(DaemonThread):
    def __init__(self):
        self._task_queue = queue.Queue()
        super().__init__()

    def task(self, function, callback, *args, **kwargs):
        logging.info('Task ' + function.__name__ + ' has been added to the queue .')
        self._task_queue.put({
            'function': function,
            'callback': callback,
            'args': args,
            'kwargs': kwargs
        })

    def run(self):
        while self._running:
            # get 为 阻塞函数
            task = self._task_queue.get()
            function = task.get('function')
            callback = task.get('callback')
            args = task.get('args')
            kwargs = task.get('kwargs')
            try:
                if callback:
                    func_return = function(*args, **kwargs)
                    callback(func_return)
                    self.global_callback(function, func_return)
            except Exception as e:
                logging.error(e)
            self._task_queue.task_done()
            logging.info('Task ' + function.__name__ + ' done')

    def size(self):
        return self._task_queue.qsize()


