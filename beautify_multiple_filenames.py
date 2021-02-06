# TODO Folders are (as of now) not touched.

# TODO Should this be a function for improving multipe or single file names? Or is both needed?

# TODO Write tests for this class!

import os
import pandas as pd
import pathlib

class FileBeautifier:
    """
    This class provides beautified filenames based on the beautified tags. These beautified filenames are however only a first step and it is very likely that additional manual check and possibly corrections of the filenames are required.
    """
    
    
    @classmethod
    def beautify_filenames(cls, df: pd.DataFrame):
        
        print(df.file[0])
        print(df.folder[0])
        print(df.beautified_tag[0])
        
        is_same_artist = cls._check_for_same_artist(tags=df.beautified_tag)
        
        is_each_track_with_disc_number, is_each_track_with_track_number = cls._check_existance_of_disc_and_track_number(tags=df.beautified_tag)
        
        cls._propose_filename_from_tags(
            tag=df.beautified_tag
            , folder=df.folder
            , is_same_artist=is_same_artist
            , is_each_track_with_disc_number=is_each_track_with_disc_number
            , is_each_track_with_track_number=is_each_track_with_track_number
            )
        
        
        
    
    
    @staticmethod
    def _check_for_same_artist(tags: pd.Series) -> bool:
        """
        Checks whether all tracks in this iteration have the same artist. If not all have it, the file renaming will be a bit different.
        
        Returns True for all tracks from the same artist, False for multiple artists and None for no artist information.
        """
        
        track_artist = set(tags[i].get("TPE1") for i in range(len(tags))) # Using set comprehension instead of list comprehension to remove duplicates.
        
        is_same_artist = None
        
        if track_artist is None:
            # Case when no track artist exists in the tags of any the files.
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
    def _check_existance_of_disc_and_track_number(cls, tags: pd.Series) -> list: # Returns a list of two booleans.
        """
        Checks whether all tracks in this iteration have a disc number and whether they all have a track number. If not all have it, the file renaming will be a bit different.
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
    
    
    @staticmethod
    def _propose_filename_from_tags(tag: dict, folder: pathlib.WindowsPath, is_same_artist:bool, is_each_track_with_disc_number: bool, is_each_track_with_track_number: bool): # Note to self: Should I generally keep folder and file in df_iteration just as string and not pathlib objects?
        """
        Returns a beautified filename based on the (beautified tags).
        """
        # TODO The output from this shall be added as column to the df_iteration, so that one is later saved as well.
        
        # TODO Basic logic should be:
        ## TODO If all tracks from same artist, then use {[Artist]} - {DiscNumber if multidisk}{Tracknumber if exists} - {Title}.mp3 # Maybe also only use tracknumber is it exists in all songs in the folder.
        ## TODO If from multiple artists, then use {DiscNumber if multidisk}{Tracknumber if exists} - {[Artist]} - {Title}.mp3 # Maybe also only use tracknumber is it exists in all songs in the folder.
        
        
        pass
    
    
    def _write_filename_from_tags(filename_current, filename_beautified):
        """
        Overwrites existing filename. However, if relevant tags are missing, then the file is not touched.
        """
        pass
    
    
        # TODO os.rename("new", "new")
    
        # TODO Add handling of edge cases where relevant tags are missing and filename shall then not be touched.