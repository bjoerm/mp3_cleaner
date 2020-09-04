
# TODO Maybe pause script and ask user (if that is easily possible), otherwise just halt in case when there are special characters like % and $
# TODO Unify hyphens into - (might need the unicode for the longer hyphens for that).
# TODO Expand the a-zA-Z for German umlaute: [^\x00-\x7F(?:\u00c4, \u00e4,\u00d6,\u00f6,\u00dc,\u00fc,\u00df)] https://stackoverflow.com/questions/22017723/regex-for-umlaut
# TODO Rectangular brackets into round brackets. [] into ()


import re # Regular expressions


def string_beautification(text: str, remove_leading_the: bool=False) -> str:

    text_beautified = str(text) # Creating a copy of the input which is used, so the original input is kept for comparisons. And ensuring that the text is a string.

    # Beautify the input
    ## Whitespaces
    text_beautified = re.sub(" +", " ", text_beautified) # Remove any multiple whitespaces.
    text_beautified = re.sub("^ +", "", text_beautified) # Remove any whitespace at the start.
    text_beautified = re.sub(" +$", "", text_beautified) # Remove any whitespace at the end.

    ## Quotation marks
    text_beautified = re.sub("\"", "'", text_beautified) # Convert double (") quotation marks from string into single quotation marks ('). That helps as " is not wanted in filenames.

    ## Accents
    text_beautified = re.sub("`", "'", text_beautified)
    text_beautified = re.sub("´", "'", text_beautified)

    ## Colons
    text_beautified = re.sub("(?<=[a-zA-Z0-9]): (?=.+)", " - ", text_beautified) # Case of colon followed by whitespace. E.g.: Deus Ex: Human Revolution -> Deus Ex - Human Revolution
    text_beautified = re.sub("(?<=[a-zA-Z0-9]):[^ ](?=.+)", "-", text_beautified) # Case of colon followed by non-whitespace. E.g.: Deus:EX -> Deus-Ex or 12:34 -> 12-34.
    text_beautified = re.sub(" : ", " - ", text_beautified) # Case of colon surrounded by whitespace. E.g.: Deus Ex : Human Revolution -> Deus Ex - Human Revolution

    ## Semicolons
    text_beautified = text_beautified.replace(";", ",")
    
    ## Slashes
    text_beautified = text_beautified.replace("\\", "-")
    text_beautified = text_beautified.replace("/", "-")
    
    ## Question marks
    text_beautified = text_beautified.replace("?", "")
    
    ## Ampersand (&)
    text_beautified = text_beautified.replace("&", "+")

    ## Missing space after comma - as long as it is not followed by digits.
    text_beautified = re.sub("(?<=[a-zA-Z0-9]),(?=[a-zA-Z])", ", ", text_beautified) # [a-zA-Z] does not contain German umlaute.
    
    ## Leading "The"
    if remove_leading_the == True:
        text_beautified = re.sub("^([T|t][H|h][E|e]\s)", "", text_beautified)
    
    ## Special cases
    text_beautified = re.sub(" [F|f]eaturing ", " Feat. ", text_beautified)
    text_beautified = re.sub(" [P|p]t. ", " Part ", text_beautified)


    # Break the string into pieces (into a list).
    text_list = text_beautified.split(" ") 

    # For each pieces, run capitalization.
    for i in range(len(text_list)): # for i in text_vec: would have also worked but not provided the number of the current loop (i) but would have returned the full string as result of print(i).
        if re.match("^[^A-Z]*$", text_list[i]): # If the string piece does not contain any capital letter, then use the title method on it.
            text_improved = text_list[i].title()

        else:
            text_improved = text_list[i]

        if i == 0:
            text_improved_list = text_improved
        else:
            text_improved_list = text_improved_list + " " + text_improved

    # Additional beautification after capitalization    
    ## 's
    text_improved_list = re.sub("(?<=\w')S(?=\s+|$)", "s", text_improved_list) # Transforms Bernd'S (capital S) into Bernd's

    
    ## Special cases
    ### Special band names
    text_improved_list = text_improved_list.replace(" 'N' ", " 'n' ")
    text_improved_list = re.sub("[A|a][C|c]-[D|d][C|c]", "ACDC", text_improved_list) # AC/DC

    # # Debugging
    # print("Original: " + text)
    # print("Improved: " + text_improved_list)

    return(text_improved_list)

