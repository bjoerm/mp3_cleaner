import re

def track_number_beautification(track_number: str, helper_length_max: int, minimum_length: int = 2) -> str:
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
