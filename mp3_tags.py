# TODO Check special character case.


from mutagen.id3 import ID3, ID3NoHeaderError, POPM, TALB, TDRC, TIT2, TPE1, TPE2, TPOS, TRCK
import pandas as pd
import re

from string_beautification import string_beautification
from track_number_beautification import track_number_beautification


class Mp3Tags:
    
    # This class should be getting the unique_folder list from the Environment class as input.
    
    def __init__(self, selected_id3_fields, files_and_folders):
        self.files_and_folders = files_and_folders
        self.unique_mp3_folders = []
        self.selected_id3_fields = selected_id3_fields # A dictionary that has as key the name of the tag (e.g. TALB) and as value what kind of data that tag contains (e.g. "String").
    
    
    
    def improve_tags(self):
        self._get_unique_mp3_folders()
        
        # Work from folder to folder.
        for i in self.unique_mp3_folders:
            print(i)
            
            df_iteration = None # Cleaning the iteration df at the start of each loop.
            
            df_iteration = self.files_and_folders[(self.files_and_folders.folder == i)]
            
            # Read all tags in folder
            df_iteration = self.read_id3_tags_in_folder(df_iteration = df_iteration)
            
            
            
            # Select and copy specified tag fields.
            df_iteration = self.select_tags(df_iteration=df_iteration)
            df_iteration = self.copy_selected_tags(df_iteration=df_iteration)
            
            
            # Remove encoding information and only keep the text.
            df_iteration = self.remove_string_encoding_information(df_iteration=df_iteration)
            
            
            # Pass tag on to a beautifier function/class.
            df_iteration["beautified_tag"] = df_iteration["unchanged_tag"].copy()
            
            # Beautify strings
            df_iteration = self.beautify_strings(df_iteration=df_iteration)
            
            
            # Remove album artist if same as track artist
            df_iteration = self.check_obsolescence_of_album_artist(df_iteration=df_iteration)
            
            # Beautifying the track number
            df_iteration = self.beautify_track_number(df_iteration=df_iteration) # TODO Add check to only execute this if there is a track number.

            # Beautifying the disc number
            df_iteration = self.beautfiy_disc_number(df_iteration=df_iteration)
            
            
            # TODO Beautify the date.
            
            
            
            # TODO Add part to delete beautified keys which are empty after the beautification!
            
            
            
            # Delete all existing tags from the ID3 object.
            [df_iteration["id3"][i].delete() for i in df_iteration.index]


            df_iteration["id3"] = [self._save_tags_to_single_id3_object(id3=df_iteration["id3"][i], beautified_tag=df_iteration["beautified_tag"][i]) for i in df_iteration.index]
        

            
            # Write beautified tag to file.
            [df_iteration["id3"][i].save(v1 = 0, v2_version = 4) for i in df_iteration.index] # Saving only as id3v2.4 tags.
            
    
    
    def _get_unique_mp3_folders(self):
        """Get list of unique folders with mp3 files in it. This will be a helper for a following loop."""

        self.unique_mp3_folders = self.files_and_folders.folder.unique()
        self.unique_mp3_folders = list(self.unique_mp3_folders).copy()

    
    
    def read_id3_tags_in_folder(self, df_iteration: pd.DataFrame) -> pd.DataFrame: 
        """Read the whole id3 tags for all provided files."""

        id3 = [self._read_id3_tag_from_single_file(i) for i in df_iteration["file"]] # Read all tags.
        
        # Attaching a column with the read tag.
        df_iteration = self._attach_column_to_df_iteration(data_for_series=id3, series_name="id3", df_iteration=df_iteration)
        
        return(df_iteration)

    
    
    def _read_id3_tag_from_single_file(self, filepath): 
        """Read the whole id3 tag for a single file."""
        
        try:
            id3 = ID3(filepath)
        except ID3NoHeaderError:  # If there is no id3 tag in file, return None. # TODO Test this!
            return None

        return(id3) # Returns an ID3 object.
    
    
    
    
    def select_tags(self, df_iteration) -> pd.DataFrame:
        """Select the specified tag fields."""
        
        unchanged_tag = [list(i.keys() & self.selected_id3_fields.keys()) for i in df_iteration["id3"]]
        
        # Attaching a column with the selected tag.
        df_iteration = self._attach_column_to_df_iteration(data_for_series=unchanged_tag, series_name="unchanged_tag", df_iteration=df_iteration)
        
        return(df_iteration)
    
    
    def copy_selected_tags(self, df_iteration: pd.DataFrame) -> pd.DataFrame:
        """Copying/filling the original tag information (but only) for the selected tag fields."""
        
        unchanged_tag = [dict(
            (k, df_iteration["id3"][i].get(k)) for k in df_iteration["unchanged_tag"][i] if k in df_iteration["id3"][i]
            ) for i in df_iteration.index] # Nested list comprehension adaptation of https://stackoverflow.com/questions/6827834/how-to-filter-a-dict-to-contain-only-keys-in-a-given-list.
        
        # Updating the column with the selected tag.
        df_iteration["unchanged_tag"] = unchanged_tag
        
        
        return(df_iteration)
    
    
    def remove_string_encoding_information(self, df_iteration: pd.DataFrame) -> pd.DataFrame:
        """Getting rid of the encoding part and only keeping the "text", so it will later be unifiedly be saved as UTF8 and not e.g. LATIN1. So changing 'TALB(encoding=<Encoding.LATIN1: 0>, text=['Stellaris : Ancient Relics'])' into 'TALB: 'Stellaris : Ancient Relics'). Not touching the rating field ("POPM:no@email") which does not contain a "text" element."""
        
        unchanged_tag = [dict(
            (k, df_iteration["unchanged_tag"][i].get(k).text[0] if k != "POPM:no@email" else df_iteration["unchanged_tag"][i].get(k)) for k in df_iteration["unchanged_tag"][i]
            ) for i in df_iteration.index] # There can be multiple tags attached. The [0] from .text[0] ensures that only the first element is taken. Without it, the text element would also be a list of strings and not a string (yet).
        
        # Updating the column with the selected tag.
        df_iteration["unchanged_tag"] = unchanged_tag
        
        return(df_iteration)
    
    
    @staticmethod
    def beautify_strings(df_iteration: pd.DataFrame) -> pd.DataFrame:
        output = df_iteration
        
        # Beautifying the album and song title.
        output["beautified_tag"] = [
            {k:string_beautification(v) if k in ["TALB", "TIT2"] else v for (k, v) in output["beautified_tag"][i].items()} # Beautifying the album and song title.
            for i in output.index]
        
        # Beautifying the album and song artist.
        output["beautified_tag"] = [
            {k:string_beautification(v, remove_leading_the=True) if k in ["TPE1", "TPE2"] else v for (k, v) in output["beautified_tag"][i].items()} # Beautifying the album and song title.
            for i in output.index]
    
        return(output)
    
    
    
    @staticmethod
    def check_obsolescence_of_album_artist(df_iteration: pd.DataFrame) -> pd.DataFrame:
        """Remove album artist if same as track artist."""
        output = df_iteration
        
        track_artist = [output["beautified_tag"][i].get("TPE1") for i in output.index]
        album_artist = [output["beautified_tag"][i].get("TPE2") for i in output.index]
        
        if track_artist == album_artist:
            [output["beautified_tag"][i].pop("TPE2", None) for i in output.index] # Remove the tag.
        
        return(output)
    
    
    
    @staticmethod
    def beautify_track_number(df_iteration: pd.DataFrame) -> pd.DataFrame:
        """Beautifying the track number by adding/correcting leading zeros."""
        
        # Be aware that there are cases, where the first track number from cd 2 is not a 1 but continues the counting from disc 1.
        
        
        output = df_iteration
        
        # Helper for number of tracks.
        
        helper_length_max = [
            int(
                re.sub("(?<=\d)\/\d+", "", output["beautified_tag"][i].get("TRCK")) # re.sub part: "01/16" will be transformed into "01". This will then be transformed into an integer.
                ) for i in output.index
            ]
        
        helper_length_max = max(helper_length_max) # Checking for the highest track number. Works also if multiple discs are present in the same folder.
        helper_length_max = len(str(helper_length_max)) # Converting into the number if digits.
        
        
        # TODO Deal with the case where no album name is present. Then do not do anything with the track numbers but keep them as they are. E.g. passing None as helper_length_max into the function already takes care of that.
        
        output["beautified_tag"] = [
            {k:track_number_beautification(v, helper_length_max=helper_length_max, minimum_length=2) if k in ["TRCK"] else v for (k, v) in output["beautified_tag"][i].items()} # Beautifying the track number.
            for i in output.index]
        
        return(output)
    
    
    @staticmethod
    def beautfiy_disc_number(df_iteration: pd.DataFrame) -> pd.DataFrame:
        """Beautifying the disc number by removing it, when it is disc number = 1 unless a) there are multiple disc numbers in the same folder OR b) the file path has "CD 1" (or similar) in it. In these two cases, keep it. If disc number > 1, also keep it."""
        # TODO Nice to have expansion: Delete leading zeros from the disc number.
        
        output = df_iteration
        
        # Check for different disc numbers in same folder.
        helper_different_disc_number = [output["beautified_tag"][i].get("TPOS") for i in output.index]
        
        helper_different_disc_number = list(set(helper_different_disc_number))

        if helper_different_disc_number is None: # There is no disc number tag.
            pass
        
        elif len(helper_different_disc_number) > 1: # There are multiple disc numbers in the same folder.
            pass
        
        elif len(helper_different_disc_number) == 1 and helper_different_disc_number[0] != "1": # There is only one disc number and that is not disc number 1.
            pass
        
        elif len(helper_different_disc_number) == 1 and helper_different_disc_number[0] == "1": # There is only one disc number and that is disc number 1.
            
            helper_folder_contains_cd_string = str(output["folder"][0])
            
            helper_folder_contains_cd_string = bool(re.search("(^| |-|\()cd( \d|-\d|\d)", helper_folder_contains_cd_string, flags=re.IGNORECASE)) # Look for the string " cd" in the folder name. Could also look in the file name instead, but went for folder to have a folder-wide handling. # TODO Expand this to handle the case of "2CD"
            
            if helper_folder_contains_cd_string == True: # If there is a " cd" string in the folder name, don't change anything.
                pass
            
            
            if helper_folder_contains_cd_string == False: # If there is no a " cd" string in the folder name, remove the disc number.
                [output["beautified_tag"][i].pop("TPOS", None) for i in output.index] # Remove the tag.
            
        
        return(output)
        

    
    
    
    
    
    def _save_tags_to_single_id3_object(self, id3, beautified_tag):
        """Save beautified tags to id3 object. This function takes only on row from df_iteration at a time."""

        for key, value in beautified_tag.items():

            if key == "POPM:no@email": # Does not have a text field and thus a bit different structure.
                exec(f'id3.add({value})') # Executes the following string as Python command. The f in the beginning marks this as "f string". See https://www.python.org/dev/peps/pep-0498/

            elif key in ("TALB", "TDRC", "TIT2", "TPE1", "TPE2", "TPOS", "TRCK"): # These fields (all but rating), have a text parameter which can be added the same way.
                exec(f'id3.add({key}(encoding = 3, text = "{value}"))') # encoding = 3 = UTF8

            else:
                # This else condition should not be reached. It is used to raise an alert, when new tag types are entered in the global variables but not yet defined here. That's a bit safer than just distinguishing between == "Rating" and != "Rating".
                # TODO Code this.
                continue
        
        return(id3)
    
    
    @staticmethod
    def _attach_column_to_df_iteration(data_for_series, series_name: str, df_iteration: pd.DataFrame) -> pd.DataFrame:
        """Helper function for adding an object (e.g. list, series, ...) as column to a pd.DataFrame."""
        
        # TODO This function is really not that good as it would not overwrite existing columns with the same name. Maybe go back to good old 'df_iteration["selected_tag"] = selected_tag'?
        
        series = pd.Series(data_for_series, name=series_name)
        
        df_iteration = df_iteration.reset_index(drop=True) # Required to match the following concat correctly.
        df_iteration = pd.concat([df_iteration, series], axis=1, sort=False) # Used this instead of files.loc[:, "x"] = x to prevent SettingWithCopyWarning from happening.
        
        return(df_iteration)