

# import re  # Regular expressions
# import time
# import typing
import toml

from Environment import Environment





def main():
    # Get options
    cfg = toml.load("options.toml", _dict=dict)

    # TODO cfg.get('selected_id3_fields')

    # Set up environment, convert them to lowercase file extension and get list of mp3 files.
    env = Environment(input_path="untouched_input", wip_path="input")

    print(env.files_and_folders)




if __name__ == "__main__":
    main()

