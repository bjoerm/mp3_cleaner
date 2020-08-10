
# TODO Convert backslash into slash and deal with question marks and such

import re # Regular expressions



def string_capitalization(text: str) -> str:
    # TODO Expand this here to prevent I'am from being turned into I'Am.
    # TODO Should I leave meE mEgA untouched? Aka. if there is any capital letter don't do anything? (If so, don't forget to still deal with brandon's)

    text_beautified = str(text) # Creating a copy of the input which is used, so the original input is kept for comparisons.


    # Beautify the input
    ## Whitespaces
    text_beautified = re.sub(" +", " ", text_beautified) # Remove any multiple whitespaces.
    text_beautified = re.sub("^ +", "", text_beautified) # Remove any whitespace at the start.
    text_beautified = re.sub(" +$", "", text_beautified) # Remove any whitespace at the end.

    ## Quotation marks
    text_beautified = re.sub("\"", "'", text_beautified) # Convert double (") quotation marks from string into single quotation marks ('). That helps as " is not wanted in filenames.

    ## Accents
    text_beautified = re.sub("`", "'", text_beautified) # Unify accents.
    text_beautified = re.sub("´", "'", text_beautified) # Unify accents.

    ## Colons
    text_beautified = re.sub("(?<=[a-zA-Z0-9]): (?=.+)", " - ", text_beautified) # Case of colon followed by whitespace. E.g.: Deus Ex: Human Revolution -> Deus Ex - Human Revolution
    text_beautified = re.sub("(?<=[a-zA-Z0-9]):[^ ](?=.+)", "-", text_beautified) # Case of colon followed by non-whitespace. E.g.: Deus:EX -> Deus-Ex or 12:34 -> 12-34. # TODO Do I really want "Deus:EX -> Deus-Ex"? This might screw up some other cases.

    ## Semicolons
    text_beautified = text_beautified.replace(";", ",") # Transform semicolons into commas.

    ## Missing space after comma
    text_beautified = re.sub("(?<=[a-zA-Z0-9]),[^ ](?=.+)", ", ", text_beautified)

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
    text_improved_list = re.sub("(?<=\w')S(?=\s+|$)", "s", text_improved_list) # Transforms Bjoern'S (capital S) into Bjoern's

    
    ## Special cases
    ### Bands
    text_improved_list = text_improved_list.replace(" 'N' ", " 'n' ")
    text_improved_list = text_improved_list.replace("'Ac/Dc'", "ACDC")

    # # Debugging
    # print("Original: " + text)
    # print("Improved: " + text_improved_list)

    return(text_improved_list)

# Some tests
## string_capitalization function
assert string_capitalization("Test's test's test`s test´s test'S") == "Test's Test's Test's Test's test's", "Test x"
assert string_capitalization("Ac/Dc AC/DC ac/dc guns 'n' roses") == "Ac/Dc AC/DC Ac/Dc Guns 'n' Roses", "Test x" # TODO Souldn't this return more ACDC?
assert string_capitalization("  lost in      space Lost in Space ") == "Lost In Space Lost In Space", "Test spaces"
# TODO Add test for colons, Accents, ...

