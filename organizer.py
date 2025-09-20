from pathlib import Path
import shutil
import json
import time
from typing import Dict, List, Tuple

# Map extensions (lowercase) to category folders
EXT_TO_CAT = {
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
    ".bmp": "Images", ".svg": "Images", ".webp": "Images",
    # Audio
    ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio", ".aac": "Audio",
    # Video
    ".mp4": "Videos", ".mkv": "Videos", ".mov": "Videos", ".avi": "Videos",
    # Docs
    ".pdf": "Documents", ".docx": "Documents", ".doc": "Documents",
    ".txt": "Documents", ".pptx": "Documents", ".xlsx": "Documents",
    # Archives
    ".zip": "Archives", ".tar": "Archives", ".gz": "Archives", ".rar": "Archives",
}

DEFAULT_CATEGORY = "Others"
HISTORY_DIR_NAME = ".history"


def scan_directory(folder: Path) -> List[Path]:
    """Return a list of files directly inside folder (non-recursive)."""
    folder = Path(folder)
    if not folder.exists() or not folder.is_dir():
        raise NotADirectoryError(f"{folder} is not a directory")
    return [p for p in folder.iterdir() if p.is_file()]


def categorize_by_extension(file_path: Path) -> str:
    """Return category name for the file based on its extension."""
    return EXT_TO_CAT.get(file_path.suffix.lower(), DEFAULT_CATEGORY)


def propose_moves(folder: Path) -> Dict[str, str]:
    """
    Build a mapping: source_path_str -> proposed_target_path_str.
    Does not create directories or move files.
    """
    folder = Path(folder)
    mapping: Dict[str, str] = {}
    for file in scan_directory(folder):
        category = categorize_by_extension(file)
        target_dir = folder / category
        target = target_dir / file.name

        # Skip if already in the correct place
        try:
            if file.resolve() == target.resolve():
                continue
        except Exception:
            pass

        mapping[str(file)] = str(target)
    return mapping


def _resolve_collision(dst: Path) -> Path:
    """If dst exists, add ' (1)', ' (2)' etc. until unique."""
    dst = Path(dst)
    if not dst.exists():
        return dst
    parent, stem, suffix = dst.parent, dst.stem, dst.suffix
    counter = 1
    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def perform_moves(mapping: Dict[str, str], history_dir: Path = None) -> Path:
    """
    Execute the moves described in mapping (src->dst).
    Returns path to saved undo-record JSON file.
    """
    # Always store undo records inside a `.history` folder
    history_dir = Path(history_dir) if history_dir else Path(HISTORY_DIR_NAME)
    history_dir.mkdir(parents=True, exist_ok=True)

    operations = []
    for src_str, dst_str in mapping.items():
        src, dst = Path(src_str), Path(dst_str)
        dst.parent.mkdir(parents=True, exist_ok=True)

        final_dst = _resolve_collision(dst)
        try:
            shutil.move(str(src), str(final_dst))
            operations.append({"src": str(src), "dst": str(final_dst)})
        except Exception as e:
            operations.append({"src": str(src), "dst": str(final_dst), "error": str(e)})

    timestamp = int(time.time())
    undo_path = history_dir / f"undo-{timestamp}.json"
    with open(undo_path, "w", encoding="utf-8") as fh:
        json.dump({"timestamp": timestamp, "operations": operations}, fh, indent=2)

    return undo_path


def _latest_undo_file(history_dir: Path) -> Path:
    history_dir = Path(history_dir)
    if not history_dir.exists():
        raise FileNotFoundError("No history directory found")
    files = sorted([p for p in history_dir.iterdir()
                    if p.name.startswith("undo-") and p.suffix == ".json"])
    if not files:
        raise FileNotFoundError("No undo records found")
    return files[-1]


def undo_last_move(history_dir: Path = Path(HISTORY_DIR_NAME)) -> Tuple[int, List[Tuple[str, str]]]:
    """
    Undo the last recorded move.
    Returns (timestamp, list of (dst, src) moved back).
    NOTE: If the original filename already exists, a suffix like ' (1)' will be added.
    """
    undo_file = _latest_undo_file(history_dir)
    with open(undo_file, "r", encoding="utf-8") as fh:
        record = json.load(fh)

    undone = []
    for op in reversed(record.get("operations", [])):
        src, dst = Path(op.get("src")), Path(op.get("dst"))
        if dst.exists():
            src.parent.mkdir(parents=True, exist_ok=True)
            final_src = _resolve_collision(src)
            try:
                shutil.move(str(dst), str(final_src))
                undone.append((str(dst), str(final_src)))
            except Exception:
                continue

    return record.get("timestamp", 0), undone

def organize_files(folder: str):
    """High-level function to organize files in a folder."""
    from pathlib import Path
    folder_path = Path(folder)

    # Step 1: Propose moves
    mapping = propose_moves(folder_path)

    # Step 2: Perform moves
    undo_file = perform_moves(mapping)

    return undo_file
