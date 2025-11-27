from functools import reduce
from typing import Any, Callable

type Composable = Callable[[Any], Any]

def compose(*functions) -> Composable:
    def apply(arg: Any, fn: Composable) -> Any:
        return fn(arg)
    return lambda x: reduce(apply, functions, x)