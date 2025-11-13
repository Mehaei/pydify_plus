import os
from typing import IO, Any, Dict, List, Tuple, Union

def prepare_files_for_httpx(file_path: str) -> Dict[str, Tuple[str, IO[bytes], str]]:
    """Prepare a file for uploading with httpx."""
    file_name = os.path.basename(file_path)
    return {"file": (file_name, open(file_path, "rb"), "application/octet-stream")}