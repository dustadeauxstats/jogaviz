from jogaviz_core.render.functions import (
    percentage,
    round,
    capitalize,
    uppercase,
    truncate,
    abbreviate_name,
)


def test_percentage() -> None:
    assert percentage(0.1234) == "12.34%"
    assert percentage(0.5) == "50.00%"
    assert percentage(1.0) == "100.00%"
    assert percentage(0.1234, 1) == "12.3%"
    assert percentage(0.1234, 3) == "12.340%"


def test_round() -> None:
    assert round(3.14159) == "3.14"
    assert round(2.71828, 3) == "2.718"
    assert round(1.0) == "1.00"
    assert round(1.005, 2) == "1.00"
    assert round(1.005, 3) == "1.005"


def test_capitalize() -> None:
    assert capitalize("hello") == "Hello"
    assert capitalize("Hello") == "Hello"
    assert capitalize("") == ""
    assert capitalize("a") == "A"
    assert capitalize("aBC") == "ABC"


def test_uppercase() -> None:
    assert uppercase("hello") == "HELLO"
    assert uppercase("Hello") == "HELLO"
    assert uppercase("") == ""
    assert uppercase("a") == "A"
    assert uppercase("aBC") == "ABC"


def test_truncate() -> None:
    assert truncate("Hello, world!", 5) == "Hello..."
    assert truncate("Short", 10) == "Short"
    assert truncate("", 5) == ""
    assert truncate("Exact", 5) == "Exact"
    assert truncate("This is a long string", 10) == "This is a ..."


def test_abbreviate_name() -> None:
    assert abbreviate_name("John Doe") == "John D."
    assert abbreviate_name("SingleName") == "SingleName"
    assert abbreviate_name("") == ""
    assert abbreviate_name("John Doe", keep_first=False) == "J. Doe"
