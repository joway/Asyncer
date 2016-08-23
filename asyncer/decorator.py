from . import timer, asyncer


def asyncer_task(callback):
    def decorator(func):
        def wrapper(*args, **kwargs):
            asyncer.task(func, callback, *args, **kwargs)

        return wrapper

    return decorator


def timer_task(callback, interval=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            timer.task(func, callback, interval, *args, **kwargs)

        return wrapper

    return decorator
