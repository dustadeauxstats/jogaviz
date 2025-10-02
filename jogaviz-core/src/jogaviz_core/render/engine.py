from typing import Any
from lxml import etree
from jogaviz_core.render.context import RenderContext
from jogaviz_core.render.directives import DIRECTIVES


def render_element(elem: etree._Element, ctx: RenderContext) -> None:
    for directive, handler in DIRECTIVES.items():
        if directive in elem.attrib:
            handler(elem, ctx)

    for child in list(elem):
        render_element(child, ctx)


def render(svg_content: str, data: dict[str, Any]) -> str:
    ctx = RenderContext(data)
    root = etree.fromstring(svg_content.encode("utf-8"))
    render_element(root, ctx)
    return etree.tostring(root, encoding="utf-8").decode("utf-8")
