from typing import Callable

FunctionType = Callable[..., str]
FUNCTIONS: dict[str, FunctionType] = {}


def register_function(name: str, func: FunctionType) -> None:
    FUNCTIONS[name] = func


def percentage(v: float, digits: int = 2) -> str:
    return f"{v * 100:.{digits}f}%"


def round(v: float, digits: int = 2) -> str:
    return f"{v:.{digits}f}"


def capitalize(v: str) -> str:
    if not v:
        return v
    return v[0].upper() + v[1:]


def uppercase(v: str) -> str:
    return v.upper()


def truncate(v: str, length: int) -> str:
    if len(v) <= length:
        return v
    return v[:length] + "..."


def abbreviate_name(v: str, keep_first: bool = True) -> str:
    parts = v.split()
    if len(parts) <= 1:
        return v
    if keep_first:
        return parts[0] + " " + " ".join(p[0].upper() + "." for p in parts[1:])
    return " ".join(p[0].upper() + "." for p in parts[:-1]) + " " + parts[-1]


register_function("percentage", percentage)
register_function("round", round)
register_function("capitalize", capitalize)
register_function("uppercase", uppercase)
register_function("truncate", truncate)
register_function("abbreviate_name", abbreviate_name)
