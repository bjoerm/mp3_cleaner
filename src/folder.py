# TODO Handle case when files are in the main input folder level and not in a sub folder.

import glob
import logging
import shutil
from pathlib import Path
from shutil import copytree, ignore_patterns
from typing import List, Optional

import regex
import tomllib

from folderdescription import FolderDescription
from foldername import FolderName
from mp3file import MP3File


class FolderPreparation:
    @staticmethod
    def generate_output_folder(folder_main_input: Path, folder_main_output: Path, folder_full_input: Path) -> Path:
        """Generate the name of the output folder and create that folder."""
        folder_main_input_abs = folder_main_input.absolute().as_posix()
        folder_main_output_abs = folder_main_output.absolute().as_posix()
        folder_full_input_abs = folder_full_input.absolute().as_posix()

        folder_full_output = regex.sub(folder_main_input_abs, folder_main_output_abs, folder_full_input_abs)  # TODO It would be nice if this would use absolute folders to work if input and output were on different drives.
        folder_full_output = Path(folder_full_output)

        folder_full_output.mkdir(parents=True, exist_ok=True)

        return folder_full_output

    @staticmethod
    def copy_to_output_folder(folder_full_input: Path, folder_full_output: Path, unwanted_files: List[str]):
        copytree(src=folder_full_input, dst=folder_full_output, ignore=ignore_patterns(*unwanted_files), dirs_exist_ok=True)  # Unwanted files won't be copied. One could also remove dirs_exist_ok to get an error as the output should ideally be empty before mp3 cleaning


class Folder:
    def __init__(self, folder_full_input: Path, folder_main_input: Path, folder_main_output: Path, unwanted_files: List[str]) -> None:
        self.folder_full: Path
        self.mp3_filepaths: List[str]
        self.mp3_files: List[MP3File]
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

        self.name.beautify_and_write_foldername(
            tags_beautified=self.mp3_files[0].tags.tags_beautified,  # Using the first file for the album name as there won't be any changes if there are different album names.
            has_each_file_a_date=self.description.has_each_file_a_date,
            has_each_file_a_disc_number=self.description.has_each_file_a_disc_number,
            folder_has_same_album=self.description.folder_has_same_album,
            folder_has_same_artist=self.description.folder_has_same_artist,
            folder_has_same_date=self.description.folder_has_same_date,
            folder_has_same_disc_number=self.description.folder_has_same_disc_number,
            is_score_or_soundtrack=self.description.is_score_or_soundtrack,
        )

    def fetch_mp3_filepaths(self) -> List[str]:
        return glob.glob(f"{str(self.folder_full)}/*.mp3", recursive=False)  # Recursive=True would mess up some album wide defined methods in this class.
        # TODO Add support for other cases of writing .mp3. Also unify it to always be in smaller letters.

    def init_mp3_file_classes(self) -> List[MP3File]:
        return [MP3File(filepath=Path(i)) for i in self.mp3_filepaths]

    def beautify_tags_isolated_per_file(self):
        for file in self.mp3_files:
            file.tags.beautify_tags_isolated()

    def beautify_track_and_album_numbers(self):
        leading_zeros_track = self._calculate_leading_zeros(numbers=[file.tags.tags_beautified.TRCK for file in self.mp3_files])

        # Ensure that the tracks always have at least a length of 2 characters.
        if leading_zeros_track is not None:
            leading_zeros_track = max(2, leading_zeros_track)

        for file in self.mp3_files:
            file.tags._improve_disc_number(disc_number=file.tags.tags_beautified.TPOS, foldername=self.name.folderpath_inital.name, folder_has_same_disc_number=self.description.folder_has_same_disc_number)

        leading_zeros_album = self._calculate_leading_zeros(numbers=[file.tags.tags_beautified.TPOS for file in self.mp3_files])

        for file in self.mp3_files:
            file.tags.add_leading_zeros_track_and_album_number(
                leading_zeros_track=leading_zeros_track,
                leading_zeros_album=leading_zeros_album,
            )

    @staticmethod
    def _calculate_leading_zeros(numbers: List[Optional[str]]) -> Optional[int]:
        """Calculates the highest disc or track number that was encountered. If any number is missing (=None) or the highest number is 1, then None will be returned."""

        if None in numbers:
            return None

        else:
            numbers_as_int = [int(i) for i in numbers]
            highest_number = max(numbers_as_int)

            if highest_number == 1:
                return None

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

    with open("options.toml", "rb") as f:
        config = tomllib.load(f)

    main_input = Path("data/")
    main_ouput = Path("output/")

    if main_ouput.is_dir():
        shutil.rmtree(main_ouput)

    abc = Folder(folder_full_input=Path("data/wikimedia_commons/"), folder_main_input=main_input, folder_main_output=main_ouput, unwanted_files=config["unwanted_files"])
    abc.mp3_files[0].tags
    abc.folder_full

    logging.info("End of script reached.")  # TODO Add proper logging. Also replace old print statements...
