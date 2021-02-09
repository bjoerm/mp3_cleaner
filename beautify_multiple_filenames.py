# TODO Rename the folder as well.
# TODO Write tests for this class!


import os
import pandas as pd
import pathlib # Even though it is not explicitly called, it is needed as pathlib paths are later expanded.

class FileBeautifier:
    """
    This class provides beautified filenames based on the beautified tags. These beautified filenames are however only a first step and it is very likely that additional manual check and possibly corrections of the filenames are required.
    """
    
    
    @classmethod
    def beautify_filenames(cls, df: pd.DataFrame):
        """
        Main method for beautifying filenames.
        """
        
        is_same_artist = cls._check_for_same_artist(tags=df.beautified_tag)
        
        is_each_track_with_disc_number, is_each_track_with_track_number = cls._check_existance_of_disc_and_track_number(tags=df.beautified_tag)
        
        df["beautified_filename"] = cls._propose_multiple_filenames_from_multiple_tags(
            tags=df.beautified_tag
            , is_same_artist=is_same_artist
            , is_each_track_with_disc_number=is_each_track_with_disc_number
            , is_each_track_with_track_number=is_each_track_with_track_number
            )
        
        df["beautified_filepath"] = cls._propose_beautified_filepath(folder=df.folder, filename=df.beautified_filename)
        
        cls._write_filename_from_tags(filepath_current=df.filepath, filepath_beautified=df.beautified_filepath)
    
    
    @staticmethod
    def _check_for_same_artist(tags: pd.Series) -> bool:
        """
        Checks whether all tracks in this iteration have the same artist. If not all have it, the file renaming will be a bit different.
        
        Returns True for all tracks from the same artist, False for multiple artists and None for no artist information.
        """
        
        track_artist = set(tags[i].get("TPE1") for i in range(len(tags))) # Using set comprehension instead of list comprehension to remove duplicates.
        
        is_same_artist = None
        
        if track_artist is None:
            # Case when there is no track artist in all of the files.
            is_same_artist = None
        
        elif len(track_artist) == 1:
            # Case when all tracks have the same artist (which is not None).
            is_same_artist = True
        
        elif len(track_artist) > 1:
            # Case when there are multiple artists. This also includes the case when e.g. one track does not have a track artist tags but all others have one.
            is_same_artist = False
        
        else:
            raise ValueError("Length of track artist might be below 1.")
        
        return(is_same_artist)
    
    
    @classmethod
    def _check_existance_of_disc_and_track_number(cls, tags: pd.Series) -> tuple:
        """
        Checks whether all tracks in this iteration have a disc number and whether they all have a disc and track number. If not all have it, the file renaming will be a bit different.
        """
        
        disc_numbers = [tags[i].get("TPOS") for i in range(len(tags))]
        track_numbers = [tags[i].get("TRCK") for i in range(len(tags))]
        
        is_each_track_with_disc_number = cls._helper_existance_of_disc_and_track_number(tags=tags, list_of_numbers=disc_numbers)
        is_each_track_with_track_number = cls._helper_existance_of_disc_and_track_number(tags=tags, list_of_numbers=track_numbers)
        
        return(is_each_track_with_disc_number, is_each_track_with_track_number)
    
    
    @staticmethod
    def _helper_existance_of_disc_and_track_number(tags: pd.Series, list_of_numbers: list):
        """
        Helper method for _check_existance_of_disc_and_track_number to not there write the same code twice.
        """
        is_each_track_with_number = None
        
        if any(x is None for x in list_of_numbers):
            # Is there any None value in the track numbers.
            is_each_track_with_number = False
        
        elif len(list_of_numbers) == len(tags):
            # Are there as many (non None) track numbers as there files.
            is_each_track_with_number = True # Possible extension: You could make this even more sophisticated (either here or in the tag beautification) to check for multiple times the same track number.
        
        return(is_each_track_with_number)
    
    
    @classmethod
    def _propose_multiple_filenames_from_multiple_tags(cls, tags: pd.Series, is_same_artist: bool, is_each_track_with_disc_number: bool, is_each_track_with_track_number: bool) -> list:
        """
        For each of the tags, call the function to process a single tag.
        """
        
        beautified_filename = [
                cls._propose_single_filename_from_single_tag(
                    tag=tags[i]
                    , is_same_artist=is_same_artist
                    , is_each_track_with_disc_number=is_each_track_with_disc_number
                    , is_each_track_with_track_number=is_each_track_with_track_number
                    )
                for i in range(len(tags))
            ]
        
        return(beautified_filename)
    
    
    @classmethod
    def _propose_single_filename_from_single_tag(cls, tag: dict, is_same_artist: bool, is_each_track_with_disc_number: bool, is_each_track_with_track_number: bool) -> str: 
        """
        Returns a beautified filename based on the (beautified tags). Returns None for cases that important information is missing. In that case, the filename should not be changed.
        """
        
        if tag.get("TPE1") is None or tag.get("TIT2") is None:
            # Case where either the artist or the track name is missing in the tag.
            beautified_filename = None
            return(beautified_filename)
        
        # Creating required single pieces.
        artist = cls._beautify_string_from_tag(tag=tag.get("TPE1"), add_square_brackets=True)
        
        # Combining disc and track number, if available.
        number = "" # If there is no TPOS or TRCK, number will remain "".
        
        if is_each_track_with_disc_number == True & is_each_track_with_track_number == True:
            number = number + cls._beautify_string_from_tag(tag=tag.get("TPOS")) # Adding disc number, if the disc as well as the track number are present. (On purpose only TPOS is added here as TRCK is added below.)
        
        if is_each_track_with_track_number == True:
            number = number + cls._beautify_string_from_tag(tag=tag.get("TRCK")) # Adding disc number, if it is present.
        
        title = cls._beautify_string_from_tag(tag=tag.get("TIT2"))
        
        extension = "mp3" # Note that I am hardcoding here the file extension. Do not put a dot in front here! # TODO Raise exception would the total correct way instead of the comment before.
        
        # Constructing the filename from the pieces.
        ## Keep in mind that above it is ensured that artist and title are not none.
        if is_same_artist == True and is_each_track_with_track_number == True:
            beautified_filename = f'{artist} - {number or ""} - {title}.{extension}'
        
        elif is_same_artist == False and is_each_track_with_track_number == True:
            beautified_filename = f'{number or ""} - {artist} - {title}.{extension}'

        elif is_each_track_with_track_number == False:
            beautified_filename = f'{artist} - {title}.{extension}'

        else:
            # This should normally not be reached as the conditions above should capture all possible cases (as long as the input values are booleans).
            beautified_filename = None
        
        return(beautified_filename)
    
    
    @staticmethod
    def _beautify_string_from_tag(tag: str, add_square_brackets: bool = False) -> str:
        """
        This is a helper to make strings from tags (that shall be used for file names) more beautiful. It takes care of the case of tag = None.
        """
        
        if tag is None or tag == "" or tag == " ":
            tag = ""
            return(tag)
        
        else:
            tag = str(tag) # Short ensurer to prevent odd cases, when a tag is not a string.
        
        if add_square_brackets == True:
            tag = "[" + tag + "]"
        
        return(tag)
    
    
    @staticmethod
    def _propose_beautified_filepath(folder: pd.Series, filename: pd.Series) -> list:
        """
        Combines the beautified filename with the folder. Returns a list of pathlib paths.
        """
        
        filepath = [folder[i] / filename[i] if filename[i] is not None else None for i in range(len(folder))] # Will write None if the filename also is None.
        
        return(filepath)
    
    
    @staticmethod
    def _write_filename_from_tags(filepath_current, filepath_beautified):
        """
        Overwrites existing filename. However, if relevant tags are missing, then the file is not touched.
        """
        
        check_for_none = any(i is None for i in filepath_beautified)
        
        if check_for_none == True:
            return # Do not rename any files if there is any None value in the beautified filepath list.
        
        
        [os.rename(filepath_current[i], filepath_beautified[i]) for i in range(len(filepath_beautified))]

