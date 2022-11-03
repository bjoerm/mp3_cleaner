from typing import Any, Optional

import regex
from pydantic import BaseModel, Field, StrictBytes, constr, validator


class ImportedTagsModel(BaseModel):
    """This Pydantic model defines the accepted tags. Any tag that is not listed below will be discarded."""

    APIC: Optional[StrictBytes] = Field(..., alias="APIC:", description="Attached picture")
    POPM: Optional[Any] = Field(..., alias="POPM:no@email", description="Popularimeter. This frame keys a rating (out of 255) and a play count to an email address.")
    TPE1: Optional[str] = Field(..., description="Lead Artist/Performer/Soloist/Group")
    TPE2: Optional[str] = Field(..., description="Band/Orchestra/Accompaniment")
    TIT2: Optional[str] = Field(..., description="Track")
    TALB: Optional[str] = Field(..., description="Album")
    TDRC: Optional[str] = Field(..., description="Recording year")
    TDRL: Optional[str] = Field(..., description="Release year")  # TODO This is new and shall only be used if there is no recording year. And then it shall be set as recording year. ;-)
    TPOS: Optional[int] = Field(..., description="Disc number")
    TRCK: Optional[int] = Field(..., description="Track Number")

    @validator("TPOS", "TRCK", pre=True)
    def keep_only_current_number(cls, v):
        """Some tags not only show the current track or disc number but also add to that the total track numbers.
        E.g. '4/10' for track 4 from an album that has 10 tracks in total. This removes the '/10' from that example."""
        v = int(regex.search(pattern=r"^[0-9]+", string=str(v))[0])  # TODO Do I really want this as Int? Or briefly as Int for deletion of any leading zeros? And then back as str as it will be filled with leading zeros later again?
        return v

    # TODO Build a validator to extract just the first four character long numbers in TDRC?

    class Config:
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True  # This only refers to leading and trailing whitespace for str & byte types.
