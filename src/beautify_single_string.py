import random
import string
from typing import Optional

import regex


class StringBeautifier:
    """
    This utility class bundles id3 tag beautification methods for strings. This class beautifies a single string at a time.
    """

    @classmethod
    def beautify_string(cls, text: Optional[str], remove_leading_the: bool = False) -> str:
        """
        This method beautifies strings. It removes not needed whitespaces, deals with special characters and some other things. It also capitalizes the string to appear more uniform.
        """

        if text is None:  # Edge case of input being None.
            return None

        text_beautified = str(text)  # Creating a copy of the input which is used, so the original input is kept for comparisons. And ensuring that the text is a string.

        # Beautify the string
        text_beautified = cls._remove_not_needed_whitespaces(text=text_beautified)
        text_beautified = cls._unify_quotation_marks_and_accents(text=text_beautified)
        text_beautified = cls._beautify_colons(text=text_beautified)
        text_beautified = cls._enforce_round_brackets(text=text_beautified)
        text_beautified = cls._unify_hyphens(text=text_beautified)
        text_beautified = cls._replace_special_characters(text=text_beautified)
        text_beautified = cls._fill_missing_space_after_comma(text=text_beautified)
        text_beautified = cls._remove_leading_the(remove_leading_the=remove_leading_the, text=text_beautified)  # Will only remove if the input variable remove_leading_the is set to True.
        text_beautified = cls._capitalize_string(text=text_beautified)
        text_beautified = cls._deal_with_special_words_and_bands(text=text_beautified)
        text_beautified = cls._remove_not_needed_whitespaces(text=text_beautified)

        return text_beautified

    @staticmethod
    def _remove_not_needed_whitespaces(text: str) -> str:
        """
        Removes any case of unneeded whitespace.
        """

        text = regex.sub(r"\(\s", "(", text)  # Remove any whitespace after an opening bracket.
        text = regex.sub(r"\s\)", ")", text)  # Remove any whitespace before a closing bracket.
        text = regex.sub(r"\s+", " ", text)  # Remove any multiple whitespaces.
        text = text.strip()  # Remove any whitespace at the start and end.

        return text

    @staticmethod
    def _unify_quotation_marks_and_accents(text: str) -> str:
        """
        Convert double (") quotation marks from string into single quotation marks ('). That helps as " is not wanted in filenames. Also converts accents into '.
        """

        # Quotation marks
        text = regex.sub('"', "'", text)
        text = regex.sub("''", "'", text)

        # Accents
        text = regex.sub("`", "'", text)
        text = regex.sub("´", "'", text)

        return text

    @staticmethod
    def _beautify_colons(text: str) -> str:
        """
        Convert colons to dashes. Deal with case "Abc: Abc" and "Abc:Abc" differently.
        """

        # Case of colon followed by whitespace. E.g.: Deus Ex: Human Revolution -> Deus Ex - Human Revolution
        text = regex.sub(r"(?<=[a-zA-Z0-9\u0080-\uFFFF]): (?=.+)", " - ", text)  # \u0080-\uFFFF catches special characters from German and other languages https://stackoverflow.com/questions/36366125/

        # All other cases of a colon.
        text = regex.sub(":", "-", text)

        return text

    @staticmethod
    def _enforce_round_brackets(text: str) -> str:
        """
        Converts curly and square brackets into round brackets.
        """
        text = regex.sub(r"\[+|\{+|⟨+", "(", text)
        text = regex.sub(r"\]+|\}+|⟩+", ")", text)

        return text

    @staticmethod
    def _unify_hyphens(text: str) -> str:
        """
        Convert all types of hyphens into simple "-".
        """

        text = regex.sub(r"\p{Pd}", "-", text)  # Pd matches every unicode character from the 'Punctuation, Dash' category: https://www.fileformat.info/info/unicode/category/Pd/list.htm

        return text

    @staticmethod
    def _replace_special_characters(text: str) -> str:
        """
        Collection of removing special characters.
        """
        # TODO Deal with % and $ - maybe also log those or raise alerts. Or ask for user input as $ might be sometimes be best represented with an S and sometimes with an USD or Dollar.

        # Semicolons
        text = text.replace(";", ",")

        # Slashes
        text = text.replace("\\", "-")
        text = text.replace("/", "-")

        # Question marks
        text = text.replace("?", "")

        return text

    @staticmethod
    def _fill_missing_space_after_comma(text: str) -> str:
        """
        Missing space after comma - as long as it is not followed by digits.
        """

        text = regex.sub(
            r"(?<=[a-zA-Z\u0080-\uFFFF]),(?=[a-zA-Z\u0080-\uFFFF])|(?<=[0-9]),(?=[a-zA-Z\u0080-\uFFFF])|(?<=[a-zA-Z\u0080-\uFFFF]),(?=[0-9])",
            ", ",
            text,
            flags=regex.IGNORECASE,
        )

        return text

    @staticmethod
    def _remove_leading_the(remove_leading_the: bool, text: str) -> str:
        """
        Remove any leading "The " from the string.
        """

        if remove_leading_the is False:
            return text

        if text in ["The", "the"]:  # Edge case where the artist is named only "the".
            return text

        text = regex.sub(r"^(the\s)", "", text, flags=regex.IGNORECASE)

        return text

    @staticmethod
    def _capitalize_string(text: str) -> str:
        """
        Capitalize each word of the string.
        """

        if text == "":
            return text

        # Break the string into pieces at place with a space (into a list).
        text_list = text.split(" ")
        text_list_improved = text_list.copy()

        # For each pieces, run capitalization.
        for i in range(len(text_list)):
            if regex.match(r".*\p{Lu}+.*", text_list[i]):  # Does the string contain a capital letter somewhere? If so, leave it as it is.
                text_list_improved[i] = text_list[i]

            elif regex.match(r"^\d+", text_list[i]):  # Does the string start with an integer (e.g. 1st, 2nd)? If so, leave it as it is. This could be expanded, to look for any intergers, not only at the beginning.
                text_list_improved[i] = text_list[i]

            elif regex.match(r".+['|`|´]\w+", text_list[i]):  # Does the string contains an accent (', ` or ´) before a string? If so, don't transform the part after the accent into uppercase. This needs to be done, after the check above for captial letters.
                text_list_improved[i] = text_list[i].capitalize()  # Capitalizes transforms that's into That's. While title would transform it into That'S.

            elif regex.match(r"^'n'$", text_list[i], flags=regex.IGNORECASE):  # Is the string an 'n' or 'N', so shortform of "and"? Like in Guns 'n' Roses? If so, keep the 'n' lowercase.
                text_list_improved[i] = text_list[i].lower()

            else:  # Convert string to title format.
                text_list_improved[i] = text_list[i].title()

        # Converting the list of strings back into a string.
        separator = " "
        output = separator.join(text_list_improved)  # Converting the list of strings into a string.

        return output

    @staticmethod
    def _deal_with_special_words_and_bands(text: str) -> str:
        """
        Deal with special cases like the strings featuring, pt., remix or live.
        """

        # Unifying special words
        text = regex.sub(
            r"(?<=^)Featuring |(?<=^)Ft. |(?<= |\()Featuring |(?<= |\()Ft. ",
            "Feat. ",
            text,
            flags=regex.IGNORECASE,
        )  # This part of multiple positive lookbehinds is not very elegant but adding ^ (for looking at the start of the string) into the other one, returned an error due to the varying widths of ^ and e.g. " "
        text = regex.sub(r"(?<=^)Pt. |(?<= |\()Pt. ", "Part ", text, flags=regex.IGNORECASE)
        text = regex.sub(
            r"(?<=^)remix(?=\)|$| )|(?<= |\()remix(?=\)|$| )",
            "Remix",
            text,
            flags=regex.IGNORECASE,
        )  # Preventing all capitalized REMIX and other similar forms. Must have space or open bracket at the beginning.
        text = regex.sub(
            r"(?<=^)live(?=\)|$| )|(?<= |\()live(?=\)|$| )",
            "Live",
            text,
            flags=regex.IGNORECASE,
        )  # Preventing all capitalized LIVE and other similar forms. Must have space or open bracket at the beginning.
        text = regex.sub(r"\svs\.\s|\svs\s", " vs. ", text, flags=regex.IGNORECASE)  # Unify vs.

        # Removing unwanted info
        text = regex.sub(r" \(explicit\)", "", text, flags=regex.IGNORECASE)  # Removing any " (Explicit)" information.
        text = regex.sub(r"®", "", text, flags=regex.IGNORECASE)  # Special registered trademark icon.

        # Special band names
        text = regex.sub(
            r"(?<=^)ac-dc(?=\)|$| )|(?<= |\()ac-dc(?=\)|$| )",
            "ACDC",
            text,
            flags=regex.IGNORECASE,
        )  # AC/DC

        return text


# TODO This whole class should be removed once refactoring is done.
class StringHelper:
    """
    This utility class contains helper methods that are not related to the generic string beautification above, but e.g. might also be useful for filename improvements.
    """

    @classmethod
    def move_feature_from_artist_to_track(cls, artist: str, track_name: str) -> list:
        """
        Move any feature information from the artist field to the track field.
        """

        valid_inputs = cls._ensure_valid_strings(string=artist) and cls._ensure_valid_strings(string=track_name)

        if valid_inputs is False:
            has_feat_in_artist = False
            return has_feat_in_artist, artist, track_name

        has_feat_in_artist, artist_without_feat, feat_info = cls._check_artist_for_feat(artist=artist)

        if has_feat_in_artist is True:

            feat_info = cls._ensure_brackets_around_feat(has_feat_in_artist=has_feat_in_artist, feat_info=feat_info)

            tpe1_updated, track_name_updated = cls._move_feat(
                artist_without_feat=artist_without_feat,
                track_name=track_name,
                feat_info=feat_info,
            )

            valid_outputs = cls._ensure_valid_strings(string=artist) and cls._ensure_valid_strings(string=track_name)  # Ensuring that the output also matches the validation criteria (e.g. minimum string length). This prevents edge case where only the feat. information was in the artist string.

            if valid_outputs:
                artist, track_name = tpe1_updated, track_name_updated
            else:
                has_feat_in_artist = False  # Setting this switch back to false.

        return has_feat_in_artist, artist, track_name

    @staticmethod
    def _ensure_valid_strings(string: str) -> list:
        """
        Check for the sanity of the input data. Both should contain valid strings.
        """

        is_valid = string is not None and len(string) >= 1

        return is_valid

    @staticmethod
    def _check_artist_for_feat(artist: str) -> list:
        """
        Check the artist field for " feat. " string and if that exists: extract it.
        """

        has_feat_in_artist = False
        artist_without_feat = ""
        feat_info = ""

        check = regex.search(r"(.+)(\s+feat\.\s+.+|\s+\(\s*feat\.\s+.+\))", artist, regex.IGNORECASE)  # Searching for " feat. " and " (feat. xyz)".

        if check is not None:
            has_feat_in_artist = True  # TODO Add sanity check that tit2 needs to be not none and have a length of at least 1 character.

            # Splitting into groups:
            artist_without_feat = check.group(1).strip()
            feat_info = check.group(2).strip()

        return has_feat_in_artist, artist_without_feat, feat_info

    @staticmethod
    def _ensure_brackets_around_feat(has_feat_in_artist, feat_info: str) -> str:
        """
        If the feat. info string that shall be moved does not yet have brackets around it. # TODO Check whether this also already works for feat. without brackets in the normal title. If not, can this be also called?
        """

        if has_feat_in_artist is False:
            return feat_info

        else:
            has_bracket = regex.match(r"^\s*\(\s*feat\.\s+.+\)\s*$", feat_info, regex.IGNORECASE)

            if has_bracket is None:
                feat_info = f"({feat_info.strip()})"  # Wrap brackets around string.

            return feat_info

    @staticmethod
    def _move_feat(artist_without_feat: str, track_name: str, feat_info: str) -> list:
        """
        Moving the feature info from the artist to the track title.
        """

        artist = artist_without_feat
        track_name = " ".join([track_name, feat_info])

        return artist, track_name

    @classmethod
    def sort_track_name_suffixes(cls, track_name: str, suffix_keywords: list) -> str:
        """
        Put any track names with multiple suffixes like (... remix), (acoustic), (live ...), (feat. ...) into an adequate order. The order comes from the order of the suffix_keywords list set in the script's options. However, "Live" will always be the last bracket.
        """

        at_least_two_sets_of_brackets = regex.search(r"(.+?)(\(.+\)\s\(.+\))", track_name, regex.IGNORECASE)  # Search for strings with multiple brackets at the end.

        if at_least_two_sets_of_brackets is None:  # No two sets of brackets found.
            return track_name

        else:
            track_name_without_suffix = at_least_two_sets_of_brackets.group(1).strip()  # Note that this would end with a space without the strip().
            suffixes_untouched_order = at_least_two_sets_of_brackets.group(2)  # This is one single string.

            suffixes_untouched_order = regex.findall(r"(\(.+?\))", suffixes_untouched_order, regex.IGNORECASE)  # Turn the single string into a list where each item is a string in brackets.

            defined_suffixes_dict = {}
            undefined_suffixes = ""

            # Splitting the found suffixes into defined and undefined ones.
            for i in suffixes_untouched_order:

                suffix = cls._remove_string_noise(i)

                if suffix.split()[0] in suffix_keywords or suffix.split()[-1] in suffix_keywords:  # Checking if found suffix is in keyword list.
                    defined_suffixes_dict[cls._find_suffix_keyword(text=i, suffix_keywords=suffix_keywords)] = i

                else:
                    undefined_suffixes = " ".join([undefined_suffixes, i])  # Keeping the original order.

            # Setting the new suffix order.
            defined_suffixes_ordered = ""
            live_suffix = ""

            for k in suffix_keywords:
                if k in defined_suffixes_dict.keys() and k != "live":  # The separation of "live" is needed here when undefined suffixes would be set between defined ones and live (which shall always be at the end).
                    defined_suffixes_ordered = f'{defined_suffixes_ordered} {defined_suffixes_dict.get(k) or ""}'
                else:
                    live_suffix = defined_suffixes_dict.get(k)

            defined_suffixes_ordered = f'{defined_suffixes_ordered} {undefined_suffixes or ""} {live_suffix or ""}'

            track_name_ordered = track_name_without_suffix + defined_suffixes_ordered

            track_name_ordered = regex.sub(r"\s+", " ", track_name_ordered).strip()

            return track_name_ordered

    @classmethod
    def _find_suffix_keyword(cls, text: str, suffix_keywords: list) -> str:
        """
        Search for the suffix keyword in the string. If not found, first string will be returned.
        """

        text = cls._remove_string_noise(text)

        first_word = text.split()[0]

        if first_word in suffix_keywords:
            return first_word

        elif first_word not in suffix_keywords:
            last_word = text.split()[-1]

            if last_word in suffix_keywords:
                return last_word

            else:
                random_key = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))  # Will generate a random key to solve cases where e.g. the suffixes are two times the same and not defined in the suffix_keywords.
                return random_key

        return first_word

    @staticmethod
    def _remove_string_noise(text: str) -> str:
        """
        Gets rid of not needed characters like non-alphanumeric characters and capitalization from a string.
        """

        text = regex.sub(pattern=r"[^0-9a-zA-Z\s]+", repl="", string=text)  # Removing any non-alphanumeric characters.
        text = text.lower()  # Uniquely transforming the word to lowercase.

        return text
