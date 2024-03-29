import logging
from pathlib import Path
from typing import Optional

from pydantic_models.tag_models import TagsExportModel


class MP3FileName:
    def __init__(self, filepath: Path) -> None:
        self.filepath_inital = filepath.absolute()
        self.filepath_temp = Path(str(filepath.absolute()) + ".tmp")
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

        self.rename_file()

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

        disc_track_number = cls._generate_disc_track_number(
            has_each_file_a_disc_number=has_each_file_a_disc_number, has_each_file_a_track_number=has_each_file_a_track_number, tag_disc=tag_disc, tag_track=tag_track
        )

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

    def rename_file(self):

        self.filepath_inital.rename(
            self.filepath_temp
        )  # Some operating systems are case insensitive. Meaning a.mp3 and A.mp3 would be consider the same. Thus, an itermediate step with renaming into a tmp file name.
        self.filepath_temp.rename(self.filepath_beautified)

        self._log_changed_file_names()

    def _log_changed_file_names(self):
        if self.filepath_inital.name != self.filepath_beautified.name:
            with open("log_changed_track_names.log", mode="a", encoding="utf-8") as file:
                file.write(f"{self.filepath_inital.name} →\n{self.filepath_beautified.name}\n")
