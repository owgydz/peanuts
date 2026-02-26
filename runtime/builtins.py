import math
import time
from .io import peanut_print, peanut_input, peanut_debug, peanut_error


def build_builtins():
    return {
        "print": peanut_print,
        "input": peanut_input,
        "debug": peanut_debug,
        "error": peanut_error,
        "len": len,
        "range": range,

        # Stdlib backend hooks
        "__peanut_math_add": lambda a, b: a + b,
        "__peanut_math_sqrt": math.sqrt,
        "__peanut_time_now": time.time,
        "__peanut_str_upper": lambda s: str(s).upper(),
        "__peanut_str_lower": lambda s: str(s).lower(),
    }