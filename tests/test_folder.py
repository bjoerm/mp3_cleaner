import pytest

from folder import Folder


@pytest.mark.parametrize(
    "name, numbers, expected_output",
    [
        ["Length 1", ["1", "2", "3"], 1],
        ["Length 2", ["1", "2", "10"], 2],
        ["Length 3", ["1", "2", "100"], 3],
        ["Length 4", ["1", "2", "1000"], 4],
        ["All None", [None, None, None], None],
        ["One None", ["1", "2", None], None],
        ["Max 1", ["1", "1", "1"], None],
    ],
)
def test_calculate_leading_zeros(name, numbers, expected_output):
    assert Folder.calculate_leading_zeros(numbers=numbers) == expected_output, name
