import pathlib

import pandas as pd
import regex


class FileBeautifier:
    """
    This class provides beautified filenames based on the beautified tags. These beautified filenames are however only a first step and it is very likely that additional manual check and possibly corrections of the filenames are required.
    """

    @classmethod
    def beautify_filenames(cls, df: pd.DataFrame, has_file_without_tags: bool):
        """
        Main method for beautifying filenames.
        """

        # Helper checks for the renaming.
        is_same_artist = cls._check_uniqueness_of_tag(tags=df.beautified_tag, id3_field="TPE1")
        (
            is_each_track_with_disc_number,
            is_each_track_with_track_number,
        ) = cls._check_existance_of_disc_and_track_number(tags=df.beautified_tag)
        is_same_disc_number = cls._check_uniqueness_of_tag(tags=df.beautified_tag, id3_field="TPOS")
        is_same_album_title = cls._check_uniqueness_of_tag(tags=df.beautified_tag, id3_field="TALB")
        is_same_date = cls._check_uniqueness_of_tag(tags=df.beautified_tag, id3_field="TDRC")

        df["beautified_filename"] = cls._propose_multiple_filenames_from_multiple_tags(  # Filename only.
            tags=df.beautified_tag,
            is_same_artist=is_same_artist,
            is_each_track_with_disc_number=is_each_track_with_disc_number,
            is_each_track_with_track_number=is_each_track_with_track_number,
        )

        df["beautified_filepath"] = cls._generate_beautified_pathlib_filepath(folder=df.folder, filename=df.beautified_filename)  # Folder plus filename.

        cls._write_filename(filepath_current=df.filepath, filepath_beautified=df.beautified_filepath)

        df["beautified_folder"] = cls._beautify_folder_name(
            tags=df.beautified_tag,
            has_file_without_tags=has_file_without_tags,
            is_same_artist=is_same_artist,
            is_same_album_title=is_same_album_title,
            is_same_date=is_same_date,
            is_each_track_with_disc_number=is_each_track_with_disc_number,
            is_same_disc_number=is_same_disc_number,
        )

        cls._rename_folder(folder_current=df.folder, beautified_folder=df.beautified_folder)

    @staticmethod
    def _check_uniqueness_of_tag(tags: pd.Series, id3_field: str) -> bool:
        """
        Checks whether or not all entries of the specified id3 field contain the same value (e.g. whether all have the same artist).

        Returns True if that is the case or False if there are multiple different values of the specified id3 field within the entries. And None if there are no information.
        """

        unique_entries = set(tags[i].get(id3_field) for i in range(len(tags)))  # Using set comprehension instead of list comprehension to remove duplicates.
        unique_entries = list(unique_entries)

        is_unique = None

        if unique_entries is None or unique_entries == [None]:
            # Case when there is no track artist in all of the files.
            is_unique = None

        elif len(unique_entries) == 1:
            # Case when all tracks have the same artist (which is not None).
            is_unique = True

        elif len(unique_entries) > 1:
            # Case when there are multiple artists. This also includes the case when e.g. one track does not have a track artist tags but all others have one.
            is_unique = False

        else:
            raise ValueError("This should not be reached. Length of tag entries might be below 1.")

        return is_unique

    @classmethod
    def _check_existance_of_disc_and_track_number(cls, tags: pd.Series) -> tuple:
        """
        Checks whether all tracks in this iteration have a disc number and whether they all have a disc and track number. If not all have it, the file renaming will be a bit different.
        """

        disc_numbers = [tags[i].get("TPOS") for i in range(len(tags))]
        track_numbers = [tags[i].get("TRCK") for i in range(len(tags))]

        is_each_track_with_disc_number = cls._helper_existance_of_disc_and_track_number(tags=tags, list_of_numbers=disc_numbers)
        is_each_track_with_track_number = cls._helper_existance_of_disc_and_track_number(tags=tags, list_of_numbers=track_numbers)

        return (is_each_track_with_disc_number, is_each_track_with_track_number)

    @staticmethod
    def _helper_existance_of_disc_and_track_number(tags: pd.Series, list_of_numbers: list) -> bool:
        """
        Helper method for _check_existance_of_disc_and_track_number to not write the same code twice.
        """
        is_each_track_with_number = None

        if any(x is None for x in list_of_numbers):
            # Is there any None value in the track numbers.
            is_each_track_with_number = False

        elif len(list_of_numbers) == len(tags):
            # Are there as many (non None) track numbers as there files.
            is_each_track_with_number = True  # Possible extension: You could make this even more sophisticated (either here or in the tag beautification) to check for multiple times the same track number.

        return is_each_track_with_number

    @classmethod
    def _propose_multiple_filenames_from_multiple_tags(
        cls,
        tags: pd.Series,
        is_same_artist: bool,
        is_each_track_with_disc_number: bool,
        is_each_track_with_track_number: bool,
    ) -> list:
        """
        For each of the tags, call the function to process a single tag.
        """

        beautified_filename = [
            cls._propose_single_filename_from_single_tag(
                tag=tags[i],
                is_same_artist=is_same_artist,
                is_each_track_with_disc_number=is_each_track_with_disc_number,
                is_each_track_with_track_number=is_each_track_with_track_number,
            )
            for i in range(len(tags))
        ]

        return beautified_filename

    @classmethod
    def _propose_single_filename_from_single_tag(
        cls,
        tag: dict,
        is_same_artist: bool,
        is_each_track_with_disc_number: bool,
        is_each_track_with_track_number: bool,
    ) -> str:
        """
        Returns a beautified filename based on the (beautified tags). Returns None for cases that important information is missing. In that case, the filename should not be changed.
        """

        if tag.get("TPE1") is None or tag.get("TIT2") is None:
            # Case where either the artist or the track name is missing in the tag.
            beautified_filename = None
            return beautified_filename

        # Creating required single pieces.
        artist = cls._beautify_string_from_tag(tag=tag.get("TPE1"), add_square_brackets=True)

        # Combining disc and track number, if available.
        number = ""  # If there is no TPOS or TRCK, number will remain "".

        if is_each_track_with_disc_number is True & is_each_track_with_track_number is True:
            number = cls._beautify_string_from_tag(tag=tag.get("TPOS"))  # Adding disc number, if the disc as well as the track number are present. (On purpose only TPOS is added here as TRCK is added below.)

        if is_each_track_with_track_number is True:
            number = number + cls._beautify_string_from_tag(tag=tag.get("TRCK"))  # Adding disc number, if it is present.

        title = cls._beautify_string_from_tag(tag=tag.get("TIT2"))

        extension = "mp3"  # Note that I am hardcoding here the file extension. Do not put a dot in front here!

        # Constructing the filename from the pieces. Keep in mind that above it is ensured that artist and title are not none.
        if is_same_artist is True and is_each_track_with_track_number is True:
            beautified_filename = f'{artist} - {number or ""} - {title}.{extension}'

        elif is_same_artist is False and is_each_track_with_track_number is True:
            beautified_filename = f'{number or ""} - {artist} - {title}.{extension}'

        elif is_each_track_with_track_number is False:
            beautified_filename = f"{artist} - {title}.{extension}"

        else:
            # This should normally not be reached as the conditions above should capture all possible cases (as long as the input values are booleans).
            beautified_filename = None

        return beautified_filename

    @staticmethod
    def _beautify_string_from_tag(tag: str, add_square_brackets: bool = False) -> str:
        """
        This is a helper to make a string from a tag (that shall be used for file names) more beautiful. It also takes care of the case of tag = None and can add square brackets (e.g. around artist name).
        """

        if tag is None or tag == "" or tag == " ":
            tag = ""
            return tag

        else:
            tag = str(tag)  # Short ensurer to prevent odd cases, when a tag is not a string.

        if add_square_brackets is True:
            tag = "[" + tag + "]"

        return tag

    @staticmethod
    def _generate_beautified_pathlib_filepath(folder: pd.Series, filename: pd.Series) -> list:
        """
        Combines the beautified filename with the folder. Returns a list of pathlib paths.
        """

        filepath = [folder[i] / filename[i] if filename[i] is not None else None for i in range(len(folder))]  # Will write None if the filename also is None.

        return filepath

    @staticmethod
    def _write_filename(filepath_current: pd.Series, filepath_beautified: pd.Series):
        """
        Overwrites existing filename. However, if relevant tags are missing, then the file is not touched.
        """

        check_for_none = any(i is None for i in filepath_beautified)

        if check_for_none is True:
            return  # Do not rename any files if there is any None value in the beautified filepath list.

        else:

            # TODO Also have a check that there are no duplicates in filepath_beautified.

            # Only rename files to new filenames if those do not already exist.
            check_filepath_already_exists = [pathlib.Path(filepath_beautified[i]).is_file() for i in range(len(filepath_beautified))]

            if any(i is True for i in check_filepath_already_exists) is True:
                return

            [filepath_current[i].rename(filepath_beautified[i]) for i in range(len(filepath_beautified))]

    @classmethod
    def _beautify_folder_name(
        cls,
        tags: pd.Series,
        has_file_without_tags: bool,
        is_same_artist: bool,
        is_same_album_title: bool,
        is_same_date: bool,
        is_each_track_with_disc_number: bool,
        is_same_disc_number: bool,
    ) -> str:
        """
        Generate improved folder names from the tags. The input tags must be the already beautified ones. If a None is returned, the folder name will not be touched.
        """

        # Cases where the folder name shall remain untouched.
        if has_file_without_tags is True:  # If there are any mp3 files without tags in the folder, do not rename the folder.
            return

        if is_same_album_title is not True:
            return

        elif (is_same_artist is False or is_same_artist is None) and not tags[0].get("TALB").endswith(("(Score)", "(Soundtrack)")) and is_same_album_title is not True:
            return

        # Creating required single pieces.
        artist = cls._beautify_string_from_tag(tag=tags[0].get("TPE1"), add_square_brackets=True)  # Pulling the artist information from the information on the first mp3 file.

        album = cls._beautify_string_from_tag(tag=tags[0].get("TALB"))

        # Dealing with special case of soundtracks and scores.
        if album.endswith(("(Score)", "(Soundtrack)")):
            artist = cls._beautify_string_from_tag(tag=tags[0].get("TALB"), add_square_brackets=False)
            artist = regex.sub(r"\(.+\)", "", artist)  # Remove any strings in brackets.
            artist = artist.strip()
            artist = regex.sub(r"\s\p{Pd}\s.+$", "", artist)  # Remove anything that starts with a space-hyphen-space pattern.
            artist = artist.strip()
            artist = regex.sub(r"\s\d+$", "", artist)  # Remove any integers add the end. If this was Terminator 2, this will be changed into Terminator.
            artist = artist.strip()
            artist = f"[{artist}]"

        # Dealing with special case of various artists but given album title
        if (is_same_artist is False or is_same_artist is None) and not tags[0].get("TALB").endswith(("(Score)", "(Soundtrack)")) and is_same_album_title is True:
            artist = "[Various Artists]"

        disc_number = ""

        if is_each_track_with_disc_number is True:
            disc_number = cls._beautify_string_from_tag(tag=tags[0].get("TPOS"))  # This just takes the disc number from the first file.

        date = ""

        if is_same_date is True:
            date = cls._beautify_string_from_tag(tag=tags[0].get("TDRC"))

        # Constructing the folder name from the pieces. Keep in mind that above it is ensured that artist and album title are unique and not none.
        beautified_folder = None

        if is_same_date is True and is_each_track_with_disc_number is True and is_same_disc_number is True:
            beautified_folder = f"{artist} - {album} (CD{disc_number}) ({date})"

        elif is_same_date is True and is_each_track_with_disc_number is True and is_same_disc_number is False:
            beautified_folder = f"{artist} - {album} ({date})"

        elif is_same_date is True and (is_each_track_with_disc_number is False or is_each_track_with_disc_number is None):
            beautified_folder = f"{artist} - {album} ({date})"

        elif (is_same_date is False or is_same_date is None) and is_each_track_with_disc_number is True and is_same_disc_number is True:
            beautified_folder = f"{artist} - {album} (CD{disc_number})"

        elif (is_same_date is False or is_same_date is None) and is_each_track_with_disc_number is True and is_same_disc_number is False:
            beautified_folder = f"{artist} - {album}"

        elif (is_same_date is False or is_same_date is None) and (is_each_track_with_disc_number is False or is_each_track_with_disc_number is None):
            beautified_folder = f"{artist} - {album}"

        else:
            # This should normally not be reached as the conditions above should capture all possible cases (as long as the input values are booleans).
            beautified_folder = None

        return beautified_folder

    @staticmethod
    def _rename_folder(folder_current: pd.Series, beautified_folder: pd.Series):
        """
        Renames existing folder. However, if relevant tags are missing or special cases occur (like mixed artists), then the folder is not touched.
        """

        check_for_none = any(i is None for i in beautified_folder)

        if check_for_none is True:
            return  # Do not rename any files if there is any None value in the beautified filepath list.

        else:
            folder_current = folder_current[0]  # This is a pathlib object.
            beautified_folder = beautified_folder[0]

            beautified_folder = folder_current.parent / beautified_folder  # Only rename the last item of the folder path. Files in subdirectories are that way not moved around.

            if pathlib.Path(beautified_folder).is_dir():
                print(f"[Error] {beautified_folder} already exists. Folder was not renamed.")
            else:
                folder_current.rename(beautified_folder)
