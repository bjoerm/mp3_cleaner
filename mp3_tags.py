import glob  # For reading files and folders.
from mutagen.id3 import ID3, ID3NoHeaderError, POPM, TALB, TDRC, TIT2, TPE1, TPE2, TPOS, TRCK
import pandas as pd

class Mp3Tags:
    
    # This class should be getting the unique_folder list from the Environment class as input.
    
    def __init__(self, files_and_folders):
        self.files_and_folders = files_and_folders
        self.unique_mp3_folders = []
    
    
    def improve_tags(self):
        self._get_unique_mp3_folders()
        
        # Work from folder to folder.
        for i in self.unique_mp3_folders:
            
            df_iteration = None # Cleaning the iteration df at the start of each loop.
            
            df_iteration = self.files_and_folders[(self.files_and_folders.folder == i)]
            
            # Debug
            print("\n" + str(i))
            print(df_iteration["file"])
            
            df_iteration = self._read_id3_tags(files = df_iteration)
            
            pass
            
    
    
    def _get_unique_mp3_folders(self):
        """ Get list of unique folders with mp3 files in it. This will be a helper for a following loop."""

        self.unique_mp3_folders = self.files_and_folders.folder.unique()
        self.unique_mp3_folders = list(self.unique_mp3_folders).copy()

    
    
    def _read_id3_tags(self, files): 
        """Read the whole id3 tags for all provided files."""

        
        whole_read_id3_tags = [self._read_single_id3_tag(i) for i in files["file"]] # files.loc[:, "file"] / files["file"]
        whole_read_id3_tags = pd.Series(whole_read_id3_tags, name="whole_read_id3_tag")
        
        files = files.reset_index(drop=True) # Required to match the following concat correctly.
        files = pd.concat([files, whole_read_id3_tags], axis=1, sort=False) # Used this instead of files.loc[:, "x"] = x to prevent SettingWithCopyWarning from happening.
        
        
        print(files)
        
        
        return(files)

    
    
    def _read_single_id3_tag(self, filepath): 
        """Read the whole id3 tag for a single file."""
        
        try:
            id3 = ID3(filepath) # TODO Add file as input!
        except ID3NoHeaderError:  # If there is no id3 tag in file, give nothing back.
            return None

        return(id3) # Returns an ID3 object.