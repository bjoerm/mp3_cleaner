# TODO Instead of having a session log. Maybe have a global .parquet log file that is expanded after each run.
# TODO Think about having a logic that moves informations on Feat. from the artist to the title. But might be a bit complicated if there are more suffixes, like (Live) or (Remix).
# TODO Think about converting "cd strings" (like "cd1") from the path into disc number tags. That would help the file beautification and recude manual work.
# TODO Switch each "return(x)"" into "return x".
# TODO Finish tests about filenames.


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
