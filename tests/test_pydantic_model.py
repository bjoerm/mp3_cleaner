import pytest

from pydantic_models.tag_models import TagsImportModel

# TODO There should be more tests for the ImportedTagsModel in total as this also only needs a dict.
# TODO Add TagsExportModel


@pytest.mark.parametrize(
    "name, input, expected_output",
    [
        ["Normal", "1/1", 1],
        ["Normal", "1", 1],
        ["Normal", "100/200", 100],
        ["Normal", "15/20", 15],
        ["Normal", "100", 100],
        ["Int", 1, 1],
        ["Int", 15, 15],
        ["Float", 1.5, 1],  # TODO Is this desired?
        ["Leading zero", "01/01", 1],
        ["Leading zero", "01", 1],
        ["Leading zero", "001", 1],
        ["Leading zero", "001/100", 1],
        ["Leading slash", "/1", 1],
        ["Leading slash", "/10", 10],
    ],
)
def test_extract_number_from_slash_format(name, input, expected_output):
    """Testing the extraction (and conversion into int) of only the current part of a track or disc number, leaving out the number of total tracks/discs."""
    assert TagsImportModel.extract_number_from_slash_format(input) == expected_output, name


@pytest.mark.parametrize(
    "name, input, expected_output",
    [["Normal", "2000", 2000], ["Normal", "01-01-2000", 2000], ["Normal", "2000-01-01", 2000], ["Normal", "01.01.2000", 2000], ["Int", 2000, 2000], ["Shorter Number", "1", None], ["Shorter Number", "10", None], ["Shorter Number", "100", None]],
)
def test_extract_year(name, input, expected_output):
    assert TagsImportModel.extract_year(input) == expected_output, name


@pytest.mark.parametrize(
    "name, input, expected_output",
    [
        ["Normal", "Track Artist", "Track Artist"],
        ["Outside Spaces", " Track Artist ", "Track Artist"],
        ["Int", 123, "123"],
    ],
)
def test_validated_tpe1(name, input, expected_output):
    input_dict = {"TPE1": input}

    assert TagsImportModel(**input_dict).TPE1 == expected_output, name
