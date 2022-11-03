from typing import Any, Optional

import regex
from pydantic import BaseModel, Field, StrictBytes, constr, validator

# TODO Should I always use constr to ensure a minimal string length of 1 to prevent cases of strings that are just ""?


class ImportedTagsModel(BaseModel):
    """This Pydantic model defines the accepted tags. Any tag that is not listed below will be discarded."""

    APIC: Optional[StrictBytes] = Field(alias="APIC:", description="Attached picture")
    POPM: Optional[Any] = Field(alias="POPM:no@email", description="Popularimeter. This frame keys a rating (out of 255) and a play count to an email address.")
    TPE1: Optional[str] = Field(description="Track artist")
    TPE2: Optional[str] = Field(description="Album artist")
    TIT2: Optional[str] = Field(description="Track")
    TALB: Optional[str] = Field(description="Album")
    TDRC: Optional[int] = Field(description="Recording year")
    TDRL: Optional[int] = Field(description="Release year")  # TODO This is new and shall only be used if there is no recording year. And then it shall be set as recording year. ;-)
    TPOS: Optional[int] = Field(description="Disc number")
    TRCK: Optional[int] = Field(description="Track Number")

    @validator("TPOS", "TRCK", pre=True)
    def extract_number_from_slash_format(cls, v):
        """Some tags not only show the current track or disc number but also add to that the total track numbers.
        E.g. '4/10' for track 4 from an album that has 10 tracks in total. This removes the '/10' from that example."""
        # TODO Do I need a skip here if these fields are None?

        v = int(regex.search(pattern=r"^[0-9]+", string=str(v))[0])  # TODO Do I really want this as Int? Or briefly as Int for deletion of any leading zeros? And then back as str as it will be filled with leading zeros later again?
        return v

    @validator("TDRC", "TDRC", pre=True)
    def extract_year(cls, v):
        """Extract only the year and omit any other information on the precise date."""
        v = int(regex.search(pattern=r"(19|20|21)\d{2}", string=str(v))[0])
        return v

    # TODO Build a validator to extract just the first four character long numbers in TDRC?

    class Config:
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True  # This only refers to leading and trailing whitespace for str & byte types.


if __name__ == "__main__":

    example = {"TPE1": " track    artist", "TPE2": "album artist ", "TIT2": "track", "TDRC": "01-01-2000"}

    tags = ImportedTagsModel(**example)
    print(tags)
    print(tags.dict(exclude_none=True))
