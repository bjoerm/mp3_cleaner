from beautify_single_string import StringBeautifier, StringHelper
from beautify_single_number import NumberBeautifier
from beautify_single_date import DateBeautifier

import pandas as pd


class TagBeautifier:
    """
    This utility class bundles id3 tag beautification methods. This class takes lists of the respective items (e.g. a list of track numbers). It then passes those to other classes that beautify single strings (e.g. one single track number).
    """

    @classmethod
    def beautify_tags(cls, tags: pd.Series, path: str) -> pd.Series:
        """
        This is the main function that is called for beautifying id3 tags. It takes the id3 tags from a folder (as a pd.Series) and beautifies them. The path is used to look for additional information, like about the possible disc number. The method returns a pd.Series again.
        """

        untouched_tag = tags.copy()

        tags = tags.to_list()  # The following methods use list comprehensions which would have converted the pd.Series into a list anyway. But this step makes that more transparant.

        tags = cls._beautify_strings(tags=tags)
        tags = cls._check_obsolescence_of_album_artist(tags=tags)
        tags = cls._check_feat_in_artist(tags=tags)
        tags = cls._beautify_track_number(tags=tags)
        tags = cls._beautify_disc_number(tags=tags, path=path)
        tags = cls._beautify_date(tags=tags)

        tags = pd.Series(tags)  # Converting back into a pd.Series.

        assert len(tags) == len(untouched_tag), "Test for not loosing tags while beautifying."

        return tags

    @staticmethod
    def _beautify_strings(tags: list) -> list:
        """
        Beautify strings. E.g. album and song titles as well as artist name.
        """

        output = tags

        # Beautifying the album and song title.
        output = [
            {k: StringBeautifier.beautify_string(v) if k in ["TALB", "TIT2"] else v for (k, v) in output[i].items()}  # Beautifying the album and song title.
            for i in range(len(output))
            ]

        # Beautifying the artist. Here is any leading "The" is cut.
        output = [
            {k: StringBeautifier.beautify_string(v, remove_leading_the=True) if k in ["TPE1", "TPE2"] else v for (k, v) in output[i].items()}
            for i in range(len(output))
            ]

        return output

    @staticmethod
    def _check_obsolescence_of_album_artist(tags: list) -> list:
        """
        Remove album artist if it is the same as track artist.
        """

        output = tags

        track_artist = [output[i].get("TPE1") for i in range(len(output))]  # This is a list with an entry for each file/tag.
        album_artist = [output[i].get("TPE2") for i in range(len(output))]

        # Remove the album artist when it is identical with track artist.
        if track_artist == album_artist:
            [output[i].pop("TPE2", None) for i in range(len(output))]  # Remove the TPE2 tag.

        # Move album artist to track artist, if track artist is not available.
        if all(x is not None for x in album_artist) and all(x is None for x in track_artist):
            # Copy tag from TPE2 to TPE1
            output = [
                {k: output[i].get("TPE2") if k in ["TPE1"] else v for (k, v) in output[i].items()}
                for i in range(len(output))]

            [output[i].pop("TPE2", None) for i in range(len(output))]  # Remove the TPE2 tag.

        return output

    @staticmethod
    def _check_feat_in_artist(tags: list) -> list:
        """
        Deal with the case of featuring information being in the track artist field by moving them from the track artist to the track name.
        """

        output = tags

        for i in output:
            if "TPE1" in i and "TIT2" in i:  # Only execute the following, if these two tags exists.
                has_feat_in_tpe1, tpe1_updated, tit2_updated = StringHelper.move_feature_from_artist_to_track(tpe1=i["TPE1"], tit2=i["TIT2"])  # TODO ADJUST!!!! ONLY TEMP WIP!!!!

                if has_feat_in_tpe1 is True:
                    # Update the track artist and title tag
                    i["TPE1"] = tpe1_updated
                    i["TIT2"] = tit2_updated

        return output

    @staticmethod
    def _beautify_track_number(tags: list) -> list:
        """
        Beautifying the track number by removing non-integers as well as adding/correcting leading zeros. The helper_lenght_max checks for the digits of the highest observed track number in the folder.
        """

        output = tags

        # Helper for number of tracks.
        # Transforming "01/16" or "01/" into "01". This will then be transformed into an integer. # TODO Move this as part with the max into a method in track_number_beautification.
        helper_length_max = [
            NumberBeautifier.extract_number_from_slash_format(output[i].get("TRCK")) for i in range(len(output))
            ]

        helper_length_max = list(filter(None.__ne__, helper_length_max))  # Removing all None values. From: https://www.kite.com/python/answers/how-to-remove-none-from-a-list-in-python

        # Edge case of all values being None values.
        if len(helper_length_max) == 0:
            return output  # End method. Don't do any beautification.

        helper_length_max = max(helper_length_max)  # Checking for the highest track number. Works also if multiple discs are present in the same folder.
        helper_length_max = len(str(helper_length_max))  # Converting into the number if digits.

        output = [
            {k: NumberBeautifier.beautify_track_number(v, helper_length_max=helper_length_max, minimum_length=2) if k in ["TRCK"] else v for (k, v) in output[i].items()}  # Beautifying the track number.
            for i in range(len(output))
            ]

        return output

    @staticmethod
    def _beautify_disc_number(tags: list, path: str = None) -> list:
        """
        Beautifying the disc number by removing it, when it is disc number = 1 unless a) there are tags showing multiple disc numbers in the same folder OR b) the file path has "CD 1" (or similar) in it. In these two cases, keep it. If disc number > 1, also keep it.
        """
        # TODO Nice to have expansion: Delete leading zeros from the disc number. Or always have two digit long cd number.
        # TODO Refactor split this into multiple smaller methods.

        output = tags

        # Check for different disc numbers in same folder.
        helper_different_disc_number = set(output[i].get("TPOS") for i in range(len(output)))  # Set comprehension to remove duplciates.
        helper_different_disc_number = list(helper_different_disc_number)

        # Keeping or removing the disc number tag.
        if helper_different_disc_number is None or helper_different_disc_number == [None]:  # There is no disc number tag.
            pass

        elif len(helper_different_disc_number) > 1:  # There are multiple different disc numbers in the same folder.
            pass

        elif len(helper_different_disc_number) == 1 and helper_different_disc_number[0] == "1/1":  # If there is only one disc number and that is disc number 1/1, remove the disc number tag.
            [output[i].pop("TPOS", None) for i in range(len(output))]

        elif len(helper_different_disc_number) == 1 and helper_different_disc_number[0] != "1":  # If there is only one disc number and that is not disc number 1, leave it.
            pass

        elif len(helper_different_disc_number) == 1 and helper_different_disc_number[0] == "1":  # If there is only one disc number and that is disc number 1, leave it.

            helper_folder_contains_cd_string = NumberBeautifier.has_cd_string_in_folder_name(path)

            if helper_folder_contains_cd_string is True:  # If there is a " cd" string in the folder name, don't remove the disc number tag.
                pass

            if helper_folder_contains_cd_string is False:  # If there is not a " cd" string in the folder name, remove the disc number tag.
                [output[i].pop("TPOS", None) for i in range(len(output))]

        is_each_track_with_number = [output[i].get("TPOS") for i in range(len(output))]

        # Convert any slash format in the disc number. E.g. 1/2 becomes 1.
        if any(x is None for x in is_each_track_with_number):
            # Is there any None value in the disc numbers.
            return output

        else:  # Maybe only call this if there is actually a slash in the number.
            [
                output[i].update(
                    {"TPOS": NumberBeautifier.extract_number_from_slash_format(output[i].get("TPOS"))}
                )
                for i in range(len(output))
            ]

        return output

    @staticmethod
    def _beautify_date(tags: list) -> list:
        """
        Shorten any YYYY-MM-DD values into YYYY.
        """

        output = tags

        output = [
            {k: DateBeautifier.extract_year(v) if k in ["TDRC"] else v for (k, v) in output[i].items()}  # Shorten to YYYY.
            for i in range(len(output))]

        return output
