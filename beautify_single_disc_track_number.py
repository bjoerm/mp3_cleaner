import re


class DiscTrackBeautifier:
    """
    This utility class bundles id3 tag beautification methods for disc number and track number. This class beautifies a single string at a time.
    """

    @classmethod
    def beautify_track_number(cls, track_number: str, helper_length_max: int, minimum_length: int = 2) -> str:
        """
        Beautifying the track numbers.
        minimum_length sets the minimum integer length of the track number 2 means that an album with only 5 tracks, will still have all track number being filled with a leading zero, so that e.g. track number "5" becomes "05" on that album.
        helper_length_max refers to the highest observed track number in that album and will be used to fill leading zeros in the track number.
        """

        if track_number is None:
            return track_number

        track_number_beautified = str(track_number)  # Ensuring that the input is a string.

        # Extract track number from format track number/tracks on disc (e.g.: "01/16" for track 1 from 16 of this disc)).
        track_number_beautified = cls.extract_number_from_slash_format(track_number_beautified)  # "01/16" will be transformed into "01"

        # Remove non-integers
        track_number_beautified = re.sub(r"[^0-9]", "", track_number_beautified)

        # Add leading zero (if required)
        helper_length_current_track = len(track_number_beautified)

        # Helper: Zeros to add
        zeros_to_add = max(helper_length_max, minimum_length) - helper_length_current_track  # The first part with the max ensures the minimum length.

        if (track_number_beautified == "" or helper_length_max is None):  # Case: Empty track number (after beautification. It might have been filled before) or no info on the length max.
            pass

        elif zeros_to_add == 0:  # Case: Correct number of leading zeros.
            pass

        elif zeros_to_add > 0:  # Case: Filling up missing zeros.
            track_number_beautified = "0" * zeros_to_add + track_number_beautified

        elif zeros_to_add < 0:  # Case: Removing not needed zeros.

            # Double check that each of the leading characters is indeed a zero.
            for i in range(abs(zeros_to_add)):
                if track_number_beautified[i] == "0":
                    pass

                else:
                    return track_number_beautified

            track_number_beautified = track_number_beautified[abs(zeros_to_add):]

        return track_number_beautified

    @staticmethod
    def extract_number_from_slash_format(string: str) -> str:
        """
        Replace any slash (and if there integers) after an initial interger.
        For dealing with cases like "01/16" or "1/" for the track number.
        """

        output = string

        if output is None:
            return None

        else:
            output = str(output)
            output = re.sub(r"(?<=\d)\/\d*", "", output)

        return output

    @staticmethod
    def has_cd_string_in_folder_name(string: str) -> bool:
        """
        Look for the strings related to the number of discs. E.g. " cd" or "2cd" in the folder name. Could have also looked in the file name instead, but went for folder to have a folder-wide unique handling.
        """

        output = bool(re.search(r"(^|\W|_)cd(\d{1,2}|\W{1,2}\d{1,2})([^a-zA-Z\u0080-\uFFFF0-9]|$)|(^|\W|_)(\d{1,2}|\d{1,2}\W{1,2})cd([^a-zA-Z\u0080-\uFFFF0-9]|$)", str(string), flags=re.IGNORECASE))  # Rather complex regex... Thus, this was put into a separate method, so it is easier to include in unittests.

        return output
