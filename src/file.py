# TODO What enhancements rely on knowing what other files in the folder look like?


from pathlib import Path
from typing import Dict

from mutagen.id3 import APIC, ID3, POPM
from mutagen.mp3 import MP3  # Alternative to ID3 and ID3NoHeaderError.

from beautify_filepaths import FileBeautifier
from beautify_multiple_tags import TagBeautifier
from pydantic_models import ImportedTagsModel


class File:
    """This class reads all tags of a file, extracts the relevant informations and only keeps accepted fields. The latter is done via Pydantic."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.tags_imported = self.import_tags_as_dict()  # TODO Hier auf die Main-Method verweisen, welche den obigen groben Ablauf abbildet.

    def import_tags_as_dict(self) -> ImportedTagsModel:
        tags_imported = self._import_id3_tag_from_file()
        tags_imported = self._extract_imported_text_tags(tags_imported)
        tags_imported = self._normalize_and_validate_imported_tags(tags_imported)

        return tags_imported

    def _import_id3_tag_from_file(self) -> ID3:
        """Import all ID3 tags from the MP3 file."""
        # TODO Add handling of files without tags.
        return ID3(self.filepath)

    def _extract_imported_text_tags(self, tags_imported: ID3) -> Dict[str, str | bytes | POPM]:
        """Converting all tags that have the attribute 'text' as strings and thus removing other attributes like the enconding attributes."""

        tags_dict: dict = dict(tags_imported)

        for k in tags_dict:
            if hasattr(tags_dict[k], "text"):
                tags_dict[k] = str(tags_dict[k].text[0])
            elif hasattr(tags_dict[k], "data"):
                tags_dict[k] = tags_dict[k].data

        return tags_dict

    def _normalize_and_validate_imported_tags(self, tags_imported: Dict[str, str | bytes | POPM]):
        tags = ImportedTagsModel(**tags_imported)

        return tags

    def export_tags_in_file(self):
        # TODO A second public method that is used for writing output to files.
        pass

    def _validate_tags_prior_update(self):
        # TODO Via Pydantic it should be checked whether the output is still according to the desired form. Should a new class be written for that?
        pass

    def _write_beautified_tag_to_files(self):
        pass


if __name__ == "__main__":

    File(
        filepath=Path("input/aaaaaaaMP3/0000 Boy - little numbers.mp3"),
    )

    pass
