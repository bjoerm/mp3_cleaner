# TODO What enhancements rely on knowing what other files in the folder look like?

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import regex
from mutagen.id3 import APIC, ID3, POPM
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
    def _convert_tags_to_dict(tags_id3_mutagen: ID3) -> Dict[str, str | bytes | POPM]:
        """Convert the fields from the mutagen ID3 class into a dictionary. Also converting as many fields as possible into normal str or other base Python objects."""

        tags_dict = dict(tags_id3_mutagen)

        for k in tags_dict:
            if hasattr(tags_dict[k], "text"):
                tags_dict[k] = str(tags_dict[k].text[0])
            elif hasattr(tags_dict[k], "data"):
                tags_dict[k] = tags_dict[k].data

        return tags_dict

    def _validate_and_beautify_tags(self, tags_import: Dict[str, str | bytes | POPM]) -> TagsExportModel:
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

        tags_export = TagsExportModel(**tags.dict(exclude_none=True, by_alias=True))  # by_alias to carry the odd naming the keys APIC: and POPM:no@email over.

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
        tags = TagsExportModel(**self.tags.dict(exclude_none=True, by_alias=True))
        tags = tags.dict(exclude_none=True, by_alias=True)  # by_alias to carry the odd naming the keys APIC: and POPM:no@email over.

        self.tags_id3_mutagen.delete()

        self._add_tags_to_id3_object(tags=tags)

        self.tags_id3_mutagen.save(v1=0, v2_version=4)

    def _add_tags_to_id3_object(self, tags: Dict[str, str | bytes | POPM]):
        """
        Save beautified tags to id3 object. This function takes only on row from df_iteration at a time.
        """

        for key, value in tags.items():

            if key in ("POPM:no@email", "APIC:"):  # Does not have a text field and thus a bit different structure.
                self.tags_id3_mutagen.add(value)
                pass
                # exec(f'id3.add({value})')

            elif key in ("TALB", "TDRC", "TIT2", "TPE1", "TPE2", "TPOS", "TRCK"):  # These fields (all but rating), have a text parameter which can be added the same way.
                exec(f'self.tags_id3_mutagen.add({key}(encoding = 3, text = "{value}"))')  # encoding = 3 = UTF8 # Executes the following string as Python command. The f in the beginning marks this as "f string". See https://www.python.org/dev/peps/pep-0498/

            else:
                # This else condition should not be reached. It is used to raise an alert, when new tag types are entered in the global variables but not yet defined here.
                raise NameError("It seems like a new key was added to options but not added to the handling above in this method.")

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
