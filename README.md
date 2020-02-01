# Todopad

A very simple and minimalist gui python software to manage ToDo's and annotations in plain text. The application uses json for persistent storage.

![mainwindow](https://raw.githubusercontent.com/gabrielchristo/todopad/master/screenshot.png)

## Dependencies

- Python 3
- PyQt5

## Installation

If you are on windows and wanna an executable, you can [download it](https://github.com/gabrielchristo/todopad/releases/download/1.0/todopad_1.0_x86.exe) or download the source code and run the following command:
> pyinstaller --name=Todopad --onefile --windowed --icon=app.ico Main.py

In any other case, clone the repository and run
> python Main.py

## Changelog

#### v1.1
- Added "Save as" option
- Internal Drag and Drop on task list
- Last save date and version on json file
- Helpful calendar window
- Exporting selected task content to pdf
- Status bar messages
 
#### v1.0
-  First release

## Future Work (or not)
- [Encrypt json file / password protect](https://pypi.org/project/pyAesCrypt/)
- Auto save feature
- Search item filter with line edit
- Splash screen

