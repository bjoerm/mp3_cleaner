import glob
from dataclasses import dataclass, field
from pathlib import Path
from shutil import copytree, ignore_patterns
from typing import List, Optional

import regex
import tomllib

from mp3_file import MP3File


@dataclass
class Folder:
    folder_full_input: Path
    folder_main_input: Path
    folder_main_output: Path
    folder_full_output: Path = field(init=False)
    folder_child_output: str = field(init=False)
    unwanted_files: List[str]
    mp3_filepaths: List[str] = field(init=False)
    mp3_files: List[MP3File] = field(init=False)

    def __post_init__(self):
        self.folder_full_output = self.generate_output_folder()
        self.folder_child_output = self.folder_full_output.name

        self.copy_to_output_folder()

        self.mp3_filepaths = glob.glob(
            f"{str(self.folder_full_output)}/*.mp3", recursive=False
        )  # Setting recursive to False is done as each folder with MP3 files in it should get (currently, 2022-11) its own call of the Folder class. Recursive=True would mess up some album wide defined methods in this class.

        self.mp3_files = self.init_file_classes()

        self.calculate_folder_wide_tags()

    def calculate_folder_wide_tags(self):
        self.calculate_leading_zeros(numbers=[file.tags.TRCK for file in self.mp3_files])

        [file.tags.TPOS for file in self.mp3_files]

        pass

    @staticmethod
    def calculate_leading_zeros(numbers: List[Optional[int]]) -> Optional[int]:
        """Calculates the highest disc or track number that was encountered. If any number is missing (=None) or the highest number is 1, then None will be returned."""

        if None in numbers:
            return None

        else:
            highest_track_number = max(numbers)

            if highest_track_number == 1:
                return None

            highest_track_number = str(highest_track_number)
            length_string = len(highest_track_number)
            return length_string

    # TODO After the init album wide tags should be beautified (e.g. leading zeros in track numbers). This should be done via a (public) classmethod in File that gets e.g. the number of leading zeros from here (the album class). That way the File classes (inside thie file_classes list) are all updated.
    # TODO The same approach should be done for the other steps on the file (tag) level like writing tages etc.
    # Thus the following pseudo code shows the next steps:
    # self.calculate_leading_zeros_track()
    # self.calculate_leading_zeros_album()
    # self.any_other_album_wide_field_or_information() e.g. whether all have the same artist.
    # self.check_missing_years()  # Log a warning if any of the Files lacks a year, track number, artist, title, if all/some (?) of the other songs have that field.
    # self.convert_pydantic_tags_to_mutagen_object (maybe this is not even needed and all can be directly handled in the write method below)
    # self.write_beautified_tags()
    # self.beautify_filenames()
    # self.beautify_folders()

    def generate_output_folder(self):
        """Generate the name of the output folder and create that folder."""
        folder_main_input = str(self.folder_main_input)
        folder_main_output = str(self.folder_main_output)
        folder_full_input = str(self.folder_full_input)

        folder_full_output = regex.sub(folder_main_input, folder_main_output, folder_full_input)  # TODO It would be nice if this would use absolute folders to work if input and output were on different drives.
        folder_full_output = Path(folder_full_output)

        folder_full_output.mkdir(parents=True, exist_ok=True)

        return folder_full_output

    def copy_to_output_folder(self):
        copytree(src=self.folder_full_input, dst=self.folder_full_output, ignore=ignore_patterns(*self.unwanted_files), dirs_exist_ok=True)  # Unwanted files won't be copied. One could also remove dirs_exist_ok to get an error as the output should ideally be empty before mp3 cleaning

    def init_file_classes(self) -> List[MP3File]:

        list_of_file_classes = [MP3File(Path(i)) for i in self.mp3_filepaths]

        return list_of_file_classes


if __name__ == "__main__":

    with open("options.toml", "rb") as f:
        config = tomllib.load(f)

    abc = Folder(folder_full_input=Path("input/aMP3/"), folder_main_input=Path("input/"), folder_main_output=Path("output/"), unwanted_files=config["unwanted_files"])
    abc.folder_full_output
