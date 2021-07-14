# TODO Add functionality that prevents folder renames in cases when there are files with tags and without at the same time. As of now cases with not tags are just dropped and are thus overlooked in later checks for Nones (in the rename folder part for example).
# TODO Instead of having a single session log. Maybe have a global .parquet log file that is expanded after each run.
# TODO Think about converting "cd strings" (like "cd1") from the path into disc number tags. That would help the file beautification and recude manual work. But might be bad in case where "cd" is not referring to a cd number.
# TODO Finish tests about filenames (and foldernames).
# TODO Have option to switch renaming files on and off. Also a switch for folders. And for album art tags.
# TODO Add case to "_check_obsolescence_of_album_artist" where album artist is "VA" or similar. Or simply delete album artist whenever there is a track artist.
# TODO _deal_with_special_words_and_bands should create brackets, so it should make "Artist - Title Live" to "Artist - Title (Live)". Same for "Remix" and "Feat.". This will be a bit complicated for cases like "Live in London", "Remix by" and of course "Feat.".
# TODO If disc number is 1/1 remove it.
# TODO Does not need to write the disc number to the folder name, if there are multiple disc names within the same folder. Currently it write CD1 there.
# TODO It seems like file names are not beautified, if the first or first x entries are already in the desired beautified format. This is problematic, if later entries are not beautified yet.


from datetime import datetime
import toml

from tag_management import TagManager
from environment import DataPreparer


def main():
    # Load options
    cfg = toml.load("options.toml", _dict=dict)

    # Set up environment, convert mp3 files to have a lowercase file extension and get list of mp3 files and their folder.
    files_and_folders = DataPreparer.prepare_input(input_path=cfg.get("input_path"), wip_path=cfg.get("wip_path"), log_path=cfg.get("log_path"), overwrite_previous_output=cfg.get("overwrite_previous_output"), unwanted_files=cfg.get("unwanted_files"))

    # Improve the MP3 ID3 tags in the specified folder(s).
    TagManager.improve_tags(selected_id3_fields=cfg.get("selected_id3_fields"), files_and_folders=files_and_folders, suffix_keywords=cfg.get("suffix_keywords"))


if __name__ == "__main__":
    main()

    print(f'Script finished at {datetime.now().strftime("%H:%M:%S")}')
