from pathlib import Path

from file.name import MP3FileName
from file.tags import MP3FileTags


class MP3File:
    def __init__(self, filepath) -> None:
        self.tags = MP3FileTags(filepath=filepath)
        self.name = MP3FileName(filepath=filepath)


if __name__ == "__main__":

    somefile = MP3File(
        filepath=Path("data/wikimedia_commons/warnsignal_train_with_some_tags.mp3"),
    )

    print(somefile.tags.tags_id3_mutagen)
