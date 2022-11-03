import pytest

from pydantic_models import ImportedTagsModel


@pytest.mark.parametrize(
    "name, input, expected_output",
    [["Normal", "1/1", 1], ["Normal", "1", 1], ["Normal", "100/200", 100], ["Normal", "15/20", 15], ["Normal", "100", 100], ["Int", 1, 1], ["Int", 15, 15], ["Float", 1.5, 1], ["Leading zero", "01/01", 1], ["Leading zero", "01", 1], ["Leading zero", "001", 1], ["Leading zero", "001/100", 1]],
)
def test_keep_only_current_number(name, input, expected_output):
    """Testing the extraction (and conversion into int) of only the current part of a track or disc number, leaving out the number of total tracks/discs."""
    assert ImportedTagsModel.keep_only_current_number(input) == expected_output, name
