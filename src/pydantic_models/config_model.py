from pathlib import Path
from typing import Optional

from pydantic import BaseModel, DirectoryPath, StrictBool


class Config(BaseModel):
    input_path: DirectoryPath
    output_path: Path
    threads: int
    do_clean_output_folder: StrictBool
    unwanted_files: list[str]

    class Config:
        extra = "forbid"
