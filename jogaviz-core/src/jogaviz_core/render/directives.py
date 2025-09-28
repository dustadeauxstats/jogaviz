from typing import Callable
import copy
from enum import Enum
from lxml import etree
from jogaviz_core.render.context import RenderContext, safe_eval


class InvalidType(Exception):
    pass


class DirectiveType(str, Enum):
    BIND = "data-bind"
    ATTR = "data-attr"
    STYLE = "data-style"
    IF = "data-if"
    REPEAT = "data-repeat"


DirectiveHandler = Callable[[etree._Element, RenderContext], None]
DIRECTIVES: dict[DirectiveType, DirectiveHandler] = {}


def register_directive(kind: DirectiveType, handler: DirectiveHandler) -> None:
    DIRECTIVES[kind] = handler


def handle_bind(elem: etree._Element, ctx: RenderContext) -> None:
    field = elem.attrib.pop(DirectiveType.BIND.value)
    if not field:
        return
    elem.text = str(safe_eval(str(field), ctx))


def handle_attr(elem: etree._Element, ctx: RenderContext) -> None:
    attr_exprs = elem.attrib.pop(DirectiveType.ATTR.value)
    if not attr_exprs:
        return
    for pair in str(attr_exprs).split(";"):
        if not pair.strip():
            continue
        attr, expr = pair.split(":", 1)
        attr = attr.strip()
        expr = expr.strip()
        elem.set(attr, str(safe_eval(str(expr), ctx)))


def handle_if(elem: etree._Element, ctx: RenderContext) -> None:
    expr = elem.attrib.pop(DirectiveType.IF.value)
    if not expr:
        return
    keep = safe_eval(str(expr), ctx)
    if not isinstance(keep, bool):
        raise InvalidType(
            f"Expression for {DirectiveType.IF.value} must evaluate to a boolean."
        )
    if not keep:
        parent = elem.getparent()
        if parent is not None:
            parent.remove(elem)


def handle_repeat(elem: etree._Element, ctx: RenderContext) -> None:
    list_expr = elem.attrib.pop(DirectiveType.REPEAT.value)
    if not list_expr:
        return

    items = safe_eval(str(list_expr), ctx)
    if not isinstance(items, list):
        raise InvalidType(
            f"Expression for {DirectiveType.REPEAT.value} must evaluate to a list."
        )
    parent = elem.getparent()
    if parent is None:
        return
    template = copy.deepcopy(elem)
    parent.remove(elem)

    for i, item in enumerate(items):
        new_elem = copy.deepcopy(template)
        item_ctx = RenderContext({**item, "@index": i, **ctx.data})
        for directive, handler in DIRECTIVES.items():
            if directive.value in new_elem.attrib:
                handler(new_elem, item_ctx)
        parent.append(new_elem)


# Register directives
register_directive(DirectiveType.BIND, handle_bind)
register_directive(DirectiveType.ATTR, handle_attr)
register_directive(DirectiveType.IF, handle_if)
register_directive(DirectiveType.REPEAT, handle_repeat)
