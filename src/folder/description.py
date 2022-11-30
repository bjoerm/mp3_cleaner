# TODO Add functionality to remove the disc number if
# - All track have the same disc number.
# - That shared disc number is =1.
# - And the album title does not contain the letters "cd" followed by an integer or space then integer.

# TODO Beware of case where cd xy is in album title but not in disc number. Do that already in Pydantic???

from typing import List, Optional

from pydantic_models.tag_models import TagsExportModel


class FolderDescription:
    """Class that stores folder wide information from analyzing the tags of all files."""

    def __init__(self, beautified_tags: List[TagsExportModel]) -> None:
        self.only_single_mp3_file: bool
        self.folder_has_same_album: bool
        self.folder_has_same_artist: bool
        self.folder_has_same_date: bool
        self.folder_has_same_disc_number: bool
        self.has_each_file_an_album: bool
        self.has_each_file_a_date: bool
        self.has_each_file_a_disc_number: bool
        self.has_each_file_a_track_number: bool
        self.is_score_or_soundtrack: bool

        self.only_single_mp3_file = len(beautified_tags) == 1

        self.folder_has_same_artist = self._check_tag_uniformity(tag=[tags.TPE1 for tags in beautified_tags])
        self.folder_has_same_disc_number = self._check_tag_uniformity(tag=[tags.TPOS for tags in beautified_tags])
        self.folder_has_same_album = self._check_tag_uniformity(tag=[tags.TALB for tags in beautified_tags])
        self.folder_has_same_date = self._check_tag_uniformity(tag=[tags.TDRC for tags in beautified_tags])

        self.has_each_file_an_album = self._check_presence_in_all_tags(tag=[tags.TALB for tags in beautified_tags])
        self.has_each_file_a_date = self._check_presence_in_all_tags(tag=[tags.TDRC for tags in beautified_tags])
        self.has_each_file_a_track_number = self._check_presence_in_all_tags(tag=[tags.TRCK for tags in beautified_tags])
        self.has_each_file_a_disc_number = self._check_presence_in_all_tags(tag=[tags.TPOS for tags in beautified_tags])

        self.is_score_or_soundtrack = self._check_album_is_score_or_soundtrack(folder_has_same_album=self.folder_has_same_album, album_name=beautified_tags[0].TALB)

    @staticmethod
    def _check_tag_uniformity(tag: List[Optional[str | int]]) -> bool:
        if None in tag:
            # TODO Print a warning in this case, although it is hard to be descriptives which tag is meant as inside this function it is hard to say what tag entered it.
            return False

        tag_unique = set(tag)

        if len(tag_unique) == 1:
            return True
        elif len(tag_unique) > 1:
            return False
        else:
            raise ValueError("This shouldn't happen.")

    @staticmethod
    def _check_presence_in_all_tags(tag: List[Optional[str | int]]) -> bool:
        if None in tag:
            # TODO Print a warning in this case, although it is hard to be descriptives which tag is meant as inside this function it is hard to say what tag entered it.
            return False
        else:
            return True

    @staticmethod
    def _check_album_is_score_or_soundtrack(folder_has_same_album: Optional[bool], album_name: Optional[str]) -> bool:
        if folder_has_same_album is False or album_name is None:
            return False

        if album_name.endswith(("(Score)", "(Soundtrack)")):
            return True

        else:
            return False
