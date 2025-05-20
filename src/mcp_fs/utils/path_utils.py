import os
from pathlib import Path
from typing import List


def expand_path(path: str | Path) -> Path:
    if isinstance(path, Path):
        path = str(path)
    expanded = os.path.expandvars(path)
    return Path(expanded).resolve()


def is_path_allowed(path: str | Path, allowed_dirs: List[Path]) -> bool:
    resolved_path = expand_path(path)
    
    for allowed_dir in allowed_dirs:
        allowed_path = expand_path(allowed_dir)
        try:
            if resolved_path == allowed_path or allowed_path in resolved_path.parents:
                return True       
        except (ValueError, OSError):
            continue

    return False

def validate_path(path: str | Path, allowed_dirs: List[Path]) -> Path:
    resolved_path = expand_path(path)

    if not is_path_allowed(resolved_path, allowed_dirs):
        raise ValueError(f"Path {resolved_path} is not allowed. Allowed directories are: {allowed_dirs}")
    return resolved_path
            