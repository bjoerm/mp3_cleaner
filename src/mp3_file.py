from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import regex
from mutagen.id3 import ID3
from mutagen.id3._frames import APIC, POPM, TALB, TDRC, TIT2, TPE1, TPOS, TRCK

from beautify_single_string import StringBeautifier
from tags_models import TagsExportModel, TagsImportModel


class MP3FileTags:
    def __init__(self, filepath) -> None:
        self.tags_id3_mutagen: ID3 = ID3(filepath)
        self.tags_beautified: TagsExportModel

    def beautify_tags_isolated(self):
        """Beautifies the tags with information found in this file. Thus, "isolated" as it does not (yet) look at information from other files in the folder."""

        tags_dict = self._convert_tags_to_dict()

        tags = TagsImportModel(**tags_dict)
        tags.TPE1, tags.TPE2 = self._check_fallback_tag_fields(tags.TPE1, tags.TPE2)
        tags.TDRC, tags.TDRL = self._check_fallback_tag_fields(tags.TDRC, tags.TDRL)
        tags.TALB = StringBeautifier.beautify_string(tags.TALB)
        tags.TIT2 = StringBeautifier.beautify_string(tags.TIT2)
        tags.TPE1 = StringBeautifier.beautify_string(tags.TPE1, remove_leading_the=True)
        tags.TPE2 = StringBeautifier.beautify_string(tags.TPE2, remove_leading_the=True)
        tags.TPE1, tags.TIT2 = self._check_feat_in_artist(album_artist=tags.TPE1, track=tags.TIT2)

        tags.TIT2 = self._sort_track_name_suffixes(tags.TIT2)

        self.tags_beautified = TagsExportModel(**tags.dict(exclude_none=True))

    def _convert_tags_to_dict(self) -> Dict[str, str | int | Dict[str, str | bytes]]:
        """Extract the relevant parts for each tag from the mutagen ID3 class into a dictionary. That means that tags are reduced to normal strings or other base Python objects."""

        # Convert
        tags_dict = dict(self.tags_id3_mutagen)

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

    @staticmethod
    def _check_fallback_tag_fields(main_field: Any, helper_field: Any) -> Tuple[Any, None]:
        """If there is no main_field (like track artist), use the helper_field (like album artist) instead. helper_field is emptied anyway afterwards."""

        if main_field is None and helper_field is not None:
            main_field = helper_field

        return main_field, None

    @staticmethod
    def _check_feat_in_artist(album_artist: Optional[str], track: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
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
    def _sort_track_name_suffixes(cls, track_name: Optional[str]) -> Optional[str]:
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
        self.tags_beautified.TRCK = self._add_leading_zeros(number_current=self.tags_beautified.TRCK, leading_zeros=leading_zeros_track)
        self.tags_beautified.TPOS = self._add_leading_zeros(number_current=self.tags_beautified.TPOS, leading_zeros=leading_zeros_album)

    @staticmethod
    def _add_leading_zeros(number_current: Optional[int], leading_zeros: Optional[int]) -> Optional[str]:

        if leading_zeros is None or number_current is None:
            number_beautified = None
        else:
            number_beautified = str(number_current).zfill(leading_zeros)

        return number_beautified

    def write_beautified_tags_to_file(self):

        # Final validation and conversion to dict:
        tags = TagsExportModel(**self.tags_beautified.dict(exclude_none=True))
        tags = tags.dict(exclude_none=True)

        self.tags_id3_mutagen.delete()  # Delete all existing tags from the mutagen id3 object inside this class.

        self._add_tags_to_id3_object(tags=tags)

        self.tags_id3_mutagen.save(v1=0, v2_version=4)

    def _add_tags_to_id3_object(self, tags: Dict[str, str | int | Dict[str, str | bytes]]):
        """
        Save beautified tags to the mutagen id3 object. This function takes only on row from df_iteration at a time.
        """
        encoding_value = 3  # 1 = UTF16, 3 = UTF8

        # TODO Try structural pattern matching here!
        for key, value in tags.items():
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


# TODO Ask Bodo whether this should be a dataclass?
class MP3FileName:
    def __init__(self, filepath: Path) -> None:
        self.filepath_inital = filepath.absolute()
        self.filepath_beautified: Path

    def beautify_and_write_filename(
        self,
        tags_beautified: TagsExportModel,
        only_single_mp3_file: bool,
        folder_has_same_artist: Optional[bool],
        has_each_file_a_disc_number: bool,
        has_each_file_a_track_number: bool,
    ):

        filename_beautified = self.generate_beautified_filename(
            tag_artist=tags_beautified.TPE1,
            tag_title=tags_beautified.TIT2,
            tag_disc=tags_beautified.TPOS,
            tag_track=tags_beautified.TRCK,
            only_single_mp3_file=only_single_mp3_file,
            folder_has_same_artist=folder_has_same_artist,
            has_each_file_a_disc_number=has_each_file_a_disc_number,
            has_each_file_a_track_number=has_each_file_a_track_number,
        )

        self.filepath_beautified = self.filepath_inital.parent / filename_beautified

        self.filepath_inital.rename(self.filepath_beautified)

    @classmethod
    def generate_beautified_filename(
        cls,
        tag_artist: Optional[str],
        tag_title: Optional[str],
        tag_disc: Optional[str],
        tag_track: Optional[str],
        only_single_mp3_file: bool,
        folder_has_same_artist: Optional[bool],
        has_each_file_a_disc_number: bool,
        has_each_file_a_track_number: bool,
    ) -> str:

        disc_track_number = cls._generate_disc_track_number(has_each_file_a_disc_number=has_each_file_a_disc_number, has_each_file_a_track_number=has_each_file_a_track_number, tag_disc=tag_disc, tag_track=tag_track)

        filename_beautified = None

        if only_single_mp3_file is True:
            filename_beautified = f"[{tag_artist}] - {tag_title}"

        elif folder_has_same_artist is True:
            filename_beautified = f"[{tag_artist}] - {disc_track_number}{tag_title}"

        elif folder_has_same_artist is False:
            filename_beautified = f"{disc_track_number}[{tag_artist}] - {tag_title}"

        return f"{filename_beautified}.mp3"  # Note that I am hardcoding here the file extension.

    @staticmethod
    def _generate_disc_track_number(has_each_file_a_disc_number: bool, has_each_file_a_track_number: bool, tag_disc: Optional[str], tag_track: Optional[str]) -> str:

        if has_each_file_a_track_number is True:
            if has_each_file_a_disc_number is True:
                disc_track_number = f"{tag_disc}{tag_track} - "
            elif has_each_file_a_disc_number is False:
                disc_track_number = f"{tag_track} - "

        elif has_each_file_a_track_number is False:
            disc_track_number = ""

        return disc_track_number


class MP3File:
    def __init__(self, filepath) -> None:
        self.tags = MP3FileTags(filepath=filepath)
        self.name = MP3FileName(filepath=filepath)


if __name__ == "__main__":

    abc = MP3File(
        filepath=Path("data/wikimedia_commons/warnsignal_train_with_some_tags.mp3"),
    )

    print(abc.tags.tags_id3_mutagen)

    pass
