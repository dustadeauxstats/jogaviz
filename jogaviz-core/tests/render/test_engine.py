from jogaviz_core.render.engine import render


def test_render_simple_bind() -> None:
    svg = '<svg><text data-bind="team.name"></text></svg>'
    data = {"team": {"name": "Red Star FC"}}

    result = render(svg, data)

    assert "<text>Red Star FC</text>" in result


def test_render_with_if() -> None:
    svg = """
    <svg>
        <text data-if="team.isChampion" data-bind="team.name"></text>
        <text data-if="not team.isChampion" data-bind="'Challenger: ' + team.name"></text>
    </svg>
    """
    data = {"team": {"name": "Red Star FC", "isChampion": True}}

    result = render(svg, data)

    assert "<text>Red Star FC</text>" in result
    assert "Challenger" not in result

    data["team"]["isChampion"] = False
    result = render(svg, data)

    assert "<text>Challenger: Red Star FC</text>" in result


def test_render_with_repeat() -> None:
    svg = """
    <svg>
        <g data-repeat="teams">
            <text data-bind="name" data-attr="y: index + 20"></text>
        </g>
    </svg>
    """
    data = {
        "teams": [
            {"name": "Red Star FC"},
            {"name": "Paris FC"},
            {"name": "PSG"},
        ]
    }

    result = render(svg, data)

    assert '<text y="20">Red Star FC</text>' in result
    assert '<text y="21">Paris FC</text>' in result
    assert '<text y="22">PSG</text>' in result
