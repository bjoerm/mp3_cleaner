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
    has_only_one_artist: Optional[bool] = field(init=False)

    def __post_init__(self):
        self.folder_full_output = self.generate_output_folder()
        self.folder_child_output = self.folder_full_output.name

        self.copy_to_output_folder()

        self.mp3_filepaths = self.fetch_mp3_filepaths()

        self.mp3_files = self.init_mp3_file_classes()

        self.unify_folder_wide_tags()

    def copy_to_output_folder(self):
        copytree(src=self.folder_full_input, dst=self.folder_full_output, ignore=ignore_patterns(*self.unwanted_files), dirs_exist_ok=True)  # Unwanted files won't be copied. One could also remove dirs_exist_ok to get an error as the output should ideally be empty before mp3 cleaning

    def fetch_mp3_filepaths(self) -> List[str]:
        return glob.glob(f"{str(self.folder_full_output)}/*.mp3", recursive=False)  # Recursive=True would mess up some album wide defined methods in this class.

    def init_mp3_file_classes(self) -> List[MP3File]:
        return [MP3File(Path(i)) for i in self.mp3_filepaths]

    def unify_folder_wide_tags(self):
        """Beautify the tags that rely on information from album/folder level."""

        self.unify_track_and_album_numbers()
        self.has_only_one_artist = self.check_artist_uniqueness(artists=[file.tags.TPE1 for file in self.mp3_files])

        # TODO Continue here with checks for Nones. [file.tags.TDRC for file in self.mp3_files]

    def unify_track_and_album_numbers(self):
        leading_zeros_track = self.calculate_leading_zeros(numbers=[file.tags.TRCK for file in self.mp3_files])

        # Ensure that the tracks always have a length of 2 characters.
        if leading_zeros_track is not None:
            leading_zeros_track = max(2, leading_zeros_track)

        leading_zeros_album = self.calculate_leading_zeros(numbers=[file.tags.TPOS for file in self.mp3_files])

        for file in self.mp3_files:
            file.beautify_track_and_album_number(leading_zeros_track=leading_zeros_track, leading_zeros_album=leading_zeros_album)

    @staticmethod
    def check_artist_uniqueness(artists: List[Optional[str]]) -> Optional[bool]:
        # TODO Maybe rewrite this so that not a boolean is returned, but the artist name or None is returned instead. Maybe even a generalised "extract_and_check_uniqueness" method can be used for artist, year, album title?
        # TODO Write unittest!
        if None in artists:
            raise ValueError("At least one file is without artist tag.")

        artists_unique = set(artists)

        if len(artists_unique) == 1:
            return True
        elif len(artists_unique) > 1:
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
    ## self.check_missing_years()  # Log a warning if any of the Files lacks a year, track number, artist, title, if all/some (?) of the other songs have that field.
    # Validate the tags one more (with an output Pydantic class)
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


if __name__ == "__main__":

    with open("options.toml", "rb") as f:
        config = tomllib.load(f)

    abc = Folder(folder_full_input=Path("input/aMP3/"), folder_main_input=Path("input/"), folder_main_output=Path("output/"), unwanted_files=config["unwanted_files"])
    abc.mp3_files[0].tags
    abc.folder_full_output
