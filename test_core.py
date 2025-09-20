import os
from src.main import scan_folder, organize_files, undo_moves
#imports the functions to test from the main(scan_folder, organize_files, undo_moves).


def test_propose_moves(tmp_path): #defines a test function for pytest, using a temporary path provided by pytest(tmp_path).
    f1 = tmp_path / "a.txt"  #Creates two temporary files in tmp_path: a text file and an image file.
    f1.write_text("hello") #writes "hello" to the text file.
    f2 = tmp_path / "b.jpg"
    f2.write_text("img")
 #they simulate files to be organized


    mapping = scan_folder(tmp_path) #mapping will be a dictionary categorizing the files in tmp_path(ex:{"Documents": ["a.txt"], "Images": ["b.jpg"]}).

    assert "Documents" in mapping
    assert "Images" in mapping
    assert "a.txt" in mapping["Documents"]
    assert "b.jpg" in mapping["Images"]
#these are assertions to check if the scan_folder worked correctly, if any fail the test fails(AssertionError).



def test_perform_and_undo(tmp_path): #this checks if files are moved correctly and can be undone.
    f1 = tmp_path / "note.txt"
    f1.write_text("x")
    f2 = tmp_path / "pic.png"
    f2.write_text("y")
    #creates two files, a text file and an image file, in the temporary dictionary.

    mapping = scan_folder(tmp_path) #scans the tmp_path and categorizes the files.
    history = organize_files(tmp_path, mapping) #moves files into their category and records the moves in history.
    #links directly to the organize_files function in the main file.


    moved_targets = list((tmp_path / "Documents").glob("*"))
    moved_images = list((tmp_path / "Images").glob("*"))
    #checks the contents of the new subfolders after moving the files.
    #.glob("*")) lists all files in the subfolder.

    assert any("note" in str(p) for p in moved_targets)
    assert any("pic" in str(p) for p in moved_images)
    #assertions to verify the files were moved correctly

    undo_moves(history)
    #calls the undo_moves from the main file and reverts the move using the history.


    assert (tmp_path / "note.txt").exists()
    assert (tmp_path / "pic.png").exists()
    #checks if the files are back in their original location, confirming the undo worked.