import re


class beautify_disc_and_track_number:
    """
    This utility class bundles id3 tag beautification methods for disc number and track number.
    """
    
    @staticmethod
    def beautify_track_number(track_number: str, helper_length_max: int, minimum_length: int = 2) -> str:
        """
        Beautifying the track numbers.
        minimum_length sets the minimum integer length of the track number 2 means that an album with only 5 tracks, will still have all track number being filled with a leading zero, so that e.g. track number "4" becomes "04".
        helper_length_max will be used to fill leading zeros in the track number.
        """
        
        track_number_beautified = str(track_number) # Ensuring that the input is a string.
        
        # Extract track number from format track number/tracks on disc (e.g.: "01/16" for track 1 from 16 of this disc)).
        track_number_beautified = re.sub("(?<=\d)\/\d+", "", track_number_beautified) # "01/16" will be transformed into "01"
        
        
        # Add leading zero (if required)
        helper_length_current_track = len(track_number_beautified)
        
        ## Zeros to add
        zeros_to_add = max(helper_length_max, minimum_length) - helper_length_current_track # The first part with the max ensures the minimum length.
        
        if (track_number_beautified == "" or helper_length_max is None) : # Case: Empty track number (after beautification. It might have been filled before) or no info on the length max.
            pass 
        elif zeros_to_add == 0: # Case: Correct number of leading zeros.
            pass
        elif zeros_to_add > 0:
            track_number_beautified = "0" * zeros_to_add + track_number_beautified # Add missing zeros to track number.
        # TODO Add case to remove too many leading zeros!
        
        return(track_number_beautified)


    @staticmethod
    def extract_track_number_from_slash_format(string: str) -> str:
        """
        Replace any slash (and if there integers) after an initial interger.
        For dealing with cases like "01/16" or "1/" for the track number.
        """
        
        output = string
        
        if output is not None: # Dealing with the special of None - which is not converted into a string.
            output = str(output)
        
        
        try:
            output = re.sub("(?<=\d)\/\d*", "", output)
        except:
            pass # If for example None is entered, return None untouched.
        
        return(output)


    @staticmethod
    def has_cd_string_in_folder_name(string: str) -> bool:
        """
        Look for the strings related to the number of discs. E.g. " cd" or "2cd" in the folder name. Could have also looked in the file name instead, but went for folder to have a folder-wide unique handling.
        """
        
        output = bool(re.search("(^|\W|_)cd(\d{1,2}|\W{1,2}\d{1,2})([^a-zA-Z0-9]|$)|(^|\W|_)(\d{1,2}|\d{1,2}\W{1,2})cd([^a-zA-Z0-9]|$)", str(string), flags=re.IGNORECASE)) # Rather complex regex... Thus, put this into a separate function, so it is easier to include in unittests.
        
        return(output)




