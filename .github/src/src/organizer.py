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
    ext = file_path.suffix.lower()
    return EXT_TO_CAT.get(ext, DEFAULT_CATEGORY)


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
        # If source is already the proposed target, skip mapping
        try:
            if file.resolve() == target.resolve():
                continue
        except Exception:
            # on weird filesystems, just proceed
            pass
        mapping[str(file)] = str(target)
    return mapping


def _resolve_collision(dst: Path) -> Path:
    """If dst exists, add ' (1)', ' (2)' before extension until unique."""
    dst = Path(dst)
    if not dst.exists():
        return dst
    parent = dst.parent
    stem = dst.stem
    suffix = dst.suffix
    counter = 1
    while True:
        new_name = f"{stem} ({counter}){suffix}"
        candidate = parent / new_name
        if not candidate.exists():
            return candidate
        counter += 1


def perform_moves(mapping: Dict[str, str], history_dir: Path = None) -> Path:
    """
    Execute the moves described in mapping (src->dst).
    Returns path to saved undo-record JSON file.
    """
    if history_dir is None:
        history_dir = Path(mapping and list(mapping.values())[0]).parents[len(str(Path('.').resolve()).split('/'))]  # fallback
    history_dir = Path(history_dir) if history_dir else Path(HISTORY_DIR_NAME)
    history_dir.mkdir(parents=True, exist_ok=True)

    operations = []
    for src_str, dst_str in mapping.items():
        src = Path(src_str)
        dst = Path(dst_str)
        # create destination dir
        dst.parent.mkdir(parents=True, exist_ok=True)
        # resolve collision
        final_dst = _resolve_collision(dst)
        try:
            shutil.move(str(src), str(final_dst))
            operations.append({"src": str(src), "dst": str(final_dst)})
        except Exception as e:
            # record the failure as an operation with error
            operations.append({"src": str(src), "dst": str(final_dst), "error": str(e)})

    timestamp = int(time.time())
    undo_path = history_dir / f"undo-{timestamp}.json"
    record = {"timestamp": timestamp, "operations": operations}
    with open(undo_path, "w", encoding="utf-8") as fh:
        json.dump(record, fh, indent=2)
    return undo_path


def _latest_undo_file(history_dir: Path) -> Path:
    history_dir = Path(history_dir)
    if not history_dir.exists():
        raise FileNotFoundError("No history directory found")
    files = sorted([p for p in history_dir.iterdir() if p.name.startswith("undo-") and p.suffix == ".json"])
    if not files:
        raise FileNotFoundError("No undo records found")
    return files[-1]


def undo_last_move(history_dir: Path = Path(HISTORY_DIR_NAME)) -> Tuple[int, List[Tuple[str, str]]]:
    """
    Undo the last recorded move. Returns (timestamp, list of (dst,src) moved back).
    Raises if no history exists.
    """
    history_dir = Path(history_dir)
    undo_file = _latest_undo_file(history_dir)
    with open(undo_file, "r", encoding="utf-8") as fh:
        record = json.load(fh)
    ops = record.get("operations", [])
    undone = []
    # reverse the operations to move files back in reverse order
    for op in reversed(ops):
        src = Path(op.get("src"))
        dst = Path(op.get("dst"))
        # if dst (current location) exists, move it back to src
        if dst.exists():
            src.parent.mkdir(parents=True, exist_ok=True)
            final_src = _resolve_collision(src)
            try:
                shutil.move(str(dst), str(final_src))
                undone.append((str(dst), str(final_src)))
            except Exception:
                # skip problematic file
                continue
    return record.get("timestamp", 0), undone
