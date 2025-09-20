import argparse
from pathlib import Path
import src.organizer as organizer


def print_proposals(mapping):
    """Nicely display proposed moves."""
    if not mapping:
        print("No files to organize in that folder.")
        return
    print("\nProposed moves:")
    for i, (s, d) in enumerate(mapping.items(), start=1):
        print(f"{i}. {Path(s).name:25} -> {d}")
    print()


def main():
    ap = argparse.ArgumentParser(description="File Organiser Utility (MVP)")
    ap.add_argument("folder", nargs="?", default=".", help="Folder to organize (default: current dir)")
    ap.add_argument("--dry-run", action="store_true", help="Show proposed moves but do not perform them")
    ap.add_argument("--undo", action="store_true", help="Undo the last move operation")
    ap.add_argument("--yes", "-y", action="store_true", help="Auto-confirm (no prompt)")
    args = ap.parse_args()

    folder = Path(args.folder).resolve()

    # Undo mode
    if args.undo:
        try:
            ts, undone = organizer.undo_last_move()
            print(f"Undone operations from record {ts}:")
            for dst, src in undone:
                print(f"moved {dst} -> {src}")
        except Exception as e:
            print("Undo failed:", e)
        return

    # Normal organize mode
    try:
        mapping = organizer.propose_moves(folder)
    except Exception as e:
        print("Error scanning folder:", e)
        return

    print_proposals(mapping)

    if args.dry_run:
        print("Dry run complete. No files were moved.")
        return

    if not mapping:
        return

    confirm = "y" if args.yes else input("Proceed with these moves? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Aborted. No changes made.")
        return

    try:
        undo_path = organizer.perform_moves(mapping)
        print(f"Moves completed. Undo record saved to: {undo_path}")
        print("To undo last move, run: python -m src.main --undo")
    except Exception as e:
        print("Error performing moves:", e)


if __name__ == "__main__":
    main()
