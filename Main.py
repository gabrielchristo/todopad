
import sys
import Resources
from MainWindow import *
from PyQt5 import QtWidgets, QtCore

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	w = MainWindow()
	stream = QtCore.QFile(':/Style.qss')
	stream.open(QtCore.QIODevice.ReadOnly)
	app.setStyleSheet(QtCore.QTextStream(stream).readAll())
	w.show()
	sys.exit(app.exec_())
