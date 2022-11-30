# TODO Add a pydantic class for the folder that has a list (with at least one entry of tagsexported class)


import glob
import logging
import shutil
from pathlib import Path
from typing import List

import tomllib
from tqdm import trange

from folder.main import Folder
from pydantic_models.config_model import Config


def main():
    with open("src/config.toml", "rb") as f:
        config = tomllib.load(f)
    config = Config(**config)

    if config.clean_output_folder is True and config.output_path.absolute().is_dir():
        shutil.rmtree(config.output_path.absolute())

    mp3_folders = _find_mp3_folders(input_path=config.input_path)  # TODO .absolute()?

    for i in trange(len(mp3_folders)):
        logging.info(f"Processing: {mp3_folders[i]}")

        Folder(folder_full_input=mp3_folders[i], folder_main_input=config.input_path, folder_main_output=config.output_path, unwanted_files=config.unwanted_files)


def _find_mp3_folders(input_path: Path) -> List[Path]:

    mp3_files = [file for file in input_path.glob("**/*.mp3")]  # **/* is recursive. Each folder with mp3 files will enter a seperate Folder class.

    mp3_folders = []
    for file in mp3_files:
        mp3_folders.append(Path(file).parent)

    unique_mp3_folders = list(set(mp3_folders))
    unique_mp3_folders.sort()

    return unique_mp3_folders


if __name__ == "__main__":

    main()

    logging.info("End of script reached.")
