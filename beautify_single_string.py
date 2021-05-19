import regex


class StringBeautifier:
    """
    This utility class bundles id3 tag beautification methods for strings. This class beautifies a single string at a time.
    """

    @classmethod
    def beautify_string(cls, text: str, remove_leading_the: bool = False) -> str:
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

        return text_beautified

    @staticmethod
    def _remove_not_needed_whitespaces(text: str) -> str:
        """
        Removes any case of unneeded whitespace.
        """

        text = regex.sub(r" +", " ", text)  # Remove any multiple whitespaces.
        text = regex.sub(r"^ +", "", text)  # Remove any whitespace at the start.
        text = regex.sub(r" +$", "", text)  # Remove any whitespace at the end.

        return text

    @staticmethod
    def _unify_quotation_marks_and_accents(text: str) -> str:
        """
        Convert double (") quotation marks from string into single quotation marks ('). That helps as " is not wanted in filenames. Also converts accents into '.
        """

        # Quotation marks
        text = regex.sub("\"", "'", text)

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
        text = regex.sub(r"(?<=[a-zA-Z\u0080-\uFFFF]): (?=.+)", " - ", text)  # \u0080-\uFFFF catches special characters from German and other languages https://stackoverflow.com/questions/36366125/

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

        text = regex.sub(r"(?<=[a-zA-Z\u0080-\uFFFF]),(?=[a-zA-Z\u0080-\uFFFF])|(?<=[0-9]),(?=[a-zA-Z\u0080-\uFFFF])|(?<=[a-zA-Z\u0080-\uFFFF]),(?=[0-9])", ", ", text, flags=regex.IGNORECASE)

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
        text = regex.sub(r"(?<=^)Featuring |(?<= |\()Featuring ", "Feat. ", text, flags=regex.IGNORECASE)  # This part of two positive lookbehinds is not very elegant but adding ^ into the other one, returned an error due to the varying widths of ^ and e.g. " "
        text = regex.sub(r"(?<=^)Pt. |(?<= |\()Pt. ", "Part ", text, flags=regex.IGNORECASE)
        text = regex.sub(r"(?<=^)remix(?=\)|$| )|(?<= |\()remix(?=\)|$| )", "Remix", text, flags=regex.IGNORECASE)  # Preventing all capitalized REMIX and other similar forms. Must have space or open bracket at the beginning.
        text = regex.sub(r"(?<=^)live(?=\)|$| )|(?<= |\()live(?=\)|$| )", "Live", text, flags=regex.IGNORECASE)  # Preventing all capitalized LIVE and other similar forms. Must have space or open bracket at the beginning.

        # Special band names
        text = regex.sub(r"(?<=^)ac-dc(?=\)|$| )|(?<= |\()ac-dc(?=\)|$| )", "ACDC", text, flags=regex.IGNORECASE)  # AC/DC

        return text


class StringHelper:
    """
    This utility class contains helper methods that are not related to the generic string beautification above.
    """

    @classmethod
    def move_feature_from_artist_to_track(cls, tpe1: str, tit2: str) -> list:

        valid_inputs = cls._ensure_valid_strings(string=tpe1) and cls._ensure_valid_strings(string=tit2)

        if valid_inputs is False:
            has_feat_in_tpe1 = False
            return has_feat_in_tpe1, tpe1, tit2

        has_feat_in_tpe1, tpe1_without_feat, feat_info = cls._check_artist(tpe1=tpe1)

        if has_feat_in_tpe1 is True:
            tpe1_updated, tit2_updated = cls._move_feat(tpe1_without_feat=tpe1_without_feat, tit2=tit2, feat_info=feat_info)

            valid_outputs = cls._ensure_valid_strings(string=tpe1) and cls._ensure_valid_strings(string=tit2)  # Ensuring that the output also matches the validation criteria (e.g. minimum string length). This prevents edge case where only the feat. information was in the artist string.

            if valid_outputs:
                tpe1, tit2 = tpe1_updated, tit2_updated
            else:
                has_feat_in_tpe1 = False  # Setting this switch back to false.

        return has_feat_in_tpe1, tpe1, tit2

    @staticmethod
    def _ensure_valid_strings(string: str) -> list:
        """
        Check for the sanity of the input data. Both should contain valid strings.
        """

        is_valid = string is not None and len(string) >= 1

        return(is_valid)

    @staticmethod
    def _check_artist(tpe1: str) -> list:
        """
        Check the artist field for " feat. " string and if that exists: extract it.
        """

        has_feat_in_tpe1 = False
        tpe1_without_feat = ""
        feat_info = ""

        check = regex.search(r"(.+)(\s+feat.\s.+)", tpe1, regex.IGNORECASE)

        if check is not None:
            has_feat_in_tpe1 = True  # TODO Add sanity check that tit2 needs to be not none and have a length of at least 1 character.

            # Splitting into groups:
            tpe1_without_feat = check.group(1)
            feat_info = check.group(2)  # This will start with a space which is okay.

        return has_feat_in_tpe1, tpe1_without_feat, feat_info

    @staticmethod
    def _move_feat(tpe1_without_feat: str, tit2: str, feat_info: str) -> list:
        """
        Moving the feature info from the artist to the track title.
        """

        tpe1 = tpe1_without_feat
        tit2 = tit2 + feat_info  # TODO Make this smarter to account for other suffixes like Remix, Live, ...

        return tpe1, tit2
