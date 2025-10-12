from lxml import etree
from .context import RenderContext, safe_eval

COMPONENTS: dict[str, etree._Element] = {}


def parse_props(expr: str, ctx: RenderContext) -> dict[str, object]:
    props: dict[str, object] = {}
    if not expr:
        return props
    for pair in str(expr).split(";"):
        if not pair.strip():
            continue
        key, value_expr = pair.split(":", 1)
        key = key.strip()
        value_expr = value_expr.strip()
        props[key] = safe_eval(str(value_expr), ctx)
    return props
