import logging
import shutil
from pathlib import Path
from typing import Optional

import regex

from folder.description import FolderDescription
from pydantic_models.tag_models import TagsExportModel


class FolderName:
    def __init__(self, folderpath: Path) -> None:
        self.folderpath_inital = folderpath.absolute()
        self.folderpath_beautified: Path

    def beautify_and_write_foldername(self, tags_beautified: TagsExportModel, folder_description: FolderDescription):

        foldername_beautified = self.generate_beautified_foldername(
            foldername_initial=self.folderpath_inital.name,
            tag_artist=tags_beautified.TPE1,
            tag_album_name=tags_beautified.TALB,
            tag_date=tags_beautified.TDRC,
            has_each_file_a_date=folder_description.has_each_file_a_date,
            folder_has_same_album=folder_description.folder_has_same_album,
            folder_has_same_artist=folder_description.folder_has_same_artist,
            folder_has_same_date=folder_description.folder_has_same_date,
            is_score_or_soundtrack=folder_description.is_score_or_soundtrack,
        )

        self.folderpath_beautified = self.folderpath_inital.parent / foldername_beautified

        self.rename_folder()

    @classmethod
    def generate_beautified_foldername(
        cls,
        foldername_initial: str,
        tag_artist: str,
        tag_album_name: Optional[str],
        tag_date: Optional[str],
        has_each_file_a_date: bool,
        folder_has_same_album: bool,
        folder_has_same_artist: bool,
        folder_has_same_date: bool,
        is_score_or_soundtrack: bool,
    ) -> str:

        if tag_album_name is None:
            # Edge case: No album title.
            return foldername_initial

        if folder_has_same_album is False:
            # Edge case: Folder has different albums -> no change.
            # TODO What about None? Should this be included? Or just cange it so that folder_has_same_album can only be True/False and not None?
            return foldername_initial

        first_part = cls._generate_first_part(artist=tag_artist, album_name=tag_album_name, folder_has_same_artist=folder_has_same_artist, is_score_or_soundtrack=is_score_or_soundtrack)

        suffix_date = cls._generate_date_suffix(date=tag_date, folder_has_same_date=folder_has_same_date, has_each_file_a_date=has_each_file_a_date)

        return f"[{first_part}] - {tag_album_name}{suffix_date}"

    @classmethod
    def _generate_first_part(cls, artist: str, album_name: str, folder_has_same_artist: bool, is_score_or_soundtrack: bool) -> str:

        if is_score_or_soundtrack is True:
            first_part = cls._generate_first_part_score_soundtrack(album_name=album_name)

        elif folder_has_same_artist is False:
            first_part = "Various Artists"

        else:
            first_part = f"{artist}"

        return first_part

    @staticmethod
    def _generate_first_part_score_soundtrack(album_name: str) -> str:
        """Reduce the album name to its core elements, so they can be used as first part of the folder name.
        E.g. "Cool Movie 2" will be shortened to "Cool Movie"
        This won't fit each case, but at least the majority.
        """

        album_name = regex.sub(r"\(.+\)", "", album_name)  # Remove any strings in brackets (like Score, Soundtrack, ...).
        album_name = album_name.strip()
        album_name = regex.sub(r"\s\p{Pd}\s.+$", "", album_name)  # Remove anything that starts with a space-hyphen-space pattern.
        album_name = album_name.strip()
        album_name = regex.sub(r"\s\d+$", "", album_name)  # Remove any integers at the end. If this was "Great Movie 2", this will be changed into "Great Movie".
        album_name = album_name.strip()
        return album_name

    @staticmethod
    def _generate_date_suffix(
        date: Optional[str],
        has_each_file_a_date: bool,
        folder_has_same_date: bool,
    ):

        if has_each_file_a_date is True or folder_has_same_date is True:
            suffix_date = f" ({date})"
        else:
            suffix_date = ""

        return suffix_date

    def rename_folder(self):
        if self.folderpath_inital == self.folderpath_beautified:
            logging.debug(f"Folder {str(self.folderpath_inital)} was already beautiful. ;-)")

        elif self.folderpath_beautified.is_dir() is False:
            # Default case: Beautified folder does not yet exist.
            self.folderpath_inital.rename(self.folderpath_beautified)

        elif self.folderpath_beautified.is_dir():
            logging.warning(f"Folder {str(self.folderpath_beautified)} already existed. Beautified files from {str(self.folderpath_inital)} are copied into that folder.")
            shutil.copytree(src=self.folderpath_inital, dst=self.folderpath_beautified, dirs_exist_ok=True)
            shutil.rmtree(self.folderpath_inital)
