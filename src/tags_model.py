from typing import Any, Optional

import regex
from pydantic import (
    BaseModel,
    Field,
    StrictBytes,
    conint,
    constr,
    root_validator,
    validator,
)

from beautify_single_string import StringBeautifier


class TagsImportedModel(BaseModel):
    """This Pydantic model defines the accepted tags. Any tag that is not listed below will be discarded.

    It also already does some first beautifications over the fields, defined in the validators below.
    """

    APIC: Optional[StrictBytes] = Field(alias="APIC:", description="Attached picture")
    POPM: Optional[Any] = Field(alias="POPM:no@email", description="Popularimeter. This frame keys a rating (out of 255) and a play count to an email address.")
    TPE1: Optional[constr(min_length=1)] = Field(description="Track artist")
    TPE2: Optional[constr(min_length=1)] = Field(description="Album artist. Only used as helper for TPE1.")
    TIT2: Optional[constr(min_length=1)] = Field(description="Track")
    TALB: Optional[constr(min_length=1)] = Field(description="Album")
    TDRC: Optional[conint(ge=1000)] = Field(description="Recording year")
    TDRL: Optional[conint(ge=1000)] = Field(description="Release year. Only used as helper for TDRC.")
    TPOS: Optional[conint(ge=1)] = Field(description="Disc number")
    TRCK: Optional[conint(ge=1)] = Field(description="Track Number")

    @validator("TPOS", "TRCK", pre=True)
    def extract_number_from_slash_format(cls, value):
        """Some tags not only show the current track or disc number but also add to that the total track numbers.
        E.g. '4/10' for track 4 from an album that has 10 tracks in total. This removes the '/10' from that example."""
        # TODO Do I need a skip here if these fields are None?

        value = int(regex.search(pattern=r"^[0-9]+", string=str(value))[0])  # TODO Do I really want this as Int? Or briefly as Int for deletion of any leading zeros? And then back as str as it will be filled with leading zeros later again?
        return value

    @validator("TDRC", "TDRC", pre=True)
    def extract_year(cls, value):
        """Extract only the year and omit any other information on the precise date."""
        value = int(regex.search(pattern=r"(19|20|21)\d{2}", string=str(value))[0])
        return value

    class Config:
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True  # This only refers to leading and trailing whitespace for str & byte types.


if __name__ == "__main__":

    example = {"TPE1": "   the track    artist", "TPE2": "the album artist ", "TIT2": "track", "TDRC": "01-01-2000"}

    tags = TagsImportedModel(**example)
    print(tags)
    print(tags.dict(exclude_none=True))
