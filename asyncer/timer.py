import datetime
from time import sleep

from asyncer import logging
from .thread import DaemonThread


class Timer(DaemonThread):
    def __init__(self):
        self._task_list = []
        super().__init__()

    def push_to_list(self, task):
        self._task_list.append(task)
        self._task_list.sort(key=lambda t: t['next_exec_time'], reverse=True)

    def sync_next_exec_time(self, microseconds=0, seconds=0):
        for i in self._task_list:
            i['next_exec_time'] -= datetime.timedelta(microseconds=microseconds, seconds=seconds)

    def task(self, function, callback, interval, *args, **kwargs):
        logging.info('Task ' + function.__name__ + ' has been added to the queue .')
        self.push_to_list({
            'function': function,
            'callback': callback,
            'interval': interval,
            'next_exec_time': datetime.datetime.now() + datetime.timedelta(seconds=interval),
            'args': args,
            'kwargs': kwargs
        })

    def run(self):
        while self._running:
            if self._task_list:
                if self._task_list[-1]['next_exec_time'] > datetime.datetime.now():
                    sleep(1)
                    continue
                # 执行 next_exec_time 最近的一次任务
                task = self._task_list.pop()

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

                # 步进当前任务队列
                task['next_exec_time'] += datetime.timedelta(seconds=task['interval'])
                self.push_to_list(task)
                logging.info('Task ' + function.__name__ + ' done')

    def size(self):
        return len(self._task_list)
