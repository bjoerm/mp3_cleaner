from mutagen.id3 import ID3, ID3NoHeaderError, POPM, TALB, TDRC, TIT2, TPE1, TPE2, TPOS, TRCK
import pandas as pd
from beautify_tags import TagBeautifier


class ProcessMp3:
    """
    This class gets the folder list from the Environment class as input. It then goes iteratively through each folder, reads the tags from all MP3 files in that folder, beautifies the tags from these files and overwrites them afterwards.
    """
    
    
    def __init__(self, selected_id3_fields, files_and_folders):
        self.files_and_folders = files_and_folders
        self.unique_mp3_folders = []
        self.selected_id3_fields = selected_id3_fields # A dictionary that has as key the name of the tag (e.g. TALB) and as value what kind of data that tag contains (e.g. "String").
    
    
    
    def improve_tags(self):
        self._get_unique_mp3_folders()
        
        # Work from folder to folder.
        for i in self.unique_mp3_folders:
            print("Processing: " + str(i))
            
            df_iteration = None # Cleaning the iteration df at the start of each loop.
            
            df_iteration = self.files_and_folders[(self.files_and_folders.folder == i)]
            
            # Read all tags in folder
            df_iteration = self.read_id3_tags_in_folder(df_iteration = df_iteration)
            
            
            # Select and copy specified tag fields.
            df_iteration = self.select_tags(df_iteration=df_iteration)
            df_iteration = self.copy_selected_tags(df_iteration=df_iteration)
            
            
            # Remove encoding information and only keep the text.
            df_iteration = self.remove_string_encoding_information(tags=df_iteration["unchanged_tag"].copy())
            
            
            # Pass tag on to the beautifier utility class.
            df_iteration["beautified_tag"] = TagBeautifier.beautify_tags(tags=df_iteration["unchanged_tag"].copy(), path = str(i)) # str(i) refers to the currently processed folder.
            
            
            # Delete all existing tags from the ID3 object.
            [df_iteration["id3"][i].delete() for i in df_iteration.index]


            df_iteration["id3"] = [self._save_tags_to_single_id3_object(id3=df_iteration["id3"][i], beautified_tag=df_iteration["beautified_tag"][i]) for i in df_iteration.index]

            
            # Write beautified tag to file.
            [df_iteration["id3"][i].save(v1 = 0, v2_version = 4) for i in df_iteration.index] # Saving only as id3v2.4 tags and not as id3v1 at all.
    
    
    def _get_unique_mp3_folders(self):
        """
        Get list of unique folders with mp3 files in it. This will be a helper for a following loop.
        """

        self.unique_mp3_folders = self.files_and_folders.folder.unique()
        self.unique_mp3_folders = list(self.unique_mp3_folders).copy()

    
    
    def read_id3_tags_in_folder(self, df_iteration: pd.DataFrame) -> pd.DataFrame: 
        """
        Read the whole id3 tags for all provided files.
        """

        id3 = [self._read_id3_tag_from_single_file(i) for i in df_iteration["file"]] # Read all tags.
        
        # Attaching a column with the read tag.
        df_iteration = self._attach_column_to_df_iteration(data_for_series=id3, series_name="id3", df_iteration=df_iteration)
        
        return(df_iteration)

    
    
    def _read_id3_tag_from_single_file(self, filepath): 
        """
        Read the whole id3 tag for a single file.
        """
        
        try:
            id3 = ID3(filepath)
        except ID3NoHeaderError:  # If there is no id3 tag in file, return None. # TODO Test this!
            return None

        return(id3) # Returns an ID3 object.
    
    
    
    
    def select_tags(self, df_iteration) -> pd.DataFrame:
        """
        Select the specified tag fields.
        """
        
        unchanged_tag = [list(i.keys() & self.selected_id3_fields.keys()) for i in df_iteration["id3"]]
        
        # Attaching a column with the selected tag.
        df_iteration = self._attach_column_to_df_iteration(data_for_series=unchanged_tag, series_name="unchanged_tag", df_iteration=df_iteration)
        
        return(df_iteration)
    
    
    def copy_selected_tags(self, df_iteration: pd.DataFrame) -> pd.DataFrame:
        """
        Copying/filling the original tag information (but only) for the selected tag fields.
        """
        
        unchanged_tag = [dict(
            (k, df_iteration["id3"][i].get(k)) for k in df_iteration["unchanged_tag"][i] if k in df_iteration["id3"][i]
            ) for i in df_iteration.index] # Nested list comprehension adaptation of https://stackoverflow.com/questions/6827834/how-to-filter-a-dict-to-contain-only-keys-in-a-given-list.
        
        # Updating the column with the selected tag.
        df_iteration["unchanged_tag"] = unchanged_tag
        
        
        return(df_iteration)
    
    
    
    @staticmethod
    def remove_string_encoding_information(tags: pd.Series) -> pd.Series:
        """
        Getting rid of the encoding part and only keeping the "text", so it will later be unifiedly be saved as UTF8 and not e.g. LATIN1. So changing 'TALB(encoding=<Encoding.LATIN1: 0>, text=['Stellaris : Ancient Relics'])' into a simple dictionary 'TALB: 'Stellaris : Ancient Relics'). 
        """
        output = tags.copy()
        
        output = [
            dict(
                    (
                        k
                        , output[i].get(k).text[0] if k != "POPM:no@email" # Not touching the rating field ("POPM:no@email") which does not contain a "text" element.
                        else output[i].get(k)
                    ) for k in output[i]
                ) for i in range(len(output))
            ]
        
        output = pd.Series(output) # Converting back into a pd.Series.
        
        assert len(output) == len(tags), "Test for not loosing tags."
        
        return(output)

    
    
    def _save_tags_to_single_id3_object(self, id3, beautified_tag):
        """
        Save beautified tags to id3 object. This function takes only on row from df_iteration at a time.
        """

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
        """
        Helper function for adding an object (e.g. list, series, ...) as column to a pd.DataFrame.
        """
        
        # TODO This function is really not that good as it would not overwrite existing columns with the same name. Maybe go back to good old 'df_iteration["selected_tag"] = selected_tag'?
        
        series = pd.Series(data_for_series, name=series_name)
        
        df_iteration = df_iteration.reset_index(drop=True) # Required to match the following concat correctly.
        df_iteration = pd.concat([df_iteration, series], axis=1, sort=False) # Used this instead of files.loc[:, "x"] = x to prevent SettingWithCopyWarning from happening.
        
        return(df_iteration)
