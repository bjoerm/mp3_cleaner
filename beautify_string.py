# TODO Check case of having special characters (Umlaute etc.).

# TODO Deal with % and $ - maybe also log those or raise alerts. Or ask for user input as $ might be sometimes be best represented with an S and sometimes with an USD or Dollar.
# TODO Unify hyphens into - (might need the unicode for the longer hyphens for that).
# TODO Expand the a-zA-Z for German umlaute: [^\x00-\x7F(?:\u00c4, \u00e4,\u00d6,\u00f6,\u00dc,\u00fc,\u00df)] https://stackoverflow.com/questions/22017723/regex-for-umlaut
# TODO Turn rectangular brackets (in tags) into round brackets. [] into ()


from os import stat
import re # Regular expressions

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
        text_beautified = cls._replace_special_characters(text=text_beautified)
        text_beautified = cls._fill_missing_space_after_comma(text=text_beautified)
        text_beautified = cls._remove_leading_the(remove_leading_the=remove_leading_the, text=text_beautified) # Will only remove if remove_leading_the = True.
        
        text_beautified = cls._capitalize_string(text=text_beautified)
        
        text_beautified = cls._deal_with_special_words_and_bands(text=text_beautified)

        return(text_beautified)


    @staticmethod
    def _remove_not_needed_whitespaces(text: str) -> str:
        output = text
        
        output = re.sub(r" +", " ", output) # Remove any multiple whitespaces.
        output = re.sub(r"^ +", "", output) # Remove any whitespace at the start.
        output = re.sub(r" +$", "", output) # Remove any whitespace at the end.
        
        return(output)
    
    
    @staticmethod
    def _unify_quotation_marks_and_accents(text: str) -> str:
        """
        Convert double (") quotation marks from string into single quotation marks ('). That helps as " is not wanted in filenames. Also converts accents into '.
        """
        output = text
        
        # Quotation marks
        output = re.sub("\"", "'", output)

        # Accents
        output = re.sub("`", "'", output)
        output = re.sub("´", "'", output)
        
        return(output)
    
    
    @staticmethod
    def _beautify_colons(text: str) -> str:
        output = text
        
        output = re.sub(r"(?<=[a-zA-Z0-9]): (?=.+)", " - ", output) # Case of colon followed by whitespace. E.g.: Deus Ex: Human Revolution -> Deus Ex - Human Revolution
        output = re.sub(":", "-", output) # All other cases of a colon.
        
        return(output)
    
    
    @staticmethod
    def _replace_special_characters(text: str) -> str:
        output = text
        
        # Semicolons
        output = output.replace(";", ",")
        
        # Slashes
        output = output.replace("\\", "-")
        output = output.replace("/", "-")
        
        # Question marks
        output = output.replace("?", "")
        
        # Ampersand (&)
        output = output.replace("&", "+")
        
        return(output)
    
    
    @staticmethod
    def _fill_missing_space_after_comma(text: str) -> str:
        """
        Missing space after comma - as long as it is not followed by digits.
        """
        output = text
        
        output = re.sub(r"(?<=[a-zA-Z]),(?=[a-zA-Z])|(?<=[0-9]),(?=[a-zA-Z])|(?<=[a-zA-Z]),(?=[0-9])", ", ", output, flags=re.IGNORECASE) # [a-zA-Z] does not contain German umlaute.
        
        return(output)
    
    
    @staticmethod
    def _remove_leading_the(remove_leading_the: bool, text: str) -> str:
        
        if remove_leading_the == False:
            return(text)
        
        if text in ["The", "the"]:
            return(text)
        
        output = text
        
        output = re.sub(r"^(the\s)", "", output, flags=re.IGNORECASE)
        
        return(output)
    
    
    @staticmethod
    def _capitalize_string(text: str) -> str:
        
        if text == "":
            return(text)
        
        # Break the string into pieces at place with a space (into a list).
        text_list = text.split(" ") 

        # For each pieces, run capitalization.
        for i in range(len(text_list)):
            if re.match(r"^[^A-Z]*$", text_list[i]): # If the string piece does not contain any capital letter, then use the title string method on it.
                text_improved = text_list[i].title()

            else:
                text_improved = text_list[i]
            
            # Glueing the list back into a string.
            if i == 0:
                output = text_improved
            else:
                output = output + " " + text_improved

        # Dealing with a special case:
        output = re.sub(r"(?<=\w')S(?=\s+|$)", "s", output) # Transforms Bernd'S (capital S) into Bernd's. This only happens if the 'S had been in capital letter even before the title method.
        
        return(output)
    
    
    @staticmethod
    def _deal_with_special_words_and_bands(text: str) -> str:
        """
        Deal with special cases like the strings featuring, pt., remix or live.
        """
        output = text
        
        # Special words
        output = re.sub(r"(?<=^)Featuring |(?<= |\()Featuring ", "Feat. ", output, flags=re.IGNORECASE) # This part of two positive lookbehinds is not very elegant but adding ^ into the other one, returned an error due to the varying widths of ^ and e.g. " "
        output = re.sub(r"(?<=^)Pt. |(?<= |\()Pt. ", "Part ", output, flags=re.IGNORECASE)
        output = re.sub(r"(?<=^)remix(?=\)|$| )|(?<= |\()remix(?=\)|$| )", "Remix", output, flags=re.IGNORECASE) # Preventing all capitalized REMIX and other similar forms. Must have space or open bracket at the beginning.
        output = re.sub(r"(?<=^)live(?=\)|$| )|(?<= |\()live(?=\)|$| )", "Live", output, flags=re.IGNORECASE) # Preventing all capitalized LIVE and other similar forms. Must have space or open bracket at the beginning.
        
        # Special band names
        output = output.replace(" 'N' ", " 'n' ") # Guns 'n' Roses.
        output = re.sub(r"(?<=^)ac-dc(?=\)|$| )|(?<= |\()ac-dc(?=\)|$| )", "ACDC", output, flags=re.IGNORECASE) # AC/DC

        return(output)
    