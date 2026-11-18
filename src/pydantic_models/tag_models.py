from typing import Optional

import regex
from pydantic import BaseModel, ConfigDict, Field, StrictBytes, StrictStr, conint, constr, field_validator, validator


class APICModel(BaseModel):
    """Defines the content of the APIC."""

    mime: StrictStr  # Not (yet?) optional as it should always be present alongside data.
    data: StrictBytes


class TagsImportModel(BaseModel):
    """This Pydantic model defines the accepted tags. Any tag that is not listed below will be discarded.

    It also already does some first beautifications over the fields, defined in the validators below.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    APIC: APICModel | None = Field(
        default=None,
        alias="APIC:",
        description="Attached picture",
    )
    POPM: int | None = Field(
        default=None,
        alias="POPM:no@email",
        ge=0,
        le=255,
        description="Popularimeter. This frame keys a rating (out of 255). The playcount that can be in POPM is omitted.",
    )
    TALB: str | None = Field(
        default=None,
        min_length=1,
        description="Album",
    )
    TDRC: int | None = Field(
        default=None,
        ge=1000,
        description="Recording year",
    )
    TDRL: int | None = Field(
        default=None,
        ge=1000,
        description="Release year. Only used as helper for TDRC.",
    )
    TIT2: str | None = Field(
        default=None,
        min_length=1,
        description="Track",
    )
    TPE1: str | None = Field(
        default=None,
        min_length=1,
        description="Track artist",
    )
    TPE2: str | None = Field(
        default=None,
        min_length=1,
        description="Album artist. Only used as helper for TPE1.",
    )
    TPOS: int | None = Field(
        default=None,
        ge=1,
        description="Disc number",
    )
    TRCK: int | None = Field(
        default=None,
        ge=1,
        description="Track Number",
    )

    @field_validator("TPOS", "TRCK", mode="before")
    @classmethod
    def extract_number_from_slash_format(cls, value):
        """Extract the current track or disc number from slash format, e.g. '4/10'."""

        if value is None:
            return value

        value = str(value)

        if value[0] == "/":
            value = value[1:]

        value = int(regex.search(pattern=r"^[0-9]+", string=value)[0])

        return value

    @field_validator("TDRC", "TDRL", mode="before")
    @classmethod
    def extract_year(cls, value):
        """Extract only the year and omit any other information on the precise date."""

        if value is None:
            return value

        value = regex.search(
            pattern=r"(18|19|20)\d{2}",
            string=str(value),
        )

        if value is None:
            return None

        return int(value[0])

    @field_validator("TALB", mode="before")
    @classmethod
    def unify_score_suffix(cls, value):
        if value is None:
            return value

        value = value.replace(
            "(Original Motion Picture Score)",
            "(Score)",
        )
        value = value.replace(
            "(O.S.T.)",
            "(Soundtrack)",
        )

        return value


from pydantic import BaseModel, ConfigDict, Field


class TagsExportModel(BaseModel):
    """Tags how they shall be exported.
    Compared to the imported tags Pydantic model:
    - Helper tags like album artist are no longer present.
    - Some tags are now mandatory.
    - Minor type changes.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        coerce_numbers_to_str=True,
        extra="forbid",
    )

    TPE1: str = Field(
        min_length=1,
        description="Track artist",
    )
    TIT2: str = Field(
        min_length=1,
        description="Track",
    )
    APIC: APICModel | None = Field(
        default=None,
        description="Attached picture",
    )
    POPM: int | None = Field(
        default=None,
        ge=0,
        le=255,
        description="Popularimeter. Rating from 0 to 255.",
    )
    TALB: str | None = Field(
        default=None,
        min_length=1,
        description="Album",
    )
    TDRC: str | None = Field(
        default=None,
        min_length=4,
        max_length=4,
        description="Recording year",
    )
    TPOS: str | None = Field(
        default=None,
        min_length=1,
        description="Disc number",
    )
    TRCK: str | None = Field(
        default=None,
        min_length=1,
        description="Track Number",
    )
