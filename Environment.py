# TODO Where to do the conversion of mp3 file extensions to lowercase? In the other class it would be more fitting - although it will then not touch the files without tags. However, those files need to get a tag anyway before I can do anything with them.


import glob
import pandas as pd
from pathlib import Path
import shutil
import regex


class DataPreparer:
    @classmethod
    def prepare_input(cls, input_path: str, wip_path: str, log_path: str, overwrite_previous_output: bool, unwanted_files: list) -> pd.DataFrame:
        """
        This is the main method. It will create a copy of the files from the input path in the output path, delete unwanted files there and will finally generate a data frame with all mp3 files (and related folders). That data frame is then used in the next class.
        """

        cls._ensure_existance_of_required_folders(input_path, wip_path, log_path)

        cls._overwrite_previous_output(overwrite_previous_output=overwrite_previous_output, wip_path=wip_path)

        cls._create_copy_that_will_be_beautified(input_path=input_path, wip_path=wip_path)

        file_list = cls._list_all_files(wip_path=wip_path)

        cls._delete_unwanted_files_from_output(file_list=file_list, unwanted_files=unwanted_files)

        files_and_folders = cls._list_mp3_files_and_folders(file_list=file_list)

        return files_and_folders

    @staticmethod
    def _ensure_existance_of_required_folders(*args: tuple):
        """
        Ensure that all required folders exist (and create them if not).
        """

        for i in args:
            Path(i).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _overwrite_previous_output(overwrite_previous_output: bool, wip_path: str):
        """
        Will delete the content of the output folder, if that option is chosen.
        """

        if overwrite_previous_output is False:
            return

        else:  # Deleting the folder.
            shutil.rmtree(wip_path)

    @staticmethod
    def _create_copy_that_will_be_beautified(input_path: str, wip_path: str):
        """
        Copy files into a working folder so original files are not touched.
        """

        print("\n[Status] Creating copies of input files.")

        shutil.copytree(src=input_path, dst=wip_path)
        # TODO Once this is upgraded to Python 3.8 or higher, dirs_exist_ok=True can be easily used. shutil.copytree(src=input_path, dst=wip_path, dirs_exist_ok=True).

    @staticmethod
    def _list_all_files(wip_path: str) -> list:
        file_list = glob.glob(wip_path + "/**", recursive=True)

        return file_list

    @staticmethod
    def _delete_unwanted_files_from_output(file_list: list, unwanted_files: list):
        """
        Deletes unwanted files to have the output folder only contain only contain relevant files.
        """

        # Transforming everything (in this function) to lowercase.
        file_list = [file.lower() for file in file_list]
        unwanted_files = [file.lower() for file in unwanted_files]

        # Deleting unwanted files.
        files_to_delete = []

        for i in unwanted_files:
            files_to_delete += [file for file in file_list if file.endswith(i)]

        if len(files_to_delete) > 0:
            for i in files_to_delete:
                Path(i).unlink()

    @staticmethod
    def _list_mp3_files_and_folders(file_list: list):
        """
        This function will return a two column data frame with all mp3 files and the related folder.
        """

        # Filter the list of files to keep only the mp3 files.
        mp3_list = [file for file in file_list if regex.match(r".+\.mp3$", file, flags=regex.IGNORECASE) is not None]

        # Creating data frame of mp3 files.
        df_mp3 = pd.DataFrame(data=mp3_list, columns=["filepath"])
        df_mp3["filepath"] = df_mp3["filepath"].apply(Path)  # Converting into a pathlib Path object.
        df_mp3["folder"] = df_mp3["filepath"].apply(lambda x: x.parent)  # Getting the folder of that respective file.

        return df_mp3
