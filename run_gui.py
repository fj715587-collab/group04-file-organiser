import tkinter as tk
from tkinter import filedialog, messagebox
import organizer  # import your file organizer module

def choose_folder():
    # Let user pick a folder
    folder = filedialog.askdirectory()
    if folder:
        try:
            organizer.organize_files(folder)  # call your organizer function
            messagebox.showinfo("Success", f"Files in '{folder}' have been organized!")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

# Create main window
root = tk.Tk()
root.title("File Organizer")
root.geometry("400x200")

# Add button
btn = tk.Button(root, text="Choose Folder to Organize", command=choose_folder, padx=20, pady=10)
btn.pack(expand=True)

# Run the app
root.mainloop()
