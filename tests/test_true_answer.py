import pytest

from alice_check_train.true_answer import first_req


@pytest.mark.parametrize("test_input,expected", [
    (0, ''),
    (5, 'пять'),
    (9, 'девять')
])
def test_answer(test_input, expected):
    assert first_req(test_input) == expected
