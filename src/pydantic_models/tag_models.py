from typing import Optional

import regex
from pydantic import BaseModel, Field, StrictBytes, StrictStr, conint, constr, validator


class APICModel(BaseModel):
    """Defines the content of the APIC."""

    mime: StrictStr  # Not (yet?) optional as it should always be present alongside data.
    data: StrictBytes


class TagsImportModel(BaseModel):
    """This Pydantic model defines the accepted tags. Any tag that is not listed below will be discarded.

    It also already does some first beautifications over the fields, defined in the validators below.
    """

    APIC: Optional[APICModel] = Field(alias="APIC:", description="Attached picture")
    POPM: Optional[conint(ge=0, le=255)] = Field(alias="POPM:no@email", description="Popularimeter. This frame keys a rating (out of 255). The playcount that can be in POPM is omitted.")
    TALB: Optional[constr(min_length=1)] = Field(description="Album")
    TDRC: Optional[conint(ge=1000)] = Field(description="Recording year")
    TDRL: Optional[conint(ge=1000)] = Field(description="Release year. Only used as helper for TDRC.")
    TIT2: Optional[constr(min_length=1)] = Field(description="Track")
    TPE1: Optional[constr(min_length=1)] = Field(description="Track artist")
    TPE2: Optional[constr(min_length=1)] = Field(description="Album artist. Only used as helper for TPE1.")
    TPOS: Optional[conint(ge=1)] = Field(description="Disc number")
    TRCK: Optional[conint(ge=1)] = Field(description="Track Number")

    @validator("TPOS", "TRCK", pre=True)
    def extract_number_from_slash_format(cls, value) -> int:
        """Some tags not only show the current track or disc number but also add to that the total track numbers.
        E.g. '4/10' for track 4 from an album that has 10 tracks in total. This removes the '/10' from that example."""

        if value is None:
            return value
        else:
            value = str(value)
            if value[0] == "/":  # Some oddly formatted tags can start with a slash.
                value = value[1:]

            value = int(regex.search(pattern=r"^[0-9]+", string=value)[0])

        return value

    @validator("TDRC", "TDRL", pre=True)
    def extract_year(cls, value):
        """Extract only the year and omit any other information on the precise date."""
        if value is None:
            return value
        else:
            value = regex.search(pattern=r"(18|19|20)\d{2}", string=str(value))  # This is a bit stricter than just \d{4}.

        if value is None:
            return None

        else:
            return int(value[0])  # The first found term.

    @validator("TALB", pre=True)
    def unify_score_suffix(cls, value):
        if value is None:
            return value
        else:
            value = value.replace("(Original Motion Picture Score)", "(Score)")
            value = value.replace("(O.S.T.)", "(Soundtrack)")
            return value

    class Config:
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True  # This only refers to leading and trailing whitespace for str & byte types.


class TagsExportModel(BaseModel):
    """Tags how they shall be exported.
    Compared to the imported tags Pydantic model:
    - Helper tags like album artist are no longer present.
    - Some tags are now mandatory.
    - Minor type changes.
    """

    TPE1: constr(min_length=1) = Field(description="Track artist")
    TIT2: constr(min_length=1) = Field(description="Track")
    APIC: Optional[APICModel] = Field(description="Attached picture")
    POPM: Optional[conint(ge=0, le=255)] = Field(description="Popularimeter. Rating from 0 to 255.")
    TALB: Optional[constr(min_length=1)] = Field(description="Album")
    TDRC: Optional[constr(min_length=4, max_length=4)] = Field(description="Recording year")
    TPOS: Optional[constr(min_length=1)] = Field(description="Disc number")
    TRCK: Optional[constr(min_length=1)] = Field(description="Track Number")

    class Config:
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True  # This only refers to leading and trailing whitespace for str & byte types.
        extra = "forbid"


if __name__ == "__main__":

    example = {"TPE1": "   the track    artist", "TPE2": " the album artist ", "TIT2": "track", "TDRC": "01-01-2000"}

    tags_import = TagsImportModel(**example)
    print(tags_import)

    tags_export = TagsExportModel(**tags_import.dict(exclude_none=True))
    print(tags_export.dict(exclude_none=True))
