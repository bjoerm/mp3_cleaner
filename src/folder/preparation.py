from pathlib import Path
from shutil import copytree, ignore_patterns
from typing import List

import regex


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
