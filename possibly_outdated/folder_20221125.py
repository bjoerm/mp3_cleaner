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
    folder_child_output: str = field(init=False)  # TODO Ask Bodo whether one should do this as extra function that is then used, when needed instead of using self.folder_child_output at these places.
    unwanted_files: List[str]
    mp3_filepaths: List[str] = field(init=False)
    mp3_files: List[MP3File] = field(init=False)
    folder_has_same_artist: Optional[bool] = field(init=False)  # TODO Does this need to be its own variable? No, if this is only used once for renaming of files and folders.

    def __post_init__(self):
        self.folder_full_output = self.generate_output_folder()
        self.folder_child_output = self.folder_full_output.name

        self.copy_to_output_folder()

        self.mp3_filepaths = self.fetch_mp3_filepaths()

        self.mp3_files = self.init_mp3_file_classes()

        self.unify_folder_wide_tags()

        self.write_tags()

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

    def fetch_mp3_filepaths(self) -> List[str]:
        return glob.glob(f"{str(self.folder_full_output)}/*.mp3", recursive=False)  # Recursive=True would mess up some album wide defined methods in this class.

    def init_mp3_file_classes(self) -> List[MP3File]:
        return [MP3File(filepath=Path(i)) for i in self.mp3_filepaths]

    def unify_folder_wide_tags(self):
        """Beautify the tags that rely on information from album/folder level."""
        self.unify_track_and_album_numbers()

        # TODO Should these really be class variables? Or just local variables inside e.g. a renaming files and folder method?
        self.folder_has_same_artist = self.check_tag_uniformity(tag=[file.tags.TPE1 for file in self.mp3_files])
        self.folder_has_same_disc_number = self.check_tag_uniformity(tag=[file.tags.TPOS for file in self.mp3_files])
        self.folder_has_same_album = self.check_tag_uniformity(tag=[file.tags.TALB for file in self.mp3_files])
        self.folder_has_same_date = self.check_tag_uniformity(tag=[file.tags.TDRC for file in self.mp3_files])

        self.has_each_file_a_track_number = self.check_tag_uniformity(tag=[file.tags.TRCK for file in self.mp3_files]) is not None  # Using the effect that None is returned, if a None is detected.
        self.has_each_file_a_disc_number = self.check_tag_uniformity(tag=[file.tags.TPOS for file in self.mp3_files]) is not None

        # TODO Maybe a check whether it is a single file in the folder? This should affect the filename as well.

    def unify_track_and_album_numbers(self):
        leading_zeros_track = self.calculate_leading_zeros(numbers=[file.tags.TRCK for file in self.mp3_files])

        # Ensure that the tracks always have a length of 2 characters.
        if leading_zeros_track is not None:
            leading_zeros_track = max(2, leading_zeros_track)

        leading_zeros_album = self.calculate_leading_zeros(numbers=[file.tags.TPOS for file in self.mp3_files])

        for file in self.mp3_files:
            file.beautify_track_and_album_number(leading_zeros_track=leading_zeros_track, leading_zeros_album=leading_zeros_album)

    @staticmethod
    def check_tag_uniformity(tag: List[Optional[str | int]]) -> Optional[bool]:
        if None in tag:
            # TODO Print a warning in this case, although it is hard to be descriptives here if e.g. all entries are Nones.
            return None

        tag_unique = set(tag)

        if len(tag_unique) == 1:
            return True
        elif len(tag_unique) > 1:
            return False
        else:
            raise ValueError("This shouldn't happen.")

    @staticmethod
    def calculate_leading_zeros(numbers: List[Optional[str]]) -> Optional[int]:
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

    # One the album level:
    ## Check whether all files have the exact same tags present. If there are deviations, this might already be a hint to not rename anything. But this might be a bit too strict however...

    # self.beautify_filenames()
    # self.beautify_folders()

    def write_tags(self):

        for file in self.mp3_files:
            file.write_beautified_tags_to_file()


if __name__ == "__main__":

    with open("options.toml", "rb") as f:
        config = tomllib.load(f)

    abc = Folder(folder_full_input=Path("data/wikimedia_commons/"), folder_main_input=Path("data/"), folder_main_output=Path("output/"), unwanted_files=config["unwanted_files"])
    abc.mp3_files[0].tags
    abc.folder_full_output
