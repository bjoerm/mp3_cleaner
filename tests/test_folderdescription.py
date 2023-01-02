import pytest

from folder.folderdescription import FolderDescription


@pytest.mark.parametrize(
    "name, tag, expected_output",
    [
        ["Deviation String", ["1", "2", "3"], False],
        ["Deviation Int", [1, 2, 3], False],
        ["Same String", ["1", "1", "1"], True],
        ["Same Int", [1, 1, 1], True],
        ["All None", [None, None, None], False],
        ["One None", ["1", "2", None], False],
        ["Single String", ["1"], True],  # There is another check whether it is only one file, that is be used e.g. for filenaming.
        ["Single Int", [1], True],  # There is another check whether it is only one file, that is be used e.g. for filenaming.
        ["Single None", [None], False],
    ],
)
def test_check_tag_uniformity(name, tag, expected_output):
    assert FolderDescription._check_tag_uniformity(tag=tag) == expected_output, name


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
    assert FolderDescription._check_presence_in_all_tags(tag=tag) == expected_output, name


@pytest.mark.parametrize(
    "name, folder_has_same_album, album_name, expected_output",
    [
        ["(Score)", True, "Super Movie (Score)", True],
        ["(Soundtrack)", True, "Super Movie (Soundtrack)", True],
        ["Score", True, "Not A Score", False],
        ["Soundtrack", True, "Not A Soundtrack", False],
        ["Different Albums", False, "(Score)", False],
        ["Different Albums", False, "Score", False],
    ],
)
def test_check_album_is_score_or_soundtrack(name, folder_has_same_album, album_name, expected_output):
    assert FolderDescription._check_album_is_score_or_soundtrack(folder_has_same_album=folder_has_same_album, album_name=album_name) == expected_output, name
