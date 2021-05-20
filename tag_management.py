# TODO Add option to turn file and folder renaming on and off.
# TODO Add functionality to move "Feat. xyz" from artist to end of the title. Be however aware of possible problems with other suffixes like "(Live), (Remix), ...".
# TODO Low prio: Is it possible to not update the date of a file when an improved id tag is written?


import datetime
from mutagen.id3 import APIC, POPM, TALB, TDRC, TIT2, TPE1, TPE2, TPOS, TRCK
from mutagen.mp3 import MP3  # Alternative to ID3 and ID3NoHeaderError.
import pandas as pd
from tqdm import trange

from beautify_multiple_tags import TagBeautifier
from beautify_filepaths import FileBeautifier


class TagManager:

    @classmethod
    def improve_tags(cls, selected_id3_fields: list, files_and_folders: pd.DataFrame):
        """
        This method gets the folder list from the Environment class as input. It then goes iteratively through each folder and reads the tags from all MP3 files in that folder. The read tags are saved as mutagen ID3 objects. These tags are then beautified. The beautified tags then replace the originally read mutagen ID3 objects. Finally these are used to overwrite the tags in the mp3 files.
        """

        unique_mp3_folders = cls._get_unique_mp3_folders(files_and_folders=files_and_folders)

        df_log = pd.DataFrame()

        # Work from folder to folder.
        for i in trange(len(unique_mp3_folders)):  # Switch to range instead of trange if you don't want a progress bar from tqdm.
            print("Processing: " + str(unique_mp3_folders[i]))  # TODO Include this better into tqdm.

            df_iteration = None  # Cleaning the iteration df at the start of each loop.

            df_iteration = cls._select_folder_for_iteration(files_and_folders=files_and_folders, current_unique_folder=unique_mp3_folders[i])

            # Read all tags in folder
            df_iteration["id3"] = cls._read_id3_tags_in_folder(paths_to_files=df_iteration["filepath"])

            # Keep only selected tags
            df_iteration["unchanged_tag"] = cls._keep_only_selected_tags(id3_column=df_iteration["id3"], selected_id3_fields=selected_id3_fields)

            # Remove encoding information and only keep the text.
            df_iteration["unchanged_tag"] = cls._remove_string_encoding_information(tags=df_iteration["unchanged_tag"])

            # Skip files without (relevant) ID3 tags.
            df_iteration, has_file_without_tags = cls._skip_files_without_tags(df=df_iteration)

            # Deal with case that all files in current folder can be without relevant tags (then continue to the next folder).
            if len(df_iteration) == 0:
                continue

            # Pass tag on to the beautifier utility class.
            df_iteration["beautified_tag"] = TagBeautifier.beautify_tags(tags=df_iteration["unchanged_tag"].copy(), path=unique_mp3_folders[i])  # Input for path refers to the currently processed folder.

            df_iteration["id3"] = cls._overwrite_tags_in_id3_object(id3_column=df_iteration["id3"], beautified_tag=df_iteration["beautified_tag"])

            # Write beautified tag to file.
            cls._write_beautified_tag_to_files(id3_column=df_iteration["id3"])

            # Beautify the filename.
            FileBeautifier.beautify_filenames(df=df_iteration, has_file_without_tags=has_file_without_tags)

            # Keep a log of the tags. Be aware that this might get big, if at some point the tag with an image of the album cover would be included.
            df_log = df_log.append(df_iteration)

        # Export a log of the untouched and beautified tags
        df_log = df_log.astype(str)
        df_log.to_parquet("logs\\log_" + str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")) + "_" + str(len(df_log)) + "_Tracks" + ".parquet")

    @staticmethod
    def _get_unique_mp3_folders(files_and_folders: list) -> list:
        """
        Get list of unique folders with mp3 files in it. This will be a helper for a following loop.
        """

        unique_mp3_folders = files_and_folders.copy()
        unique_mp3_folders = unique_mp3_folders.folder.unique()
        unique_mp3_folders = list(unique_mp3_folders)

        return unique_mp3_folders

    @staticmethod
    def _select_folder_for_iteration(files_and_folders: pd.DataFrame, current_unique_folder) -> pd.DataFrame:
        """
        Selecting the files in the i'th unique folder.
        """

        df_iteration = files_and_folders[(files_and_folders.folder == current_unique_folder)].copy()  # The .copy() is required to have a real copy and not just a view of the list.

        df_iteration = df_iteration.reset_index(drop=True)

        return df_iteration

    @classmethod
    def _read_id3_tags_in_folder(cls, paths_to_files: pd.Series) -> pd.Series:
        """
        Read the whole id3 tags for all provided files.
        """

        id3 = [cls._read_id3_tag_from_single_file(i) for i in paths_to_files]  # Read all tags.

        return id3

    @staticmethod
    def _read_id3_tag_from_single_file(filepath):
        """
        Read the whole id3 tag for a single file.
        """

        mp3 = MP3(filepath)
        if mp3.tags is None:
            mp3.add_tags()
        id3 = mp3.tags  # Only fetching the id3 tag.
        id3.filename = mp3.filename  # Adding the filename as that is not passed.

        return id3  # Returns an ID3 object.

    @staticmethod
    def _keep_only_selected_tags(id3_column: pd.Series, selected_id3_fields: list) -> pd.DataFrame:
        """
        Filtering of the original tag information to only keep the defined tag fields.
        """

        unchanged_tag = [
            {
                k: v for (k, v) in id3_column[i].items() if k in selected_id3_fields
            }  # Selecting only the tags that are specified in selected_id3_fields
            for i in id3_column.index
            ]

        assert len(id3_column) == len(unchanged_tag), "Test for not loosing tags."

        return unchanged_tag

    @staticmethod
    def _remove_string_encoding_information(tags: pd.Series) -> pd.Series:
        """
        Getting rid of the encoding part and only keeping the "text", so it will later be unifiedly be saved as UTF8 and not e.g. LATIN1. So changing 'TALB(encoding=<Encoding.LATIN1: 0>, text=['Stellaris : Ancient Relics'])' into a simple dictionary 'TALB: 'Stellaris : Ancient Relics').
        """

        output = tags.copy()

        output = [
            dict(
                (
                    k
                    , output[i].get(k).text[0] if k not in ("APIC:", "POPM:no@email")  # Not touching the rating field ("POPM:no@email") and the album art as those do not contain any "text" element.
                    else output[i].get(k)
                ) for k in output[i]
            ) for i in output.index
            ]

        output = pd.Series(output)  # Converting back into a pd.Series.

        assert len(output) == len(tags), "Test for not loosing tags."

        return output

    @staticmethod
    def _skip_files_without_tags(df: pd.DataFrame) -> tuple:
        """
        Skipping the files that have either no ID3 tag or that have no relevant/defined ID3 tag. They will be skipped in the following beautification as the tags are empty anyway.
        """

        has_file_without_tags = False

        if len(df) > len(df[df.unchanged_tag != {}]):

            has_file_without_tags = True

            df = df[df.unchanged_tag != {}]

            df = df.reset_index(drop=True)

        return df, has_file_without_tags

    @classmethod
    def _overwrite_tags_in_id3_object(cls, id3_column: pd.Series, beautified_tag: pd.Series) -> pd.Series:
        """
        Overwrite existing tags from the ID3 object that is saved in the id3 column of the df_iteration.
        """
        # Delete all existing tags from the ID3 object.
        [id3_column[i].delete() for i in id3_column.index]

        # Create new ID3 object from beautified tag.
        id3_column = [cls._save_tags_to_single_id3_object(id3=id3_column[i], beautified_tag=beautified_tag[i]) for i in id3_column.index]  # This will pass each i (file's ID3 tag) to the save function.

        return id3_column

    @staticmethod
    def _save_tags_to_single_id3_object(id3, beautified_tag):
        """
        Save beautified tags to id3 object. This function takes only on row from df_iteration at a time.
        """

        for key, value in beautified_tag.items():

            if key in ("POPM:no@email", "APIC:"):  # Does not have a text field and thus a bit different structure.
                id3.add(value)
                # exec(f'id3.add({value})')

            elif key in ("TALB", "TDRC", "TIT2", "TPE1", "TPE2", "TPOS", "TRCK"):  # These fields (all but rating), have a text parameter which can be added the same way.
                exec(f'id3.add({key}(encoding = 3, text = "{value}"))')  # encoding = 3 = UTF8 # Executes the following string as Python command. The f in the beginning marks this as "f string". See https://www.python.org/dev/peps/pep-0498/


            else:
                # This else condition should not be reached. It is used to raise an alert, when new tag types are entered in the global variables but not yet defined here.
                raise NameError("It seems like a new key was added to options but not added to the handling above in this method.")

        return id3

    @staticmethod
    def _write_beautified_tag_to_files(id3_column: pd.Series):
        """
        Write the beautified tag from the id3 object to the respective files.
        """

        # TODO Have some more checks to ensure that the correct file is gets the correct tag.

        [id3_column[i].save(v1=0, v2_version=4) for i in id3_column.index]  # Saving only as id3v2.4 tags and not as id3v1 at all.
