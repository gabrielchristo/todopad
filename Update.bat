@echo off
echo Updating Resources
pyrcc5 -o Resources.py Resources.qrc
echo Updating UI Forms
pyuic5 Ui_MainWindow.ui -o Ui_MainWindow.py
echo Generating Executable
pyinstaller --onefile --windowed --icon=app.ico Main.py
pause