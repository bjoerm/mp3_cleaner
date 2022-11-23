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
# TODO Script should also work if input only consists of a single file that is not in a folder.
# TODO Rename (Original Motion Picture Soundtrack) into (Score).
# TODO There seems to be an error, when the track numbers in a folder can/do reach three digits (so more than 100 files). It will currently only fill one leading zero.


from datetime import datetime

import toml

from environment import DataPreparer
from tag_management import TagManager


def main():
    # Load options
    cfg = toml.load("options.toml", _dict=dict)

    # Set up environment, convert mp3 files to have a lowercase file extension and get list of mp3 files and their folder.
    files_and_folders = DataPreparer.prepare_input(
        input_path=cfg.get("input_path"),
        wip_path=cfg.get("wip_path"),
        log_path=cfg.get("log_path"),
        overwrite_previous_output=cfg.get("overwrite_previous_output"),
        unwanted_files=cfg.get("unwanted_files"),
    )

    # Improve the MP3 ID3 tags in the specified folder(s).
    TagManager.improve_tags(
        selected_id3_fields=cfg.get("selected_id3_fields"),
        files_and_folders=files_and_folders,
        suffix_keywords=cfg.get("suffix_keywords"),
    )


if __name__ == "__main__":
    start_time = datetime.now()
    print(f'Script started at {start_time.strftime("%H:%M:%S")}.')

    main()

    finish_time = datetime.now()
    print(f'Script finished at {finish_time.strftime("%H:%M:%S")}.\nTook {int((finish_time - start_time).total_seconds())} seconds.')
