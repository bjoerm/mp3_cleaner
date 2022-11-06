# TODO What enhancements rely on knowing what other files in the folder look like?
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import regex
from mutagen.id3 import APIC, ID3, POPM
from mutagen.mp3 import MP3  # Alternative to ID3 and ID3NoHeaderError.

from beautify_filepaths import FileBeautifier
from beautify_multiple_tags import TagBeautifier
from beautify_single_string import StringBeautifier
from tags_model import TagsImportedModel


class File:
    """This class reads all tags of a file, extracts the relevant informations and only keeps accepted fields. The latter is done via Pydantic."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.tags_imported: Dict[str, str | bytes | POPM] = self.import_tags_as_dict()  # TODO Hier auf die Main-Method verweisen, welche den obigen groben Ablauf abbildet.
        self.tags_beautified = self.validate_and_beautify_tags()

    def import_tags_as_dict(self) -> Dict[str, str | bytes | POPM]:
        """Import all ID3 tags from the MP3 file as dict. Also converting as much fields as possible from ID3 classes into normal str or other base Python objects."""
        tags_imported = ID3(self.filepath)

        tags_dict = dict(tags_imported)

        for k in tags_dict:
            if hasattr(tags_dict[k], "text"):
                tags_dict[k] = str(tags_dict[k].text[0])
            elif hasattr(tags_dict[k], "data"):
                tags_dict[k] = tags_dict[k].data

        return tags_dict

    def validate_and_beautify_tags(self):
        """TODO Docstring"""
        tags = TagsImportedModel(**self.tags_imported)
        tags.TPE1, tags.TPE2 = self.check_alternative_fields(tags.TPE1, tags.TPE2)
        tags.TDRC, tags.TDRL = self.check_alternative_fields(tags.TDRC, tags.TDRL)
        tags.TALB = StringBeautifier.beautify_string(tags.TALB)
        tags.TIT2 = StringBeautifier.beautify_string(tags.TIT2)
        tags.TPE1 = StringBeautifier.beautify_string(tags.TPE1, remove_leading_the=True)
        tags.TPE2 = StringBeautifier.beautify_string(tags.TPE2, remove_leading_the=True)
        tags.TPE1, tags.TIT2 = self.check_feat_in_artist(album_artist=tags.TPE1, track=tags.TIT2)

        # TODO _sort_track_name_suffixes()

        return tags

    @staticmethod
    def check_alternative_fields(main_field: Any, helper_field: Any) -> Tuple[Any, None]:
        """If there is no main_field, use the helper_field instead. helper_field is emptied anyway afterwards.
        E.g. there is no track artist but an album artist. Then the album artist is used as track artist."""
        if main_field is None and helper_field is not None:
            main_field = helper_field

        return main_field, None

    @staticmethod
    def check_feat_in_artist(album_artist: Optional[str], track: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
        """
        Deal with the case of featuring information being in the track artist field by moving it from the track artist to the track name.
        Needs be executed after the normal string beautification.
        """
        if album_artist is None or track is None:
            return album_artist, track

        feat_from_artist_field = regex.search(r"(.+)(\s+feat\.\s+.+|\s+\(\s*feat\.\s+.+\))", album_artist, regex.IGNORECASE)  # Searching for " feat. " and " (feat. xyz)".

        if feat_from_artist_field is not None:
            feat_info = feat_from_artist_field.group(2).strip()

            # Ensure brackets around feat
            has_bracket = regex.match(r"^\s*\(\s*feat\.\s+.+\)\s*$", feat_info, regex.IGNORECASE)

            if has_bracket is None:
                feat_info = f"({feat_info.strip()})"  # Wrap brackets around string.

            album_artist = feat_from_artist_field.group(1).strip()
            track = f"{track} {feat_info.strip()}"

        return album_artist, track

    def export_tags_in_file(self):
        # TODO A second public method that is used for writing output to files.
        pass

    def validate_tags_prior_update(self):
        # TODO Via Pydantic it should be checked whether the output is still according to the desired form. Should a new class be written for that?
        pass

    def write_beautified_tag_to_files(self):
        pass


if __name__ == "__main__":

    abc = File(
        filepath=Path("input/aaaaaaaMP3/0000 Boy - little numbers.mp3"),
    )

    print(abc.tags_imported)
    print(abc.tags_beautified)

    pass
