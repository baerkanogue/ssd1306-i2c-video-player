from time import time_ns
from typing import Callable, TypeVar, ParamSpec
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")


def print_execution_time(func: Callable[P, R]) -> Callable[P, R]:

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time: int = time_ns()

        result: R = func(*args, **kwargs)

        total_time: float = (time_ns() - start_time) / 1e9
        print(f"{func.__name__} executed in: {total_time:.3f} seconds.")
        return result

    return wrapper
