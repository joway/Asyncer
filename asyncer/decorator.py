from . import calendar


def asyncer_task(callback):
    def decorator(func):
        def wrapper(*args, **kwargs):
            asyncer.task(func, callback, *args, **kwargs)

        return wrapper

    return decorator


def calendar_task(callback, interval=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            calendar.task(func, callback, interval, *args, **kwargs)
        return wrapper

    return decorator
