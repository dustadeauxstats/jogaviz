from jogaviz_core.render.components import parse_props
from jogaviz_core.render.context import RenderContext


def test_parse_scalar_props() -> None:
    ctx = RenderContext({"a": 10, "b": 20})
    expr = "x: a + b; y: a * b ; z: 'test'; empty: '' ; spaced :  42"
    props = parse_props(expr, ctx)
    assert props == {
        "x": 30,
        "y": 200,
        "z": "test",
        "empty": "",
        "spaced": 42,
    }


def test_parse_object_props() -> None:
    ctx = RenderContext({"player": {"name": "Vino", "age": 30}})
    expr = "player_name: player.name; age_next_year: player.age + 1"
    props = parse_props(expr, ctx)
    assert props == {
        "player_name": "Vino",
        "age_next_year": 31,
    }
