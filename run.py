import organizer

if __name__ == "__main__":
    folder = input("Enter the path to the folder you want to organize: ").strip()
    mapping = organizer.propose_moves(folder)
    print("Proposed moves:")
    for src, dst in mapping.items():
        print(f"{src} -> {dst}")

    confirm = input("Proceed with moves? (y/n): ").lower()
    if confirm == "y":
        undo_file = organizer.perform_moves(mapping)
        print(f"Files moved! Undo file saved at {undo_file}")
    else:
        print("No changes made.")
