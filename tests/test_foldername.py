import pytest

from folder.foldername import FolderName


@pytest.mark.parametrize(
    "name, album_name, expected_output",
    [
        ["No Score", "Movie", "Movie"],
        ["Score", "Movie (Score)", "Movie"],
        ["Soundtrack", "Movie (Soundtrack)", "Movie"],
        ["Score Number", "Movie 2 (Score)", "Movie"],
        ["Score Number", "Movie - Part 2 (Score)", "Movie"],
        ["Soundtrack Number", "Movie 2 (Soundtrack)", "Movie"],
        ["No brackets", "The Great Score", "The Great Score"],
        ["Numbers", "2000 (Score)", "2000"],
        ["No Score Numbers", "2000", "2000"],
        ["Movie 2000", "Movie 2000", "Movie"],
        ["Movie - 2000", "Movie - 2000", "Movie"],
        ["Movie - 2000 (Score)", "Movie - 2000 (Score)", "Movie"],
        ["Movie 2000 (Score)", "Movie 2000 (Score)", "Movie"],
    ],
)
def test_generate_first_part_score_soundtrack(name, album_name, expected_output):
    assert FolderName._generate_first_part_score_soundtrack(album_name=album_name) == expected_output, name
