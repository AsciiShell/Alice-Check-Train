import pytest

from alice_check_train.true_answer import _NUMBERS_TO_STR


@pytest.mark.parametrize("test_input,expected", [
    (0, ''),
    (5, 'пять'),
    (9, 'девять')
])
def test_answer(test_input, expected):
    assert _NUMBERS_TO_STR[test_input] == expected
