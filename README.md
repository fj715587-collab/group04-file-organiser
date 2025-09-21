# (Group 04) File Organiser Utility Project.

We will build a File Organizer Utility that scans a user-selected folder, groups files into categories based on file extensions,
shows a preview of proposed moves in a confirmation GUI, performs the moves on confirmation, and supports undoing the last operation. We’ll use Python 3.10, pipenv for dependency management, pytest for tests, and Tkinter for a minimal GUI. Developer(s) will implement scanning, preview, move, and undo; QA will write two pytest tests (propose moves, undo). Docs/Presenter will prepare README, demo video, and final report.

## Features  
- Organizes files into folders by file extension.  
- Command-line interface (CLI) for quick use.  
- Graphical user interface (GUI) with Tkinter.  
- Automated tests using Pytest.

## Tests
Run the CLI:
pipenv run python src/main.py

Run the GUI:
pipenv run python src/gui.py

Run the test suite with:
pipenv run pytest

## Team
- Coordinator: [Jacob Oluwakemi]: Scheduling meetings, overall coordination, GitHub repo management.
- Developer: [Abdurrahim Ibrahim, Gaius Nathaniel]: Wrote main.py for file organization.
- QA / Tests: [Ogah Christopher]: Wrote test_main.py with Pytest and ensured code quality.
- Docs / Presenter: [Gaius Nathaniel] Wrote README, final report, and created the demo video


## 🎥 Demo Video 
https://drive.google.com/file/d/13t3HihXLt5TWUqSFlH6Mf0KZvY-ltaOy/view?usp=drivesdk




## Notes
Python version: 3.10+
Dependency management: Pipenv (Pipfile + Pipfile.lock)
Testing: Pytest with minimum 2 passing tests
Version control: GitHub repository with clear commit history



