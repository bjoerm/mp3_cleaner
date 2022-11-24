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


@pytest.mark.parametrize(
    "name, tag, expected_output",
    [
        ["Deviation String", ["1", "2", "3"], False],
        ["Deviation Int", [1, 2, 3], False],
        ["Same String", ["1", "1", "1"], True],
        ["Same Int", [1, 1, 1], True],
        ["All None", [None, None, None], None],
        ["One None", ["1", "2", None], None],
        ["Single String", ["1"], True],  # TODO Is this desired, if there is only a single file?
        ["Single Int", [1], True],  # TODO Is this desired, if there is only a single file?
        ["Single None", [None], None],
    ],
)
def test_check_tag_uniformity(name, tag, expected_output):
    assert Folder.check_tag_uniformity(tag=tag) == expected_output, name


@pytest.mark.parametrize(
    "name, tag, expected_output",
    [
        ["Deviation String", ["1", "2", "3"], True],
        ["Deviation Int", [1, 2, 3], True],
        ["Same String", ["1", "1", "1"], True],
        ["Same Int", [1, 1, 1], True],
        ["All None", [None, None, None], False],
        ["One None", ["1", "2", None], False],
        ["Single String", ["1"], True],
        ["Single Int", [1], True],
        ["Single None", [None], False],
    ],
)
def test_check_presence_in_all_tags(name, tag, expected_output):
    """Using the effect that None is returned, if a None is detected."""
    assert (Folder.check_tag_uniformity(tag=tag) is not None) == expected_output, name
