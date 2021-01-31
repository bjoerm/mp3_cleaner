import re # Regular expressions
import regex

class beautify_string:
    """
    This utility class bundles id3 tag beautification methods for strings. This class beautifies a single string at a time.
    """
    
    @classmethod
    def beautify_string(cls, text: str, remove_leading_the: bool=False) -> str:
        """
        This method beautifies strings. It removes not needed whitespaces, deals with special characters and some other things. It also capitalizes the string to appear more uniform.
        """

        if text == None: # Edge case of input being None.
            return(None)

        text_beautified = str(text) # Creating a copy of the input which is used, so the original input is kept for comparisons. And ensuring that the text is a string.


        # Beautify the string
        text_beautified = cls._remove_not_needed_whitespaces(text=text_beautified)
        text_beautified = cls._unify_quotation_marks_and_accents(text=text_beautified)
        text_beautified = cls._beautify_colons(text=text_beautified)
        text_beautified = cls._enforce_round_brackets(text=text_beautified)
        text_beautified = cls._unify_hyphens(text=text_beautified)
        text_beautified = cls._replace_special_characters(text=text_beautified)
        text_beautified = cls._fill_missing_space_after_comma(text=text_beautified)
        text_beautified = cls._remove_leading_the(remove_leading_the=remove_leading_the, text=text_beautified) # Will only remove if the input variable remove_leading_the is set to True.
        
        
        text_beautified = cls._capitalize_string(text=text_beautified)
        
        text_beautified = cls._deal_with_special_words_and_bands(text=text_beautified)

        return(text_beautified)


    @staticmethod
    def _remove_not_needed_whitespaces(text: str) -> str:
        """
        Removes any case of unneeded whitespace.
        """
        
        text = re.sub(r" +", " ", text) # Remove any multiple whitespaces.
        text = re.sub(r"^ +", "", text) # Remove any whitespace at the start.
        text = re.sub(r" +$", "", text) # Remove any whitespace at the end.
        
        return(text)
    
    
    @staticmethod
    def _unify_quotation_marks_and_accents(text: str) -> str:
        """
        Convert double (") quotation marks from string into single quotation marks ('). That helps as " is not wanted in filenames. Also converts accents into '.
        """
        
        # Quotation marks
        text = re.sub("\"", "'", text)

        # Accents
        text = re.sub("`", "'", text)
        text = re.sub("´", "'", text)
        
        return(text)
    
    
    @staticmethod
    def _beautify_colons(text: str) -> str:
        """
        Convert colons to dashes. Deal with case "Abc: Abc" and "Abc:Abc" differently.
        """
        
        # Case of colon followed by whitespace. E.g.: Deus Ex: Human Revolution -> Deus Ex - Human Revolution
        text = re.sub(r"(?<=[a-zA-Z\u0080-\uFFFF]): (?=.+)", " - ", text) # \u0080-\uFFFF catches special characters from German and other languages https://stackoverflow.com/questions/36366125/
        
        # All other cases of a colon.
        text = re.sub(":", "-", text)
        
        return(text)
    
    
    @staticmethod
    def _enforce_round_brackets(text: str) -> str:
        """
        Converts curly and square brackets into round brackets.
        """
        text = re.sub(r"\[+|\{+|⟨+", "(", text)
        text = re.sub(r"\]+|\}+|⟩+", ")", text)
        
        
        return(text)
    
    
    @staticmethod
    def _unify_hyphens(text: str) -> str:
        """
        Convert all types of hyphens into simple "-".
        """
        
        text = regex.sub(r"\p{Pd}", "-", text) # Pd matches every unicode character from the 'Punctuation, Dash' category: https://www.fileformat.info/info/unicode/category/Pd/list.htm
        
        return(text)
    
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
        
        # Ampersand (&)
        text = text.replace("&", "+")
        
        return(text)
    
    
    @staticmethod
    def _fill_missing_space_after_comma(text: str) -> str:
        """
        Missing space after comma - as long as it is not followed by digits.
        """
        
        text = re.sub(r"(?<=[a-zA-Z\u0080-\uFFFF]),(?=[a-zA-Z\u0080-\uFFFF])|(?<=[0-9]),(?=[a-zA-Z\u0080-\uFFFF])|(?<=[a-zA-Z\u0080-\uFFFF]),(?=[0-9])", ", ", text, flags=re.IGNORECASE)
        
        return(text)
    
    
    @staticmethod
    def _remove_leading_the(remove_leading_the: bool, text: str) -> str:
        """
        Remove any leading "The " from the string.
        """
        
        
        if remove_leading_the == False:
            return(text)
        
        if text in ["The", "the"]:
            return(text)
        
        text = re.sub(r"^(the\s)", "", text, flags=re.IGNORECASE)
        
        return(text)
    

    
    
    
    @staticmethod
    def _capitalize_string(text: str) -> str:
        """
        Capitalize each word of the string.
        """
        
        if text == "":
            return(text)
        
        # Break the string into pieces at place with a space (into a list).
        text_list = text.split(" ")
        text_list_improved = text_list.copy()

        # For each pieces, run capitalization.
        for i in range(len(text_list)):
            if regex.match(r".*\p{Lu}+.*", text_list[i]): # Does the string contain a capital letter somewhere? If so, leave it as it is.
                text_list_improved[i] = text_list[i]
            
            elif regex.match(r".+['|`|´]\w+", text_list[i]): # Does the string contains an accent (', ` or ´) before a string? If so, don't transform the part after the accent into uppercase. This needs to be done, after the check above for captial letters.
                text_list_improved[i] = text_list[i].capitalize() # Capitalizes transforms that's into That's. While title would transform it into That'S.
            
            else: # Convert it to uppercase.
                text_list_improved[i] = text_list[i].title()
        
        
        # Converting the list of strings back into a string.
        separator = " "
        output = separator.join(text_list_improved) # Converting the list of strings into a string.
        
        return(output)
    
    
    @staticmethod
    def _deal_with_special_words_and_bands(text: str) -> str:
        """
        Deal with special cases like the strings featuring, pt., remix or live.
        """
        
        # Special words
        text = re.sub(r"(?<=^)Featuring |(?<= |\()Featuring ", "Feat. ", text, flags=re.IGNORECASE) # This part of two positive lookbehinds is not very elegant but adding ^ into the other one, returned an error due to the varying widths of ^ and e.g. " "
        text = re.sub(r"(?<=^)Pt. |(?<= |\()Pt. ", "Part ", text, flags=re.IGNORECASE)
        text = re.sub(r"(?<=^)remix(?=\)|$| )|(?<= |\()remix(?=\)|$| )", "Remix", text, flags=re.IGNORECASE) # Preventing all capitalized REMIX and other similar forms. Must have space or open bracket at the beginning.
        text = re.sub(r"(?<=^)live(?=\)|$| )|(?<= |\()live(?=\)|$| )", "Live", text, flags=re.IGNORECASE) # Preventing all capitalized LIVE and other similar forms. Must have space or open bracket at the beginning.
        
        # Special band names
        text = text.replace(" 'N' ", " 'n' ") # Guns 'n' Roses.
        text = re.sub(r"(?<=^)ac-dc(?=\)|$| )|(?<= |\()ac-dc(?=\)|$| )", "ACDC", text, flags=re.IGNORECASE) # AC/DC

        return(text)
    