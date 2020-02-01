@echo off
echo Updating Resources
pyrcc5 -o Resources.py Resources.qrc
rem echo Updating UI Forms
rem pyuic5 Ui_MainWindow.ui -o Ui_MainWindow.py
echo Generating Executable
pyinstaller --name=Todopad --onefile --windowed --icon=app.ico Main.py
pause