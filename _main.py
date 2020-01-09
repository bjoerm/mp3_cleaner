# Never ever bulk (!) search and replace the quotation marks as the exec command needs both " and ' at the same time.



# TODO Remove Leading "The " from Artist field.

# TODO tdrc should only contain the year.
# TODO trck should either everywhere or nowhere feature a leading zero.


# TODO
# Check whether this works if there are no tags at all.
## Solution for that: https://stackoverflow.com/questions/4040605/does-anyone-have-good-examples-of-using-mutagen-to-write-to-files


# Switch to mutagen normal - not easyid3
## http://www.blog.pythonlibrary.org/2010/04/22/parsing-id3-tags-from-mp3s-using-python/
## Or https://thebuildingcoder.typepad.com/blog/2013/02/mp3-manipulation-using-python-mutagen-and-ffmpeg.html use normal id3 and not easyid3.
## Should also be super easy see "4.   Declared ID3v2 frames" http://id3.org/id3v2.4.0-frames
## https://stackoverflow.com/questions/4040605/does-anyone-have-good-examples-of-using-mutagen-to-write-to-files


# Sources:
## https://mutagen.readthedocs.io/en/latest/user/gettingstarted.html
## https://mutagen.readthedocs.io/en/latest/api/id3.html




import glob  # For reading files and folders.
import os  # For file path check.
import re  # Regular expressions # TODO Do I need to write the dependency here again?
import time
from pathlib import Path  # For getting the parentfolder of the found mp3.
import shutil  # For copying folders to create backups.

import pandas as pd

from mutagen.id3 import ID3, ID3NoHeaderError, POPM, TALB, TDRC, TIT2, TPE1, TPE2, TPOS, TRCK

from string_capitalization import string_capitalization  # From local function.

# Options

## Tags

global_selected_id3_fields = {
    "POPM:no@email": "Rating"  # "Popularimeter" / Rating. The tag is structered like: 'POPM:no@email': POPM(email='no@email', rating=242, count=0).
    , "TALB": "String"  # "Album/Movie/Show title" # Album.
    , "TDRC": "Date"  # "Recording time" # Recording date ideally year.
    , "TIT2": "String"  # "Title/songname/content description" # Title.
    , "TPE1": "String"  # "Lead performer(s)/Soloist(s)" # Track artist.
    , "TPE2": "String"  # "Band/orchestra/accompaniment" # Album artist.
    , "TPOS": "Disc number"  # "Disc number".
    , "TRCK": "Track number"  # "Track number/Position in set" # Track number.    
}  # Key = Tag id and value = categorization within this script. Documentation on tag ids (called frames by mutagen): https://mutagen.readthedocs.io/en/latest/api/id3_frames.html#id3v2-3-4-frames

## Folders

original_folder = "untouched_input"  # Folder that is not touched.
working_folder = "input"  # Folder where files are saved.


# Setting up the workspace
def copy_files_to_working_folder(original_folder_input, working_folder_input):
    ## Delete working folder, if it exists.
    if os.path.exists(working_folder_input):
        shutil.rmtree(working_folder_input)

    time.sleep(1) # Wait for stuff e.g. Dropbox in my debug example to catch up.

    ## Copy files into a working folder so original files are not touched.
    shutil.copytree(original_folder_input, working_folder_input)


copy_files_to_working_folder(original_folder_input=original_folder, working_folder_input=working_folder)

time.sleep(1) # Wait for stuff e.g. Dropbox in my debug example to catch up.


## Convert file extension to lowercase for all mp3's in selected folder.
def convert_file_extension_to_lower_case(working_folder_input):
    files = glob.glob(working_folder_input + "/**/*.[mM][pP]3", recursive=True)

    for i in range(len(files)):
        pre, ext = os.path.splitext(files[i])

        os.rename(files[i], pre + ".mp3")  # Convert each file extention into lowercase.


convert_file_extension_to_lower_case(working_folder_input=working_folder)



def list_folders_with_mp3_files(folder):
    # This function will return all (unique) (sub)folders that contain .mp3 files in given main folder. # TODO Nice to have: Could be extended to use multiple inputs via *args.
    # This is currently a bit dirty by first searching for all .mp3s in the provided folder and its subfolders and then reduces this to only return the unique folders.
    # Grabs all mp3 files in the defined folder.
    files_list = glob.glob(
        folder + "/**/*.[mM][pP]3"  # glob itself seems to not care about whether file extension contain capital letters. Anyways, [mM][pP]3 is a bit safer than just mp3. # TODO double check that this does not perceive .mp3a as .mp3. Or if a folder contains the name .mp3 somewhere.
        , recursive=True)  # Recursive = True in combination with ** in the path will lead to a search in every folder and subfolder and subsubfolder and ...

    # Getting and attaching the folder path
    files = pd.DataFrame(data=files_list, columns=['file']) # Converting into a pandas data.frame and name the column.
    files['file'] = files['file'].apply(Path)  # Getting the path, so the "parent" method can be used in the following line.
    files['folder'] = files['file'].apply(lambda x: x.parent) # Getting the folder of that respective file.

    # Unique folders with mp3 files in it
    unique_folders = files.folder.unique()

    return(unique_folders) # Do only return the unique folders.


def list_mp3_files_in_folder(folder):
    folder = str(folder) # TODO Remove this?!? / or move this to a better part?

    # Grabs all mp3 files in the defined folder.
    files_in_folder = glob.glob(folder + "/**/*.[mM][pP]3", recursive=True)  # glob itself seems to not care about whether file extension contain capital letters. Anyways, [mM][pP]3 is a bit safer than just mp3. # Recursive = True in combination with ** in the path will lead to a search in every folder and subfolder and subsubfolder and ...

    # Converting into a data frame to allow (for later) addition of further information like the id3 tags into a column for each file.
    files_in_folder = pd.DataFrame(files_in_folder, columns =["filepath"])

    files_in_folder = files_in_folder.replace(r"\\", "/", regex=True) # There are some odd (escaped) backslashs coming from the glob.glob above. This is fixed (dirty) here.

    return(files_in_folder) # Returns a data.frame with all found mp3 files.



def read_all_tags_from_file(filepath):
    # Read the whole id3 tag for the respective file.
    try:
        id3 = ID3(filepath)
    except ID3NoHeaderError:  # If there is no id3 tag in file, give nothing back.
        return None

    return(id3) # Returns an ID3 object.




def extract_specified_tags(id3_object, dict_id3_fields_selected):

    # TODO Is the case if id3 being a None object possible? If so, code an exception.

    # If there are no tags, return None. # TODO The case of tags, but none of the ones that we are looking for should also be coded.
    if len(id3_object.keys()) == 0:
        return None
    
    # Checking the number of desired keys present in the file
    intersecting_keys = list(id3_object.keys() & dict_id3_fields_selected.keys())

    if(len(intersecting_keys) == 0):
        return None # If there are non tags, return None.

    # Reduce desired id3_fields to the ones that are present in the actual file.
    dict_id3_fields_selected = {key: value for key, value in dict_id3_fields_selected.items() if key in intersecting_keys} # Dictionary comprehension. Only keep the key values for keys that are members of intersecting_keys.
    


    # Storing the desired id3 information in a dictionary.
    output_dict_id3 = {}  # Create an empty dictionary.


    for key, value in dict_id3_fields_selected.items():  # Check which of the specified id3_fields are available in the tags and read them in accordingly. # TODO Code improvement: Loop through the intersecting_keys and not all keys from id3_fields.

        id3_field = None # Initialize / reset to an empty id3_field variable.

        # Check whether the defined id3_field exists in the file's tag information. If not, then skip this tag. # TODO Possible code improvement: Loop through the intersecting_keys and not all keys from id3_fields for speed improvements.
        if key not in id3_object.keys():
            continue

        # Read the tags
        id3_field = id3_object.get(key)  # Fetching the information for the respective id3 field from the id3 tag. Get returns a string (or None) while getall returns a list!

        ## If the certain tag ("key") is defined in id3_fields is not present in the mp3, then try the next tag.
        if id3_field is None:
            continue  # Skip to the next i in this loop.

        if value in ("Date", "Disc number", "String", "Track number"): # These fields (all but rating), have a text parameter which is extracted here. See https://mutagen.readthedocs.io/en/latest/api/id3_frames.html.
            id3_field = id3_field.text  # Extract the text/string information.

            id3_field = id3_field[0]  # There can be multiple tags attached. We just take the first element. This also ensures that the value is a string (which can be used in the string manipulation).

        else:
            continue
            # This else condition should not be reached. It is used to raise an alert, when new tag types are entered in the global variables but not yet defined here. That's a bit safer than just distinguishing between == "Rating" and != "Rating".
                # TODO Code this.

        
        
        # Adding the entry (both key and value) to the dictionary (which is returned from this function).
        ## None values to do not add any value and are omitted. # TODO Think whether an empty string "" should also be dropped. That could however also be done after the beautify string steps.
        if id3_field is not None: 
            output_dict_id3.update({key: id3_field})
        else:
            continue


    return(output_dict_id3) # TODO Do I need a check that returns None for empty dictionaries?



# End of functions




def run_main(folder, global_selected_id3_fields):
    unique_folders = list_folders_with_mp3_files(folder=folder)

    print(unique_folders)

    for folder in unique_folders:
        files_in_folder = list_mp3_files_in_folder(folder=folder)


        for file in files_in_folder["filepath"]:
            # Read id3 fields
            id3_object = read_all_tags_from_file(filepath=file) # This returns a mutagen id3 object
            
            # Extract specified tags
            dict_selected_fields = extract_specified_tags(id3_object=id3_object, dict_id3_fields_selected=global_selected_id3_fields) # This will return a dictionary for each file. 
            
            # TODO Append this to a list with each dictionary from this unique_folder. Then analyse it further w.r.t. album artist, track number (leading zeros) and disc number (disc number only if that is anyhow possible). Or I just always write disc number = 1 for the cases where non is provided. (If so, then I should also delete any leading zeros for disc numbers in general.)


            # Improve id3 tags (e.g. capitalization)
            # TODO
            # TODO Format TDRC (and potential other mutagen.id3.TimeStampTextFrame class tags) so that this is only a string, not a list (like it is read from the tag). Especially, as I only care for the year and not the exact relase day.


            # Update the id3 tag object
            ## Delete all existing tag information from the id3 object.
            id3_object.delete(delete_v1=True, delete_v2=True)

            def write_tags_into_id3_object(parameter_list):
                pass


            ## Write new id3 tags from id3_selected_fields dictionary into the id3 object
            for key, value in dict_selected_fields.items():
                # print(key) Renable for debugging.
                tag_type = global_selected_id3_fields.get(key)


                if tag_type in ("Date", "Disc number", "String", "Track number"): # All but rating, which does not have a text parameter. See https://mutagen.readthedocs.io/en/latest/api/id3_frames.html.

                    exec(f'id3_object.add({key}(encoding = 3, text = "{value}"))') # Executes the following string as Python command. The f in the beginning marks this as "f string". See https://www.python.org/dev/peps/pep-0498/

                elif tag_type == "Rating":
                    exec(f'id3_object.add({value})') # The structure for ratings is a bit different.                    


                else:
                    # This else condition should not be reached. It is used to raise an alert, when new tag types are entered in the global variables but not yet defined here. That's a bit safer than just distinguishing between == "Rating" and != "Rating".
                    # TODO Code this.

                    continue
                    # TODO Should I have an error message / notification here?


            # Save id3 tag object to mp3 file.
            id3_object.save(v1 = 0, v2_version = 4) # Saving only as id3v2.4 tags.

    return("End of script reached.")



# run_main(folder=working_folder + "/easy_test_single_file", global_selected_id3_fields=global_selected_id3_fields)

# Time tracking
start = time.process_time()

# Execute the script on the specified folder and for the specified id3 fields.
run_main(folder=working_folder, global_selected_id3_fields=global_selected_id3_fields)

# Print time tracking
print(time.process_time() - start)