from pathlib import Path

from pydantic import BaseModel, DirectoryPath, StrictBool


class Config(BaseModel):
    input_path: DirectoryPath
    output_path: Path
    do_clean_output_folder: StrictBool
    unwanted_files: list[str]

    class Config:
        extra = "forbid"
