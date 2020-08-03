import glob  # For reading files and folders.
from mutagen.id3 import ID3, ID3NoHeaderError, POPM, TALB, TDRC, TIT2, TPE1, TPE2, TPOS, TRCK
import pandas as pd

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
            
            df_iteration = None # Cleaning the iteration df at the start of each loop.
            
            df_iteration = self.files_and_folders[(self.files_and_folders.folder == i)]
            
            # Read all tags in folder
            df_iteration = self.read_id3_tags_in_folder(df_iteration = df_iteration)
            
            
            # Select only specified tag fields.
            df_iteration = self.select_tags(df_iteration=df_iteration)
            df_iteration = self.fill_selected_tags(df_iteration=df_iteration)
            

            
            # TODO Next step is to have a loop/list comprehension that goes through each row's tags and compares with self.selected_id3_fields to pass it to different methods. E.g. a string method, a Date number method, ...
            
            
            pass
            
    
    
    def _get_unique_mp3_folders(self):
        """Get list of unique folders with mp3 files in it. This will be a helper for a following loop."""

        self.unique_mp3_folders = self.files_and_folders.folder.unique()
        self.unique_mp3_folders = list(self.unique_mp3_folders).copy()

    
    
    def read_id3_tags_in_folder(self, df_iteration: pd.DataFrame) -> pd.DataFrame: 
        """Read the whole id3 tags for all provided files."""

        untouched_tag = [self._read_id3_tag_from_single_file(i) for i in df_iteration["file"]] # Read all tags.
        
        # Attaching a column with the read tag.
        df_iteration = self._attach_column_to_df_iteration(data_for_series=untouched_tag, series_name="untouched_tag", df_iteration=df_iteration)
        
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
        
        selected_tag = [list(i.keys() & self.selected_id3_fields.keys()) for i in df_iteration["untouched_tag"]]
        
        # Attaching a column with the selected tag.
        df_iteration = self._attach_column_to_df_iteration(data_for_series=selected_tag, series_name="selected_tag", df_iteration=df_iteration)
        
        return(df_iteration)
    
    
    def fill_selected_tags(self, df_iteration) -> pd.DataFrame:
        """Copying/filling the original tag information (but only) for the selected tag fields."""
        
        df_iteration["selected_tag"] = [dict.fromkeys(i, None) for i in df_iteration.selected_tag] # Converting list to dict (with empty values).
        
        [df_iteration["selected_tag"][i].update(df_iteration["untouched_tag"][i]) for i in df_iteration.index] # Filling the selected tags with the untouched values. At this stage, this column contains the untouched, original tags - but only for the selected tag fields.
        
        return(df_iteration)
    
    
    
    
    @staticmethod
    def _attach_column_to_df_iteration(data_for_series, series_name: str, df_iteration: pd.DataFrame) -> pd.DataFrame:
        """Helper function for adding an object (e.g. list, series, ...) as column to a pd.DataFrame."""
        
        series = pd.Series(data_for_series, name=series_name)
        
        df_iteration = df_iteration.reset_index(drop=True) # Required to match the following concat correctly.
        df_iteration = pd.concat([df_iteration, series], axis=1, sort=False) # Used this instead of files.loc[:, "x"] = x to prevent SettingWithCopyWarning from happening.
        
        return(df_iteration)