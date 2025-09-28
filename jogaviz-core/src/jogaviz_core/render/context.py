from typing import Any
from simpleeval import simple_eval, NameNotDefined, AttributeDoesNotExist


class RenderContext:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data
        self.env = data.copy()


class SymbolNotFound(Exception):
    pass


def safe_eval(expr: str, ctx: RenderContext) -> Any:
    try:
        return simple_eval(expr, names=ctx.env)
    except NameNotDefined as e:
        raise SymbolNotFound(f"Name not defined in expression '{expr}': {e}") from e
    except AttributeDoesNotExist as e:
        raise SymbolNotFound(
            f"Attribute does not exist in expression '{expr}': {e}"
        ) from e
