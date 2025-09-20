from pathlib import Path
from src import organizer

def main():
    # Pick a folder to organize (change this path for your demo)
    folder = Path("C:/Users/User/Downloads")

    print(f"📂 Scanning folder: {folder}")

    # Step 1: Propose moves
    mapping = organizer.propose_moves(folder)
    if not mapping:
        print("No files to organize.")
        return

    print("\nProposed moves:")
    for src, dst in mapping.items():
        print(f"  {src} -> {dst}")

    # Step 2: Perform moves
    print("\nOrganizing files...")
    undo_file = organizer.perform_moves(mapping)
    print(f"✅ Files organized. Undo record saved at {undo_file}")

    # Step 3: Undo last move (for demo purposes)
    print("\nUndoing last move...")
    ts, undone = organizer.undo_last_move()
    print(f"⏪ Undid moves from timestamp {ts}:")
    for dst, src in undone:
        print(f"  {dst} -> {src}")

if __name__ == "__main__":
    main()
