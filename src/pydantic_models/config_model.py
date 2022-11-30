from pathlib import Path
from typing import List

from pydantic import BaseModel


class Config(BaseModel):
    input_path: Path
    output_path: Path
    clean_output_folder: bool
    unwanted_files: List[str]
