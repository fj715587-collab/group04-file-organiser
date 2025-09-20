import os
from src.main import scan_directory, propose_moves, perform_moves, undo_last_move

#imports the functions to test from the main(scan_directory,propose_move, perform_moves, undo_last_move).


def test_propose_moves(tmp_path): #defines a test function for pytest, using a temporary path provided by pytest(tmp_path).
    f1 = tmp_path / "a.txt"  #Creates two temporary files in tmp_path: a text file and an image file.
    f1.write_text("hello") #writes "hello" to the text file.
    f2 = tmp_path / "b.jpg"
    f2.write_text("img")

 #they simulate files to be organized


    mapping = propose_moves(tmp_path) #mapping will be a dictionary categorizing the files in tmp_path(ex:{"Documents": ["a.txt"], "Images": ["b.jpg"]}).

    assert str(f1) in mapping #checks if files are included in mapping
    assert str(f2) in mapping
    
    assert str(tmp_path / "Documents" / "a.txt") == mapping[str(f1)]
    assert str(tmp_path / "Images" / "b.jpg") == mapping[str(f2)]

#these are assertions to check if the documents and image go to the folder correctly, if any fail the test fails(AssertionError).



def test_perform_and_undo(tmp_path): #this checks if files are moved correctly and can be undone.
    f1 = tmp_path / "note.txt"
    f1.write_text("x")
    f2 = tmp_path / "pic.png"
    f2.write_text("y")
   
    #creates two files, a text file and an image file, in the temporary dictionary.

  
    mapping = propose_moves(tmp_path) #builds mapping of wheree to move files based on the extensions
    history_file = perform_moves(mapping, tmp_path / ".history") #moves files into their category and records the moves in history.
    


    assert (tmp_path / "Documents" / "note.txt").exists()
    assert (tmp_path / "Images" / "pic.png").exists() 

    #assertions to verify the files were moved correctly


    undo_last_move(tmp_path/".history")
    
    #calls the undo_last_moves from the main file and reverts the move using the history.


    assert (tmp_path / "note.txt").exists()
    assert (tmp_path / "pic.png").exists()
    #checks if the files are back in their original location, confirming the undo worked.
