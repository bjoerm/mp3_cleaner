import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
from mutagen.id3 import APIC, ID3, POPM, TALB, TDRC, TIT2, TPE1, TPE2, TPOS, TRCK
from mutagen.mp3 import MP3  # Alternative to ID3 and ID3NoHeaderError.
from pydantic import BaseModel, Field, conint, constr
from tqdm import trange

from beautify_filepaths import FileBeautifier
from beautify_multiple_tags import TagBeautifier


class AcceptedID3Tags(BaseModel):
    APIC: Optional[str] = Field(alias="APIC:", description="Attached (or linked) picture")  # TODO Which would be the correct type for this field?
    POPM: Optional[str] = Field(description="Popularimeter. This frame keys a rating (out of 255) and a play count to an email address.")
    TALB: Optional[str] = Field(description="Album name")
    TDRC: Optional[str] = Field(description="Recording time")  # TODO Think about whether mutagen.id3.TDRL (release time) shouldn't also be checked.
    TIT2: Optional[str] = Field(description="Track name")
    TPE1: Optional[str] = Field(description="Lead Artist/Performer/Soloist/Group")
    TPE2: Optional[str] = Field(description="Band/Orchestra/Accompaniment")
    TPOS: Optional[conint(regex=r"^[0-9]+")] = Field(description="Part of set. Example: Disc number.")
    TRCK: Optional[constr(regex=r"^[0-9]+")] = Field(description="Track Number")

    class Config:
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True  # This only refers to leading and trailing whitespace for str & byte types.


class FileModel(BaseModel):
    selected_id3_tags: AcceptedID3Tags


class File:
    # Grobe Idee:
    # Eine Folder Klasse übergibt beim Instanzieren der File Klasse das Feld filepath (zu der File) an diese Klasse.
    # Die File Klasse liest dann alle Tags der File ein, filtert nur auf gesuchte Tags, konvertiert diese in ein Dictionary, validiert (und normiert) dieses Dict anschließend via Pydantic. Die folgenden Beautifications sollten dann wieder auf Folderebene passieren, da File-übergreifende Infos in manchen Fällen benötigt werden.

    def __init__(self, filepath: Path, accepted_tags: List[str]):
        self.filepath = filepath
        self.accepted_tags = accepted_tags
        self.tags_imported = self.import_tags_as_dict()  # TODO Hier auf die Main-Method verweisen, welche den obigen groben Ablauf abbildet.

    def import_tags_as_dict(self):
        tags_imported = self._import_id3_tag_from_file()
        tags_imported = self._keep_only_accepted_tags(tags_imported)
        tags_imported = self._extract_imported_text_tags(tags_imported)
        self._normalize_and_validate_imported_tags(tags_imported)

        return tags_imported

    def _import_id3_tag_from_file(self) -> ID3:
        """Import all ID3 tags from the MP3 file."""
        # TODO Add handling of files without tags.
        return ID3(self.filepath)

    def _keep_only_accepted_tags(self, tags_imported: ID3) -> Dict[str, APIC | POPM | TALB | TDRC | TIT2 | TPE1 | TPE2 | TPOS | TRCK]:
        """Keeping only the defined accepted tags."""
        return {k: v for (k, v) in tags_imported.items() if k in self.accepted_tags}  # TODO I could even get rid of this method and only do this in the Pydantic check with the exclude / include settings.

    def _extract_imported_text_tags(self, tags_imported: Dict[str, APIC | POPM | TALB | TDRC | TIT2 | TPE1 | TPE2 | TPOS | TRCK]) -> Dict[str, str | APIC | POPM]:
        """Converting all tags that have the attribute 'text' as strings and thus removing other attributes like the enconding attributes."""

        tags_imported: Dict[str, str | APIC | POPM] = dict((k, tags_imported[k].text[0] if hasattr(tags_imported[k], "text") else tags_imported[k]) for k in tags_imported)

        for k in tags_imported:
            if hasattr(tags_imported[k], "text"):
                tags_imported[k] = tags_imported[k].text[0]  # TODO How to solve this type hinting warning?

        return tags_imported

    def _normalize_and_validate_imported_tags(self, tags_imported: Dict[str, str | APIC | POPM]):
        # TODO Via pydantic
        AcceptedID3Tags(**tags_imported)
        pass

    def export_tags_in_file(self):
        # TODO A second public method that is used for writing output to files.
        pass

    def _validate_tags_prior_update(self):
        # TODO Via Pydantic it should be checked whether the output is still according to the desired form. This could theoretically also be done on the folder level instead using root_validators.
        pass

    def _write_beautified_tag_to_files(self):
        pass


if __name__ == "__main__":
    File(
        filepath=Path("input/aaaaaaaMP3/01. This Is The Beginning.mp3"),
        accepted_tags=[
            "APIC:",
            "POPM:no@email",
            "TALB",
            "TDRC",
            "TIT2",
            "TPE1",
            "TPE2",
            "TPOS",
            "TRCK",
        ],
    )
