# TODO Add log files with tags prior and after change.
# TODO Add progress in percent calculated based on the share of finished folders.

import toml

from environment import Environment
from tag_management import TagManager



def main():
    # Get options
    cfg = toml.load("options.toml", _dict=dict)

    # TODO cfg.get("selected_id3_fields")    

    # Set up environment, convert them to lowercase file extension and get list of mp3 files and their folder.
    env = Environment(input_path=cfg.get("input_path"), wip_path=cfg.get("wip_path"))

    # Improve the MP3 ID3 tags in the specified folder(s).
    # tags = TagManager(selected_id3_fields=cfg.get("selected_id3_fields"), files_and_folders=env.files_and_folders)
    
    TagManager.improve_tags(selected_id3_fields=cfg.get("selected_id3_fields"), files_and_folders=env.files_and_folders)


if __name__ == "__main__":
    main()

    print("Script finished")