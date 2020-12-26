from mutagen.id3 import ID3, ID3NoHeaderError, POPM, TALB, TDRC, TIT2, TPE1, TPE2, TPOS, TRCK
import pandas as pd
from beautify_tags import TagBeautifier


class TagManager:
    """
    This class gets the folder list from the Environment class as input. It then goes iteratively through each folder, reads the tags from all MP3 files in that folder, beautifies the tags from these files and overwrites them afterwards.
    """


    @classmethod
    def improve_tags(cls, selected_id3_fields: list, files_and_folders: pd.DataFrame):
        unique_mp3_folders = cls._get_unique_mp3_folders(files_and_folders=files_and_folders)
        
        # Work from folder to folder.
        for i in unique_mp3_folders:
            print("Processing: " + str(i))
            
            df_iteration = None # Cleaning the iteration df at the start of each loop.
            
            df_iteration = cls._select_current_folder(files_and_folders=files_and_folders, current_unique_folder=i)

            
            # Read all tags in folder
            df_iteration = cls._read_id3_tags_in_folder(df_iteration=df_iteration)
            
            
            # Keep only selected tags
            df_iteration = cls._keep_only_selected_tags(df_iteration=df_iteration, selected_id3_fields=selected_id3_fields)
            
            
            # Remove encoding information and only keep the text.
            df_iteration["unchanged_tag"] = cls._remove_string_encoding_information(tags=df_iteration["unchanged_tag"])
            
            
            # Pass tag on to the beautifier utility class.
            df_iteration["beautified_tag"] = TagBeautifier.beautify_tags(tags=df_iteration["unchanged_tag"].copy(), path = str(i)) # str(i) refers to the currently processed folder.
            
            
            # Delete all existing tags from the ID3 object.
            [df_iteration["id3"][i].delete() for i in df_iteration.index]

            # Create new ID3 object from beautified tag.
            df_iteration["id3"] = [cls._save_tags_to_single_id3_object(id3=df_iteration["id3"][i], beautified_tag=df_iteration["beautified_tag"][i]) for i in df_iteration.index]

            
            # Write beautified tag to file.
            [df_iteration["id3"][i].save(v1 = 0, v2_version = 4) for i in df_iteration.index] # Saving only as id3v2.4 tags and not as id3v1 at all.
    
    
    
    @staticmethod
    def _get_unique_mp3_folders(files_and_folders: list) -> list:
        """
        Get list of unique folders with mp3 files in it. This will be a helper for a following loop.
        """

        unique_mp3_folders = files_and_folders.copy()
        unique_mp3_folders = unique_mp3_folders.folder.unique()
        unique_mp3_folders = list(unique_mp3_folders)
        
        return(unique_mp3_folders)


    @staticmethod
    def _select_current_folder(files_and_folders: pd.DataFrame, current_unique_folder) -> pd.DataFrame:
        """
        Selecting the files in the i'th unique folder.
        """
        
        df_iteration = files_and_folders[(files_and_folders.folder == current_unique_folder)].copy() # The .copy() is required to have a real copy and not just a view of the list.
        
        df_iteration = df_iteration.reset_index(drop=True)
        
        return(df_iteration)


    
    @classmethod
    def _read_id3_tags_in_folder(cls, df_iteration: pd.DataFrame) -> pd.DataFrame: # TODO Could get rid of the cls, once _attach_column_to_df_iteration is removed/replaced.
        """
        Read the whole id3 tags for all provided files.
        """

        df_iteration["id3"] = [cls._read_id3_tag_from_single_file(i) for i in df_iteration["file"]] # Read all tags.
        
        return(df_iteration)

    
    @staticmethod
    def _read_id3_tag_from_single_file(filepath): 
        """
        Read the whole id3 tag for a single file.
        """
        
        try:
            id3 = ID3(filepath)
        except ID3NoHeaderError:  # If there is no id3 tag in file, return None. # TODO Test this!
            return None

        return(id3) # Returns an ID3 object.


    
    @staticmethod
    def _keep_only_selected_tags(df_iteration: pd.DataFrame, selected_id3_fields: list) -> pd.DataFrame:
        """
        Creating a copy of the original tag information (but only) for the selected tag fields.
        """
        
        # TODO This should be refactored to have only the id3 column (pd.Series), where every entry is a dictionary per file, as input and return an pd.Series of the same shape.
        
        unchanged_tag = [
            {
                k:v for (k, v) in df_iteration["id3"][i].items() if k in selected_id3_fields
            } # Selecting only the tags that are specified in selected_id3_fields
            for i in df_iteration.index
            ]
        
        df_iteration["unchanged_tag"] = unchanged_tag
        
        return(df_iteration)
    
    
    
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
                        , output[i].get(k).text[0] if k != "POPM:no@email" # Not touching the rating field ("POPM:no@email") which does not contain a "text" element.
                        else output[i].get(k)
                    ) for k in output[i]
                ) for i in range(len(output))
            ]
        
        output = pd.Series(output) # Converting back into a pd.Series.
        
        assert len(output) == len(tags), "Test for not loosing tags."
        
        return(output)

    
    @staticmethod
    def _save_tags_to_single_id3_object(id3, beautified_tag):
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
