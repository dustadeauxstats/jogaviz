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
    expr = elem.attrib.pop("data-repeat")
    if not expr:
        return

    items = safe_eval(str(expr), ctx)

    if not isinstance(items, list):
        raise InvalidType(
            f"Expression for {DirectiveType.REPEAT.value} must be a list."
        )

    template_children = [copy.deepcopy(child) for child in elem]

    for child in list(elem):
        elem.remove(child)

    for idx, item in enumerate(items):
        merged_env = {**ctx.env, **item, "index": idx}
        new_ctx = RenderContext(merged_env)

        for template_child in template_children:
            clone = copy.deepcopy(template_child)
            from .engine import render_element

            render_element(clone, new_ctx)
            elem.append(clone)


# Register directives
register_directive(DirectiveType.BIND, handle_bind)
register_directive(DirectiveType.ATTR, handle_attr)
register_directive(DirectiveType.IF, handle_if)
register_directive(DirectiveType.REPEAT, handle_repeat)
