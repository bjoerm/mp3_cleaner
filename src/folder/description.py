from dataclasses import InitVar, field
from typing import List, Optional

from pydantic import StrictBool
from pydantic.dataclasses import dataclass

from pydantic_models.tag_models import TagsExportModel


@dataclass
class FolderDescription:
    """Class that storesfrom analyzing the tags of all files in the folder."""

    beautified_tags: InitVar[Optional[List[TagsExportModel]]]
    only_single_mp3_file: StrictBool = field(init=False)
    folder_has_same_album: StrictBool = field(init=False)
    folder_has_same_artist: StrictBool = field(init=False)
    folder_has_same_date: StrictBool = field(init=False)
    folder_has_same_disc_number: StrictBool = field(init=False)
    has_each_file_an_album: StrictBool = field(init=False)
    has_each_file_a_date: StrictBool = field(init=False)
    has_each_file_a_disc_number: StrictBool = field(init=False)
    has_each_file_a_track_number: StrictBool = field(init=False)
    is_score_or_soundtrack: StrictBool = field(init=False)

    def __post_init__(self, beautified_tags) -> None:
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
