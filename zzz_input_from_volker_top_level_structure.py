from typing import (
    List,  # For specifying types input and output. Here only lists are loaded but import typing for all object types is also fine.
)


class Environment:
    def __init__(self, input_path: str = "/tmp/mp3s"):

        self._input_path = input_path  # TODO

    def get_files(self) -> List:

        return [1, 2, 3]

    def process_files(self, callback):  # A callback is for passing a function.

        files = self.get_files()

        for file in files:

            callback(file)


def string_cap(file):

    print(file + 1)


def main(env: Environment):  # Giving an environment as input.

    env.process_files(string_cap)  # This executes the process_files command and passes the string_cap function to it as an input.


if __name__ == "__main__":

    main(
        Environment(
            input_path="/tmp/mp3s",
        )
    )


# Misc. questions:
## Is there a prefered choice between " or ' for strings?
