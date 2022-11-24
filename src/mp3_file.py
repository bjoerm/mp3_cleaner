# TODO What enhancements rely on knowing what other files in the folder look like?

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import regex
from mutagen.id3 import ID3
from mutagen.id3._frames import APIC, POPM, TALB, TDRC, TIT2, TPE1, TPOS, TRCK
from mutagen.mp3 import MP3  # Alternative to ID3 and ID3NoHeaderError.

from beautify_single_string import StringBeautifier
from tags_model import TagsExportModel, TagsImportModel


@dataclass
class MP3File:
    """This class reads all tags of a file, extracts the relevant informations and only keeps accepted fields. The latter is done via Pydantic."""

    filepath: Path
    filename: str = field(init=False)
    tags_id3_mutagen: ID3 = field(init=False)
    tags: TagsExportModel = field(init=False)
    leading_zeros_track: Optional[int] = field(init=False)
    leading_zeros_album: Optional[int] = field(init=False)

    def __post_init__(self):
        self.filename = self.filepath.name  # TODO Remove this here and create own filename class or have all the filename handling in the folder class?
        self.tags_id3_mutagen = ID3(self.filepath)  # TODO Have this more elaborated to deal with the case of no tags in file.
        self.tags = self.convert_validate_and_beautify_tags()

    def convert_validate_and_beautify_tags(self) -> TagsExportModel:
        tags_import = self._convert_tags_to_dict(tags_id3_mutagen=self.tags_id3_mutagen)
        tags_export = self._validate_and_beautify_tags(tags_import=tags_import)

        return tags_export

    @staticmethod
    def _convert_tags_to_dict(tags_id3_mutagen: ID3) -> Dict[str, str | int | Dict[str, str | bytes]]:
        """Extract the relevant parts for each tag from the mutagen ID3 class into a dictionary. That means that tags are reduced to normal strings or other base Python objects."""

        # Convert
        tags_dict = dict(tags_id3_mutagen)

        # Extract
        for k in tags_dict:
            if hasattr(tags_dict[k], "text"):
                tags_dict[k] = str(tags_dict[k].text[0])
            elif hasattr(tags_dict[k], "mime") and hasattr(tags_dict[k], "data"):  # For APIC
                tags_dict[k] = {"mime": tags_dict[k].mime, "data": tags_dict[k].data}
            elif hasattr(tags_dict[k], "data"):
                tags_dict[k] = tags_dict[k].data
            elif hasattr(tags_dict[k], "rating"):  # For POPM
                tags_dict[k] = tags_dict[k].rating
            else:
                pass

        return tags_dict

    def _validate_and_beautify_tags(self, tags_import: Dict[str, str | int | Dict[str, str | bytes]]) -> TagsExportModel:
        """TODO Docstring"""

        tags = TagsImportModel(**tags_import)
        tags.TPE1, tags.TPE2 = self.check_fallback_tag_fields(tags.TPE1, tags.TPE2)
        tags.TDRC, tags.TDRL = self.check_fallback_tag_fields(tags.TDRC, tags.TDRL)
        tags.TALB = StringBeautifier.beautify_string(tags.TALB)
        tags.TIT2 = StringBeautifier.beautify_string(tags.TIT2)
        tags.TPE1 = StringBeautifier.beautify_string(tags.TPE1, remove_leading_the=True)
        tags.TPE2 = StringBeautifier.beautify_string(tags.TPE2, remove_leading_the=True)
        tags.TPE1, tags.TIT2 = self.check_feat_in_artist(album_artist=tags.TPE1, track=tags.TIT2)

        tags.TIT2 = self.sort_track_name_suffixes(tags.TIT2)

        tags_export = TagsExportModel(**tags.dict(exclude_none=True))

        return tags_export

    @staticmethod
    def check_fallback_tag_fields(main_field: Any, helper_field: Any) -> Tuple[Any, None]:
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

    def beautify_track_and_album_number(self, leading_zeros_track: Optional[int], leading_zeros_album: Optional[int]):
        self.tags.TRCK = self._add_leading_zeros(number_current=self.tags.TRCK, leading_zeros=leading_zeros_track)
        self.tags.TPOS = self._add_leading_zeros(number_current=self.tags.TPOS, leading_zeros=leading_zeros_album)

    @staticmethod
    def _add_leading_zeros(number_current: Optional[int], leading_zeros: Optional[int]) -> Optional[str]:

        if leading_zeros is None or number_current is None:
            number_beautified = None
        else:
            number_beautified = str(number_current).zfill(leading_zeros)

        return number_beautified

    def write_beautified_tags_to_file(self):

        # Final validation and conversion to dict:
        tags = TagsExportModel(**self.tags.dict(exclude_none=True))
        tags = tags.dict(exclude_none=True)

        self.tags_id3_mutagen.delete()  # Delete all existing tags from the mutagen id3 object inside this class.

        self._add_tags_to_id3_object(tags=tags)

        self.tags_id3_mutagen.save(v1=0, v2_version=4)

    def _add_tags_to_id3_object(self, tags: Dict[str, str | int | Dict[str, str | bytes]]):
        """
        Save beautified tags to the mutagen id3 object. This function takes only on row from df_iteration at a time.
        """

        for key, value in tags.items():

            encoding_value = 3  # 1 = UTF16, 3 = UTF8

            if key == "APIC":
                self.tags_id3_mutagen.add(APIC(mime=value["mime"], data=value["data"]))

            elif key == "POPM":
                self.tags_id3_mutagen.add(POPM(email="no@email", rating=value))

            elif key == "TPE1":
                self.tags_id3_mutagen.add(TPE1(encoding=encoding_value, text=value))

            elif key == "TIT2":
                self.tags_id3_mutagen.add(TIT2(encoding=encoding_value, text=value))

            elif key == "TALB":
                self.tags_id3_mutagen.add(TALB(encoding=encoding_value, text=value))

            elif key == "TDRC":
                self.tags_id3_mutagen.add(TDRC(encoding=encoding_value, text=value))

            elif key == "TPOS":
                self.tags_id3_mutagen.add(TPOS(encoding=encoding_value, text=value))

            elif key == "TRCK":
                self.tags_id3_mutagen.add(TRCK(encoding=encoding_value, text=value))

            else:
                raise NameError("This else condition should not be reached. Check the Pydantic classes.")

    def beautify_filename(self):
        pass

        # TODO Use another Filename class?
        # TODO abc.tags_beautified.dict() -> change the dict key for APIC back to APIC:. Also check whether POPM need changes.


if __name__ == "__main__":

    abc = MP3File(
        filepath=Path("input/aMP3/0000 Boy - little numbers.mp3"),
    )

    print(abc.tags_id3_mutagen)
    print(abc.tags)

    pass
