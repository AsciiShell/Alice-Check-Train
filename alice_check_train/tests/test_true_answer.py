import pytest

from alice_check_train.true_answer import first_req


@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 42)
])
def test_answer(test_input, expected):
    assert first_req(test_input) == expected
