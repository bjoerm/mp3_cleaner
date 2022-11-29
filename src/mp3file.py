from pathlib import Path

from mp3filename import MP3FileName
from mp3filetags import MP3FileTags


class MP3File:
    def __init__(self, filepath) -> None:
        self.tags = MP3FileTags(filepath=filepath)
        self.name = MP3FileName(filepath=filepath)


if __name__ == "__main__":

    abc = MP3File(
        filepath=Path("data/wikimedia_commons/warnsignal_train_with_some_tags.mp3"),
    )

    print(abc.tags.tags_id3_mutagen)

    pass
