# Todopad

A very simple and minimalist gui python software to manage ToDo's and annotations in plain text. The application uses json for persistent storage.

Developed primarily for my own use.

![mainwindow](https://raw.githubusercontent.com/gabrielchristo/todopad/master/screenshot.png)

## Dependencies

- Python 3
- PyQt5

## Installation

If you are on windows and wanna create an executable, you can download the source code and run the following command:
> pyinstaller --onefile --windowed --icon=app.ico Main.py

In any other case, clone the repository and run Main.py

## Changelog

- 2019-12-24 First release

## Future Work (or not)
- [Export selected task content to pdf](https://stackoverflow.com/questions/22591865/save-contents-of-qtextedit-as-pdf)
- Encrypt json file / password protect
- [Move items up/down in list](https://www.qtcentre.org/threads/17996-Move-items-up-and-down-in-QListWidget)
- Implement auto save feature
- Implement a category filter?
- A mobile version?
