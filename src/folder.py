import glob
from pathlib import Path
from shutil import copytree, ignore_patterns
from typing import List

import regex
import tomllib

from file import File


class Folder:
    def __init__(self, folderpath: Path, folder_main_input: Path, folder_main_output: Path, unwanted_files: List[str]):
        self.folder_full_input = folderpath
        self.folder_main_input = folder_main_input
        self.folder_main_output = folder_main_output
        self.folder_full_output = self.generate_output_folder()
        self.folder_child_output = self.folder_full_output.name

        self.unwanted_files = unwanted_files
        self.copy_to_output_folder()

        self.mp3_files = glob.glob(
            f"{str(self.folder_full_output)}/*.mp3", recursive=False
        )  # Setting recursive to False is done as each folder with MP3 files in it should get (currently, 2022-11) its own call of the Folder class. Recursive=True would mess up some album wide defined methods in this class.

        self.file_classes = self.init_file_classes()
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

    def init_file_classes(self) -> List[File]:

        list_of_file_classes = [File(Path(i)) for i in self.mp3_files]

        return list_of_file_classes


if __name__ == "__main__":

    with open("options.toml", "rb") as f:
        config = tomllib.load(f)

    abc = Folder(folder_main_input=Path("input/"), folder_main_output=Path("output/"), folderpath=Path("input/aMP3/"), unwanted_files=config["unwanted_files"])
