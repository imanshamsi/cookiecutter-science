def multiply(a: int, b: int) -> int:
    return a * b


def test_multiply_basic():
    assert multiply(2, 3) == 6


def test_multiply_zero():
    assert multiply(10, 0) == 0


def test_multiply_negative():
    assert multiply(-2, 4) == -8
