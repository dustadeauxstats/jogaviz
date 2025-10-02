import pytest
from lxml import etree
from jogaviz_core.render.directives import (
    InvalidType,
    handle_bind,
    handle_attr,
    handle_if,
    handle_repeat,
)
from jogaviz_core.render.context import RenderContext, SymbolNotFound


def test_handle_bind_replaces_text() -> None:
    elem = etree.Element("text", attrib={"data-bind": "team.name"})
    ctx = RenderContext({"team": {"name": "Red Star FC"}})

    handle_bind(elem, ctx)

    assert elem.text == "Red Star FC"
    assert "data-bind" not in elem.attrib


def test_handle_bind_missing_field() -> None:
    elem = etree.Element("text", attrib={"data-bind": "missing_field"})
    ctx = RenderContext({"team": {"name": "Red Star FC"}})

    with pytest.raises(SymbolNotFound):
        handle_bind(elem, ctx)


def test_handle_bind_with_function() -> None:
    elem = etree.Element("text", attrib={"data-bind": "uppercase(team.name)"})
    ctx = RenderContext({"team": {"name": "Red Star FC"}})

    handle_bind(elem, ctx)

    assert elem.text == "RED STAR FC"
    assert "data-bind" not in elem.attrib


def test_handle_bind_with_nested_function() -> None:
    elem = etree.Element(
        "text", attrib={"data-bind": "truncate(uppercase(team.name), 7)"}
    )
    ctx = RenderContext({"team": {"name": "Red Star FC"}})

    handle_bind(elem, ctx)

    assert elem.text == "RED STA..."
    assert "data-bind" not in elem.attrib


def test_handle_attr_sets_attributes() -> None:
    elem = etree.Element(
        "rect", attrib={"data-attr": "color: team.color; stroke: team.border"}
    )
    ctx = RenderContext({"team": {"color": "blue", "border": "black"}})

    handle_attr(elem, ctx)

    assert elem.attrib["color"] == "blue"
    assert elem.attrib["stroke"] == "black"
    assert "data-attr" not in elem.attrib


def test_handle_attr_partial_missing_field() -> None:
    elem = etree.Element(
        "rect", attrib={"data-attr": "color: team.color; stroke: team.border"}
    )
    ctx = RenderContext({"team": {"color": "blue"}})

    with pytest.raises(SymbolNotFound):
        handle_attr(elem, ctx)


def test_handle_if_removes_element() -> None:
    parent = etree.Element("svg")
    elem = etree.SubElement(parent, "circle", attrib={"data-if": "team.active"})
    ctx = RenderContext({"team": {"active": False}})

    handle_if(elem, ctx)

    assert len(parent) == 0


def test_handle_if_keeps_element() -> None:
    parent = etree.Element("svg")
    elem = etree.SubElement(parent, "circle", attrib={"data-if": "team.active"})
    ctx = RenderContext({"team": {"active": True}})

    handle_if(elem, ctx)

    assert len(parent) == 1
    assert parent[0] is elem
    assert "data-if" not in elem.attrib


def test_handle_if_missing_field() -> None:
    parent = etree.Element("svg")
    elem = etree.SubElement(parent, "circle", attrib={"data-if": "team.missing_field"})
    ctx = RenderContext({"team": {"active": True}})

    with pytest.raises(SymbolNotFound):
        handle_if(elem, ctx)


def test_handle_if_invalid_type() -> None:
    parent = etree.Element("svg")
    elem = etree.SubElement(parent, "circle", attrib={"data-if": "team.name"})
    ctx = RenderContext({"team": {"name": "Red Star FC"}})

    with pytest.raises(InvalidType):
        handle_if(elem, ctx)


def test_handle_repeat_creates_elements() -> None:
    root = etree.Element("svg")
    parent = etree.SubElement(root, "g", attrib={"data-repeat": "teams"})
    etree.SubElement(
        parent,
        "text",
        attrib={
            "data-bind": "name",
            "data-attr": "y: index * 20 + 20",
        },
    )
    ctx = RenderContext(
        {
            "teams": [
                {"name": "Red Star FC"},
                {"name": "Paris FC"},
            ]
        }
    )

    handle_repeat(parent, ctx)

    assert len(parent) == 2
    assert parent[0].text == "Red Star FC"
    assert parent[0].attrib["y"] == "20"
    assert parent[1].text == "Paris FC"
    assert parent[1].attrib["y"] == "40"
    assert "data-repeat" not in parent[0].attrib
    assert "data-repeat" not in parent[1].attrib


def test_handle_repeat_missing_field() -> None:
    parent = etree.Element("svg")
    elem = etree.SubElement(parent, "g", attrib={"data-repeat": "missing_field"})
    ctx = RenderContext({"teams": [{"name": "Red Star FC"}]})

    with pytest.raises(SymbolNotFound):
        handle_repeat(elem, ctx)


def test_handle_repeat_missing_item_field() -> None:
    root = etree.Element("svg")
    parent = etree.SubElement(root, "g", attrib={"data-repeat": "teams"})
    etree.SubElement(parent, "text", attrib={"data-bind": "missing_field"})
    ctx = RenderContext(
        {
            "teams": [
                {"name": "Red Star FC"},
            ]
        }
    )

    with pytest.raises(SymbolNotFound):
        handle_repeat(parent, ctx)


def test_handle_repeat_empty_list() -> None:
    root = etree.Element("svg")
    parent = etree.SubElement(root, "g", attrib={"data-repeat": "teams"})
    ctx = RenderContext({"teams": []})

    handle_repeat(parent, ctx)

    assert len(parent) == 0


def test_handle_repeat_invalid_type() -> None:
    parent = etree.Element("svg")
    elem = etree.SubElement(parent, "text", attrib={"data-repeat": "team.name"})
    ctx = RenderContext({"team": {"name": "Red Star FC"}})

    with pytest.raises(InvalidType):
        handle_repeat(elem, ctx)
