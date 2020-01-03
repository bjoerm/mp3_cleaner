# TODO First step should be a migration to id3v2.4 tags. Mutagen does this by default, when saving.
## Source: https://mutagen.readthedocs.io/en/latest/user/id3.html
## By default mutagen will:
## Load the file
## Upgrade any ID3v2.2 frames to their ID3v2.3/4 counterparts (TT2 to TIT2 for example)

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


# Console:
## conda activate mp3_cleaner


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

selected_id3_fields = {
    # "POPM": "Rating"  # "Popularimeter" # Rating # TODO Remove as the key is constructed differently (see following line).
    "POPM:no@email": "Rating"   # The tag is structered like: 'POPM:no@email': POPM(email='no@email', rating=242, count=0)
    , "TALB": "String"  # "Album/Movie/Show title" # Album
    , "TDRC": "Date"  # "Recording time" # Recording date ideally yar.
    , "TIT2": "String"  # "Title/songname/content description" # Title
    , "TPE1": "String"  # "Lead performer(s)/Soloist(s)" # Track artist.
    , "TPE2": "String"  # "Band/orchestra/accompaniment" # Album artist
    , "TPOS": "Disc number"  # "Disc number"
    , "TRCK": "Track number"  # "Track number/Position in set" # Track number
}  # Key = Tag id and value = categorization within this script.

## Folders

original_folder = "untouched_input"  # Folder that is not touched.
working_folder = "input"  # Folder where files are saved.


# Setting up the workspace
## Restoring test workspace from last test.
def setting_up_workspace(original_folder_input, working_folder_input):
    ## Delete working folder, if it exists.
    if os.path.exists(working_folder_input):
        shutil.rmtree(working_folder_input)

    time.sleep(2) # Wait for stuff e.g. Dropbox in my debug example to catch up.

    ## Copy files into a working folder so original files are not touched.
    shutil.copytree(original_folder_input, working_folder_input)


setting_up_workspace(original_folder_input=original_folder, working_folder_input=working_folder)

time.sleep(3) # Wait for stuff e.g. Dropbox in my debug example to catch up.


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




def extract_specified_tags(id3_fields_all, id3_fields_selected):

    # TODO Is the case if id3 being a None object possible? If so, code an exception.

    # If there are no tags, return None. # TODO The case of tags, but none of the ones that we are looking for should also be coded.
    if len(id3_fields_all.keys()) == 0:
        return None
    
    # Checking the number of desired keys present in the file
    intersecting_keys = list(id3_fields_all.keys() & id3_fields_selected.keys())

    if(len(intersecting_keys) == 0):
        return None # If there are non tags, return None.

    # Reduce desired id3_fields to the ones that are present in the actual file.
    id3_fields_selected = {key: value for key, value in id3_fields_selected.items() if key in intersecting_keys} # Dictionary comprehension. Only keep the key values for keys that are members of intersecting_keys.
    


    # Storing the desired id3 information in a dictionary.
    id3_dictionary = {}  # Create an empty dictionary.


    for key, value in id3_fields_selected.items():  # Check which of the specified id3_fields are available in the tags and read them in accordingly. # TODO Code improvement: Loop through the intersecting_keys and not all keys from id3_fields.

        id3_field = None # Initialize / reset to an empty id3_field variable.

        # Check whether the defined id3_field exists in the file's tag information. If not, then skip this tag. # TODO The following would make this check chunk obsolete. Code improvement: Loop through the intersecting_keys and not all keys from id3_fields.
        if key not in id3_fields_all.keys():
            print(key + "not present")
            continue

        # Read the tags
        if value in ("Date", "Disc number", "String", "Track number"):
            id3_field = id3_fields_all.get(key)  # Fetching the information for the respective id3 field from the id3 tag. Get returns a string (or None) while getall returns a list!

            # If the certain tag ("key") is defined in id3_fields is not present in the mp3, then try the next tag.
            if id3_field is None:
                continue  # Skip to the next i in this loop.

            id3_field = id3_field.text  # Extract the text/string information.

            id3_field = id3_field[0]  # There can be multiple tags attached. We just take the first element. This also ensures that the value is a string (which can be used in the string manipulation).

        elif value == "Rating":
            id3_field = id3_fields_all.get(key)  # Fetching the information for the respective id3 field from the id3 tag. Get returns a string (or None) while getall returns a list!

            # If the certain tag ("key") is defined in id3_fields is not present in the mp3, then try the next tag.
            if id3_field is None:
                continue  # Skip to the next i in this loop.



        # Stop for tags that are not yet implemented. (Only works if the conditions above are chained via elif)
        else:
            continue

        
        
        # Adding the entry (both key and value) to the dictionary.
        ## None values to do not add any value and are omitted. # TODO Think whether an empty string "" should also be dropped. That could however also be done after the beautify string steps.
        if id3_field is not None: 
            id3_dictionary.update({key: id3_field})
        else:
            continue

    # Show the initial tags
    print(id3_fields_all)


    # Show the collected tags
    print(id3_dictionary) # TODO Remove this line.

    return(id3_dictionary) # TODO Do I need a check that returns None for empty dictionaries?










# End of functions








# WIP WIP WIP WIP WIP


list_folders_with_mp3_files(folder=working_folder)


# test_list = list_mp3_files_in_folder("input/deep/mp3")
test_list = list_mp3_files_in_folder(folder=working_folder + "/Has MM Ratings Tags") # No slash at the beginning nor the end.


test_read = read_all_tags_from_file(filepath=test_list["filepath"][0])

test_extract = extract_specified_tags(id3_fields_all=test_read, id3_fields_selected=selected_id3_fields)

print(test_extract)

# for folder in unique_folders:

#     files_in_folder = list_mp3_files_in_folder(folder=folder)

#     for file in files_in_folder:
#         # Read id3 fields
#         id3_all = read_all_tags_from_file(filepath=file)
#         
#         # Extract specified tags
#         id3_selected_fields = extract_specified_tags(id3_fields_all=id3_all, id3_fields_selected=id3_fields) # This will return a dictionary for each file. # TODO Append this to a list with each dictionary from this unique_folder. Then analyse it further w.r.t. album artist, track number (leading zeros) and disc number (disc number only if that is anyhow possible). Or I just always write disc number = 1 for the cases where non is provided. (If so, then I should also delete any leading zeros for disc numbers in general.)


# WIP WIP WIP WIP WIP












#     # TODO id3.add add Tag
#     ## Remove all tags (e.g. id3.delall) and then add them again with results from this dictionary.
#     ## audio.add(TALB(encoding = 3, text = u"An example")) # TODO What does the encoding=3 stand for? 3 = UTF8.
#     ## Ensure that this write id3v2.4 tags and does not keep any old id3 tag version.
#
#     id3.delete(delete_v1 = True, delete_v2 = True) # Delete all tags from the file.
#
#     # Adding the tag to the id3 python object.
#     id3.add(TPE1(encoding = 3, text = id3_dictionary["TPE1"])) # TODO Make this dynamic w.r.t. to the values in the dictionary.
#
#
#     for key in id3_dictionary:
#         if key == "POPM": # TODO Add that again!
#             continue
#
#         exec('id3.add('+key+'(encoding = 3, text = id3_dictionary["'+key+'"]))') # Execute the following string as Python command.
#     # prog = 'print("The sum of 5 and 10 is", (5+10))'
#     # exec(prog)
#
#
#     # Writing the tag to the file.
#     id3.save()
#
#
#
#     # def store(self, mutagen_file, value):
#     #         frame = mutagen.id3.Frames[self.key](encoding=3, text=[value])
#     #         mutagen_file.tags.setall(self.key, [frame])
#
#
# # # TODO Best approach:
# # ## Fetch Track Number, Disc Number, Date, Artist, Album Artist, Title, (maybe also rating, picture, loudness (should be one or both: TXXX RGAD) for existing files, TXXX enthält viel mehr als nur .text). (Maybe also PCNT Play counter)
# # ## Then delete all tags.
# # ## Write the earlier fetched information again into a fresh new id3 v2.4 tag which is also in UTF8. -> All other crappy information like Amazon Song Id, Genre, ... are gone. Also odd tag text formats are replaced by UTF8
#
#
# # audio.delete(delete_v1 = True, delete_v2 = False) # Only delete ID3 v1 tags. Note that this already writes into the files!
# # print(audio)
#
#
# # audio.save(v1 = 0, v2_version = 4, v23_sep = '/', padding = None)