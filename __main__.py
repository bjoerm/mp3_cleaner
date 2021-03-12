# TODO Instead of having a single session log. Maybe have a global .parquet log file that is expanded after each run.
# TODO Think about having a logic that moves informations on Feat. from the artist to the title.
# TODO Think about converting "cd strings" (like "cd1") from the path into disc number tags. That would help the file beautification and recude manual work. But might be bad in case where this is not a cd number.
# TODO Finish tests about filenames.
# TODO Think about keeping the tag with the album art (or at least have an option to activate and deactivate that one).
# TODO Have option to switch renaming files on and off. Also a switch for folders.
# TODO Think about option to throw away certain file types (e.g. .exe, .nfo, .txt, .url, .DS_Store, ...) to keep the folders clean.

import toml

from environment import Environment
from tag_management import TagManager


def main():
    # Load options
    cfg = toml.load("options.toml", _dict=dict)

    # Set up environment, convert mp3 files to have a lowercase file extension and get list of mp3 files and their folder.
    env = Environment(input_path=cfg.get("input_path"), wip_path=cfg.get("wip_path"))

    # Improve the MP3 ID3 tags in the specified folder(s).
    TagManager.improve_tags(selected_id3_fields=cfg.get("selected_id3_fields"), files_and_folders=env.files_and_folders)


if __name__ == "__main__":
    main()

    print("Script finished")
