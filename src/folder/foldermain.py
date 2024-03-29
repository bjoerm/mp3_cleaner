import logging
import shutil
from pathlib import Path
from typing import Optional

import tomllib

from file.filemain import MP3File
from folder.folderdescription import FolderDescription
from folder.foldername import FolderName
from folder.folderpreparation import FolderPreparation


class Folder:
    def __init__(self, folder_full_input: Path, folder_main_input: Path, folder_main_output: Path, unwanted_files: list[str]) -> None:
        self.folder_full: Path
        self.mp3_filepaths: list[Path]  # Contains only .mp3 files.
        self.mp3_files: list[MP3File]
        self.description: FolderDescription
        self.name: FolderName

        self.folder_full = FolderPreparation.generate_output_folder(folder_full_input=folder_full_input, folder_main_input=folder_main_input, folder_main_output=folder_main_output)
        FolderPreparation.copy_to_output_folder(folder_full_input=folder_full_input, folder_full_output=self.folder_full, unwanted_files=unwanted_files)

        self.name = FolderName(folderpath=self.folder_full)

        self.mp3_filepaths = self.fetch_mp3_filepaths()
        self.mp3_files = self.init_mp3_file_classes()

        self.beautify_tags_isolated_per_file()

        self.description = FolderDescription(beautified_tags=[file.tags.tags_beautified for file in self.mp3_files])

        self.beautify_track_and_album_numbers()

        self.write_tags()

        self.beautify_and_write_filenames()

        self.name.beautify_and_write_foldername(tags_beautified=self.mp3_files[0].tags.tags_beautified, folder_description=self.description)  # Using the first file for the folder name as there won't be any changes if there are different album names.

    def fetch_mp3_filepaths(self) -> list[Path]:
        mp3_files = [f for f in self.folder_full.glob("*.mp3")]  # This is not recursive (and that is intended as any folder with mp3 files gets its own folder class).

        if len(mp3_files) == 0:
            raise ValueError("No .mp3 files were found. This shouldn't be possible.")

        return mp3_files

    def init_mp3_file_classes(self) -> list[MP3File]:
        return [MP3File(filepath=i) for i in self.mp3_filepaths]

    def beautify_tags_isolated_per_file(self):
        for file in self.mp3_files:
            file.tags.beautify_tags_isolated()

    def beautify_track_and_album_numbers(self):
        leading_zeros_track = self._calculate_leading_zeros(numbers=[file.tags.tags_beautified.TRCK for file in self.mp3_files])

        # Ensure that the tracks always have at least a length of 2 characters.
        if leading_zeros_track is not None:
            leading_zeros_track = max(2, leading_zeros_track)

        for file in self.mp3_files:
            file.tags.tags_beautified.TPOS = file.tags._improve_disc_number(disc_number=file.tags.tags_beautified.TPOS, foldername=self.name.folderpath_inital.name, folder_has_same_disc_number=self.description.folder_has_same_disc_number)

        self.description.has_each_file_a_disc_number = self.description._check_presence_in_all_tags(tag=[tags.tags.tags_beautified.TPOS for tags in self.mp3_files])  # Update the description after potential changes to disc number from above.

        leading_zeros_disc = self._calculate_leading_zeros(numbers=[file.tags.tags_beautified.TPOS for file in self.mp3_files])

        for file in self.mp3_files:
            file.tags.add_leading_zeros_track_and_album_number(
                leading_zeros_track=leading_zeros_track,
                leading_zeros_disc=leading_zeros_disc,
            )

    @staticmethod
    def _calculate_leading_zeros(numbers: list[Optional[str]]) -> Optional[int]:
        """Calculates the highest disc or track number that was encountered as long as all tracks in the folder have a number. This has to be done on the album level."""

        if None in numbers:
            return None

        else:
            numbers_as_int = [int(i) for i in numbers]
            highest_number = max(numbers_as_int)
            highest_number = str(highest_number)
            length_string = len(highest_number)

            return length_string

    def write_tags(self):
        for file in self.mp3_files:
            file.tags.write_beautified_tags_to_file()

    def beautify_and_write_filenames(self):
        for file in self.mp3_files:
            file.name.beautify_and_write_filename(
                tags_beautified=file.tags.tags_beautified,
                only_single_mp3_file=self.description.only_single_mp3_file,
                folder_has_same_artist=self.description.folder_has_same_artist,
                has_each_file_a_disc_number=self.description.has_each_file_a_disc_number,
                has_each_file_a_track_number=self.description.has_each_file_a_track_number,
            )


if __name__ == "__main__":

    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    main_input = Path("data/")
    main_ouput = Path("output/")

    if main_ouput.is_dir():
        shutil.rmtree(main_ouput)

    somefolder = Folder(folder_full_input=Path(main_input / "wikimedia_commons"), folder_main_input=main_input, folder_main_output=main_ouput, unwanted_files=config["unwanted_files"])
    somefolder.mp3_files[0].tags
    somefolder.folder_full

    logging.info("End of script reached.")
