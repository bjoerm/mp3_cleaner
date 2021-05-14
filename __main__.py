# TODO Add functionality that prevents folder renames in cases when there are files with tags and without at the same time. As of now cases with not tags are just dropped and are thus overlooked in later checks for Nones (in the rename folder part for example).

# TODO Instead of having a single session log. Maybe have a global .parquet log file that is expanded after each run.
# TODO Think about having a logic that moves informations on Feat. from the artist to the title.
# TODO Think about converting "cd strings" (like "cd1") from the path into disc number tags. That would help the file beautification and recude manual work. But might be bad in case where this is not a cd number.
# TODO Finish tests about filenames (and foldernames).
# TODO Have option to switch renaming files on and off. Also a switch for folders.

import toml

from tag_management import TagManager
from environment import DataPreparer


def main():
    # Load options
    cfg = toml.load("options.toml", _dict=dict)

    files_and_folders = DataPreparer.prepare_input(input_path=cfg.get("input_path"), wip_path=cfg.get("wip_path"), log_path=cfg.get("log_path"), overwrite_previous_output=cfg.get("overwrite_previous_output"), unwanted_files=cfg.get("unwanted_files"))

    # # Set up environment, convert mp3 files to have a lowercase file extension and get list of mp3 files and their folder.
    # env = Environment(input_path=cfg.get("input_path"), wip_path=cfg.get("wip_path"))

    # Improve the MP3 ID3 tags in the specified folder(s).
    TagManager.improve_tags(selected_id3_fields=cfg.get("selected_id3_fields"), files_and_folders=files_and_folders)


if __name__ == "__main__":
    main()

    print("Script finished")
