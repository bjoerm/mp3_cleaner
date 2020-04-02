
import glob  # For reading files and folders.
import os  # For file path check.
import pandas as pd
from pathlib import Path  # For getting the parentfolder of the found mp3.
import shutil  # For copying folders to create backups.



class Environment: # TODO Find a more fitting name.

    def __init__(self, input_path: str, wip_path: str):

        self.input_path = input_path # TODO Ask Volker whether the underscore in the beginning is commonly used style to name (self) variables in a class.
        self.wip_path = wip_path
        self.files_and_folders = pd.DataFrame(columns=["file", "folder"]) # TODO Ask Volker whether it makes sense to put functions from the environment already in the __init__ or whether this should be done in the "main" call of that environment? As of now this only fetches it at the beginning once and even prior moving files or change file extension to lowercase. So this already hints at the reasonable answer. ;-)        

        self.unique_mp3_folders = [] # TODO Ask Volker whether I should even bother with defining these empty self.variables at all. Or whether I should either don't define them at all or define them even just as None (as they will be overwritten anyway).

        # Execute one-time needed functions:
        ## Setting up working environment
        self.copy_files_to_working_folder()

        ## Get list of files and folders (which is triggered from inside the get_unique_mp3_folders function) as well as the list of the unique folders.
        self.get_unique_mp3_folders()

        ## Convert all file extensions to lowercase
        self.convert_file_extension_to_lowercase()


    def copy_files_to_working_folder(self):
        """ Setting up the workspace. """
        
        # Delete previously existing working folder, if it exists.
        if os.path.exists(self.wip_path):
            shutil.rmtree(self.wip_path)

        # Copy files into a working folder so original files are not touched.
        shutil.copytree(self.input_path, self.wip_path)


    def get_mp3_files_and_folders(self):        
        """ This function will return a two column data frame with all mp3 files and the folder that contains the .mp3 file. """
        
        # Grabs all mp3 files in the defined folder.
        files_list = glob.glob(
            self.wip_path + "/**/*.[mM][pP]3"  # glob itself seems to not care about whether file extension contain capital letters. Anyways, [mM][pP]3 is a bit safer than just mp3. This does not perceive .mp3a as .mp3. TODO Check whether it has problems with folders that contains the .mp3 somewhere.
            , recursive=True)  # Recursive = True in combination with ** in the path will lead to a search in every folder and subfolder and subsubfolder and ...

        # Getting and attaching the folder path
        files = pd.DataFrame(data=files_list, columns=['file']) # Converting into a pandas data.frame and name the column.
        files['file'] = files['file'].apply(Path)  # Getting the path, so the "parent" method can be used in the following line.
        files['folder'] = files['file'].apply(lambda x: x.parent) # Getting the folder of that respective file.

        self.files_and_folders = files # Updating the self data frame.


    def get_unique_mp3_folders(self):
        """ Get list of unique folders with mp3 files in it. """

        self.get_mp3_files_and_folders() # Ensure that this self data frame is updated.

        unique_mp3_folders = self.files_and_folders.folder.unique()
        unique_mp3_folders = list(unique_mp3_folders)

        self.unique_mp3_folders = unique_mp3_folders  # Updating the self list.


    def convert_file_extension_to_lowercase(self):
        """ Convert file extension to lowercase for all mp3's in working folder. """

        self.get_mp3_files_and_folders() # Ensure that this self data frame is updated.
        
        files = list(self.files_and_folders['file'])

        for i in range(len(files)):
            pre, ext = os.path.splitext(files[i])

            os.rename(files[i], pre + ".mp3")  # Convert each file extention into lowercase.

        self.get_mp3_files_and_folders() # Ensure that this self data frame is updated after any potential changes have been done in this function.