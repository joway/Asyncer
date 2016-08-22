import logging
import queue
import threading

logging.basicConfig(level=logging.INFO)


class Asyncer(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self._task_queue = queue.Queue()
        # daemon线程无法等待,会在主线程终止时自动销毁
        self._running = True
        self.start()

    def task(self, function, callback, *args, **kwargs):
        logging.info('Task ' + function.__name__ + ' has been added to the queue .')
        self._task_queue.put({
            'function': function,
            'callback': callback,
            'args': args,
            'kwargs': kwargs
        })

    def terminate(self):
        self._running = False

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

    def global_callback(self, func, func_return):
        logging.info('Task ' + func.__name__ + ' returns : ' + str(func_return))
