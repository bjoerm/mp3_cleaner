# TODO Prevent copying empty subfolders.
# TODO Be fine with files from the top level of the input folder (raise ValueError(f"Please move the files from the main directory into a subfolder. Example {in_input_path[0]}"))

import shutil
import tomllib
from datetime import datetime
from pathlib import Path

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

from folder.foldermain import Folder
from pydantic_models.config_model import Config


def mp3_cleaner():
    """Run this function after setting up the config.toml to clean and beautify"""

    with open("src/config.toml", "rb") as f:
        config = tomllib.load(f)
    config = Config(**config)

    if config.do_clean_output_folder is True:
        if config.output_path.absolute().is_dir():
            shutil.rmtree(config.output_path.absolute())
        for log in ["log_changed_folders.log", "log_changed_track_names.log"]:
            Path(log).unlink(missing_ok=True)

    mp3_folders = find_mp3_folders(input_path=config.input_path)

    clean_mp3s(mp3_folders=mp3_folders, input_path=config.input_path, output_path=config.output_path, unwanted_files=config.unwanted_files, threads=config.threads)


def find_mp3_folders(input_path: Path) -> list[Path]:
    mp3_files = [file for file in input_path.glob("**/*.mp3")]  # **/* is recursive. Each folder with mp3 files will enter a seperate Folder class.

    in_input_path = [file for file in input_path.glob("*.mp3")]  # Looking for files directly in the first level of the input path.

    if len(in_input_path) > 0:
        raise ValueError(f"Please move the files from the main directory into a subfolder. Example {in_input_path[0]}")

    mp3_folders = []
    for file in mp3_files:
        mp3_folders.append(Path(file).parent)

    unique_mp3_folders = list(set(mp3_folders))
    unique_mp3_folders.sort()

    return unique_mp3_folders


def clean_mp3s(mp3_folders: list[Path], input_path: Path, output_path: Path, unwanted_files: list[str], threads: int):
    print(f"Start of MP3 cleaning. Input path: {input_path}. Output path: {output_path}.")

    if threads == 1:
        for folder_i in tqdm(range(len(mp3_folders))):
            Folder(folder_full_input=mp3_folders[folder_i], folder_main_input=input_path, folder_main_output=output_path, unwanted_files=unwanted_files)

    elif threads > 1:

        def worker(folder_i: int):
            """Works on one folder at a time. Thus, can be used in parallel."""
            Folder(folder_full_input=mp3_folders[folder_i], folder_main_input=input_path, folder_main_output=output_path, unwanted_files=unwanted_files)

        thread_map(worker, range(len(mp3_folders)), desc="Folders", unit=" folders", max_workers=threads)  # Uses all cores. Number of parallel workers can be limited via , max_workers=1.


if __name__ == "__main__":
    start_time = datetime.now()
    print(f'Script started at {start_time.strftime("%H:%M:%S")}.')

    mp3_cleaner()

    finish_time = datetime.now()
    print(f'Script finished at {finish_time.strftime("%H:%M:%S")}.\nTook {round((finish_time - start_time).total_seconds(), 1)} seconds.')

    print("End of script reached.")
