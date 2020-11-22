# TODO Add log files with tags prior and after change.
# TODO Add progress in percent calculated based on the share of finished folders.

# Restore # TODO The following part needs to be restored! Checking the file path for a "cd xy" string. in beautify_tags.py

import toml

from environment import Environment
from tag_management import ProcessMp3



def main():
    # Get options
    cfg = toml.load("options.toml", _dict=dict)

    # TODO cfg.get("selected_id3_fields")    

    # Set up environment, convert them to lowercase file extension and get list of mp3 files and their folder.
    env = Environment(input_path=cfg.get("input_path"), wip_path=cfg.get("wip_path"))

    tags = ProcessMp3(selected_id3_fields=cfg.get("selected_id3_fields"), files_and_folders=env.files_and_folders)
    
    tags.improve_tags()


    # print(env.files_and_folders)

if __name__ == "__main__":
    main()

    print("Finished")