from mutagen.id3 import ID3, ID3NoHeaderError, POPM, TALB, TDRC, TIT2, TPE1, TPE2, TPOS, TRCK

# TODO Convert into class. Add the "selfs".
# TODO I want to use the Environment.get_files_and_folders method in another class. How to best do that?

class Mp3Tags:
    
    def read_all_tags_from_file(filepath):
        # Read the whole id3 tag for the respective file.
        try:
            id3 = ID3(filepath)
        except ID3NoHeaderError:  # If there is no id3 tag in file, give nothing back.
            return None

        return(id3) # Returns an ID3 object.

    # TODO Have the following checks in the reading parts / or (partly) after the intersection check:
        # # TODO Is the case if id3 being a None object possible? If so, code an exception. Or better have that exception in the main function and not in this check here.

        # # If there are no tags, return None. # TODO The case of tags, but none of the ones that we are looking for should also be coded.
        # if len(id3_object.keys()) == 0:
        #     return None

        # if(len(intersecting_keys) == 0):
        # return None # If there are non of the desired tags availabe, return None.

        # intersecting_keys.sort()


    def look_for_available_specified_tags(id3_object, dict_id3_fields_selected):
        # Checking the number of desired keys present in the id3 object
        available_specified_tags = list(id3_object.keys() & dict_id3_fields_selected.keys())

        # Sorting the list
        available_specified_tags.sort()

        return(available_specified_tags)


    def extract_available_specified_tags(id3_object, available_specified_tags):

        # Storing the extracted id3 information in a dictionary.
        extracted_tags = {}  # Initialize / reset to an empty dictionary.

        for tag in available_specified_tags:
            id3_field = None # Initialize / reset to an empty variable.

            # Read the tags
            id3_field = id3_object.get(tag)  # Fetching the information for the respective id3 field from the id3 tag. Get returns a string (or None) while getall returns a list!

            ## Special filter for tags with a text fields (could also have been done in a seperate function). # TODO Think about putting this into a seperate function for less complexity per function.
            if tag == "POPM:no@email": # Does not have a text field. So no further operation is required before it will be saved below.
                pass

            elif tag in ("TALB", "TDRC", "TIT2", "TPE1", "TPE2", "TPOS", "TRCK"): # These fields (all but rating), have a text parameter which is extracted here. See https://mutagen.readthedocs.io/en/latest/api/id3_frames.html.
                id3_field = id3_field.text  # Extract the text/string information.

                id3_field = id3_field[0]  # There can be multiple tags attached. We just take the first element. This also ensures that the value is a string (which can be used in the string manipulation).

            else:
                continue # This else condition should not be reached. It is used to raise an alert, when new tag types are entered in the global variables but not yet defined here. That's a bit safer than just distinguishing between == "Rating" and != "Rating".
                # TODO Code this.
            
            # Adding the entry (both key and value) to the dictionary (which is returned from this function).
            ## None values to do not add any value and are omitted. # TODO Think whether an empty string "" should also be dropped. That could however also be done after the beautify string steps.
            if (id3_field is not None) & (id3_field != ""): 
                extracted_tags.update({tag: id3_field})
            else:
                continue

        return(extracted_tags) # TODO Do I need a check that returns None for empty dictionaries?



    def write_tags_into_id3_object(id3_object, clean_tags):

        for key, value in clean_tags.items():

            if key == "POPM:no@email": # Does not have a text field and thus a bit different structure.
                exec(f'id3_object.add({value})') # Executes the following string as Python command. The f in the beginning marks this as "f string". See https://www.python.org/dev/peps/pep-0498/

            elif key in ("TALB", "TDRC", "TIT2", "TPE1", "TPE2", "TPOS", "TRCK"): # These fields (all but rating), have a text parameter which can be added the same way.
                exec(f'id3_object.add({key}(encoding = 3, text = "{value}"))') 

            else:
                # This else condition should not be reached. It is used to raise an alert, when new tag types are entered in the global variables but not yet defined here. That's a bit safer than just distinguishing between == "Rating" and != "Rating".
                # TODO Code this.
                continue

        return(id3_object)