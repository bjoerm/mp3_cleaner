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
        self.filename = self.filepath.name  # TODO Remove this here and create own filename class or have all the filename handling in the folder class?
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

    def validate_and_beautify_tags(self) -> TagsImportedModel:
        """TODO Docstring"""
        tags = TagsImportedModel(**self.tags_imported)
        tags.TPE1, tags.TPE2 = self.check_secondary_tag_fields(tags.TPE1, tags.TPE2)
        tags.TDRC, tags.TDRL = self.check_secondary_tag_fields(tags.TDRC, tags.TDRL)
        tags.TALB = StringBeautifier.beautify_string(tags.TALB)
        tags.TIT2 = StringBeautifier.beautify_string(tags.TIT2)
        tags.TPE1 = StringBeautifier.beautify_string(tags.TPE1, remove_leading_the=True)
        tags.TPE2 = StringBeautifier.beautify_string(tags.TPE2, remove_leading_the=True)
        tags.TPE1, tags.TIT2 = self.check_feat_in_artist(album_artist=tags.TPE1, track=tags.TIT2)

        tags.TIT2 = self.sort_track_name_suffixes(tags.TIT2)

        return tags

    @staticmethod
    def check_secondary_tag_fields(main_field: Any, helper_field: Any) -> Tuple[Any, None]:
        """If there is no main_field (like track artist), use the helper_field (like album artist) instead. helper_field is emptied anyway afterwards."""

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

    @classmethod
    def sort_track_name_suffixes(cls, track_name: Optional[str]) -> Optional[str]:
        """Put any track names with multiple suffixes like (... Remix), (Acoustic), (Live ...), (Feat. ...) into an adequate order."""  # TODO If I only set Live at the end, then I don't need to over do it here.
        if track_name is None:
            return track_name

        track_name, suffixes = cls._extract_suffixes(track_name)

        if suffixes is None:
            return track_name

        suffixes = regex.findall(r"(\(.+?\))", suffixes, regex.IGNORECASE)  # Convert string into a list of strings.

        selected_suffixes = {"live": None, "feat": None}

        for suffix in suffixes.copy():  # Using a copy for iterating as items from the original list can be removed in this loop.
            suffix_bare = cls._remove_string_noise(suffix)

            for keyword in ["live", "feat"]:
                # Looking for the keyword in the first and last word of the suffix.
                if suffix_bare.split()[0] == keyword or suffix_bare.split()[-1] == keyword:
                    selected_suffixes[keyword] = suffix
                    suffixes.remove(suffix)

        track_name_reordered = f'{track_name} {" ".join(suffixes)} {selected_suffixes.get("feat") or ""} {selected_suffixes.get("live") or ""}'

        track_name_reordered = StringBeautifier._remove_not_needed_whitespaces(track_name_reordered)

        return track_name_reordered

    @staticmethod
    def _extract_suffixes(track_name: str) -> Tuple[str, Optional[str]]:
        """Checking the track name for multiple brackets."""
        at_least_two_sets_of_brackets = regex.search(r"(.+?)(\(.+\)\s\(.+\))", track_name, regex.IGNORECASE)  # Search for strings with multiple brackets at the end.

        if at_least_two_sets_of_brackets is None:  # Less than two sets of brackets found, no need for re-ordering.
            return track_name, None

        track_name_without_suffixes = at_least_two_sets_of_brackets.group(1).strip()  # Note that this would end with a space without the strip().
        suffixes = at_least_two_sets_of_brackets.group(2)  # This is one single string.

        return track_name_without_suffixes, suffixes

    @staticmethod
    def _remove_string_noise(text: str) -> str:
        """
        Gets rid of not needed characters like non-alphanumeric characters and capitalization from a string.
        """

        text = regex.sub(pattern=r"[^0-9a-zA-Z\s]+", repl="", string=text)  # Removing any non-alphanumeric characters.
        text = text.lower()  # Uniquely transforming the word to lowercase.

        return text

    def validate_tags_prior_update(self):
        # TODO Via Pydantic it should be checked whether the output is still according to the desired form. Should a new class be written for that?
        pass

    def write_beautified_tags_to_file(self):
        pass

    def beautify_filename(self):
        pass

        # TODO Use another Filename class?


if __name__ == "__main__":

    abc = File(
        filepath=Path("input/aMP3/0000 Boy - little numbers.mp3"),
    )

    print(abc.tags_imported)
    print(abc.tags_beautified)

    pass
