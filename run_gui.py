import tkinter as tk
from tkinter import filedialog, messagebox
import organizer

def choose_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        try:
            # Step 1: propose file moves
            mapping = organizer.propose_moves(folder_selected)

            if not mapping:
                messagebox.showinfo("Info", "No files to organize.")
                return

            # Step 2: perform file moves
            undo_file = organizer.perform_moves(mapping)

            messagebox.showinfo("Success", f"Files organized!\nUndo record saved at: {undo_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

def main():
    root = tk.Tk()
    root.title("File Organizer Utility")
    root.geometry("350x200")

    label = tk.Label(root, text="Organize your files by type", font=("Arial", 12))
    label.pack(pady=15)

    button = tk.Button(root, text="Choose Folder", command=choose_folder, width=20)
    button.pack(pady=10)

    quit_button = tk.Button(root, text="Quit", command=root.quit, width=20)
    quit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

def undo_last(root):
    try:
        timestamp, undone = organizer.undo_last_move()
        if undone:
            messagebox.showinfo("Undo Success", f"Reverted {len(undone)} moves.", parent=root)
        else:
            messagebox.showinfo("Undo", "Nothing to undo.", parent=root)
    except Exception as e:
        messagebox.showerror("Undo Failed", str(e), parent=root)

def main():
    root = tk.Tk()
    root.title("File Organizer Utility")
    root.geometry("300x200")

    label = tk.Label(root, text="Organize your files by type")
    label.pack(pady=10)

    button = tk.Button(root, text="Choose Folder", command=choose_folder)
    button.pack(pady=10)

    undo_button = tk.Button(root, text="Undo Last", command=lambda: undo_last(root))
    undo_button.pack(pady=10)

    quit_button = tk.Button(root, text="Quit", command=root.quit)
    quit_button.pack(pady=10)

    root.mainloop()

