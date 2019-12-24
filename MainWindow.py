
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QListWidget, QSplitter, QTextEdit, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QDir, QFile, QSize
from PyQt5.QtGui import QIcon
from Ui_MainWindow import *
from Item import *
import json
import Resources

class MainWindow(QMainWindow, Ui_MainWindow):

    # construtor
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.loadSplitter()
        self.setWindowTitle("Todopad")
        self.connects()
        self.path = QDir.currentPath()
        self.setWindowIcon(QIcon(':/app.ico'))
        self.textEdit.setAcceptRichText(False)
        
    # connects
    def connects(self):
        # clique em item da lista -> atualiza text edit
        self.listWidget.itemClicked.connect(self.updateTxtEdit)
        # mudança no text edit -> atualiza data/modified do current item
        self.textEdit.textChanged.connect(self.updateItemData)
        # botão de salvar -> salva lista atual como json
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.triggered.connect(self.saveJson)
        # botão de abrir -> limpa tudo e carrega arquivo json
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.loadJson)
        # botão sobre -> mostra message box com info
        self.actionAbout.triggered.connect(self.about)
        # botão add -> adiciona item ao final da lista
        self.addButton.clicked.connect(self.addItem)
        # botão clear -> limpa a lista e zera text edit/labels
        self.clearButton.clicked.connect(self.clearList)
        # botão remove -> remove item selecionado da lista e atualiza textedit/labels
        self.removeButton.clicked.connect(self.removeItem)

    # atualiza text edit e labels com currentItem
    def updateTxtEdit(self, crrtItem):
        self.textEdit.blockSignals(True)
        self.textEdit.setText(crrtItem.data)
        self.textEdit.blockSignals(False)
        # atualizando labels
        self.createdLabel.setText("Created at "+crrtItem.created.replace('T',' '))
        self.modifiedLabel.setText("Modified at "+crrtItem.modified.replace('T',' '))

    # atualiza E.D. data/modified e label modified do currentItem (se existir)
    def updateItemData(self):
        # se item da lista for invalido -> early return e MessageBox
        if(self.listWidget.count()==0 or self.listWidget.currentRow()==-1):
            msg = QMessageBox()
            msg.setText("Add a task to the list for editing")
            msg.setWindowTitle("No task selected")
            msg.setStandardButtons(QMessageBox.Ok)
            self.clearTextAndLabels()
            msg.exec()
            return
        # atualizando dados e label modified em tempo real
        item = self.listWidget.currentItem()
        item.updateData(self.textEdit.toPlainText(), item.getDateTime())
        self.modifiedLabel.setText("Modified at "+item.modified.replace('T',' '))

    # salva lista atual em json
    def saveJson(self):
	    objects = []
	    for i in range(self.listWidget.count()):
		    item = self.listWidget.item(i)
		    dict = {}
		    dict["title"] = item.text()
		    dict["data"] = item.data
		    dict["created"] = item.created
		    dict["modified"] = item.modified
		    dict["checked"] = item.checkState()
		    objects.append(dict)
	    filename = QFileDialog.getSaveFileName(self, 'Save JSON file', self.path, "JSON File (*.json)")
	    # cancelo operação -> early return
	    if (len(filename[0])==0): return
	    # atualizando path
	    self.path = filename[0]
	    with open(filename[0], 'w') as json_file: json.dump(objects, json_file, indent = 4, sort_keys=True)

    # carrega json na interface
    def loadJson(self):
        filename = QFileDialog.getOpenFileName(self, 'Open JSON file', self.path, "JSON File (*.json)")
        # cancelo operação -> early return
        if (len(filename[0])==0): return
        # limpando lista/textedit/labels sem confirmação
        self.listWidget.clear()
        self.clearTextAndLabels()
        # atualizando path
        self.path = filename[0]
        with open(filename[0], 'r') as json_file: jsonData = json.load(json_file)
        # para cado objeto no jsonArray crio um item com dados correspondentes
        for objects in jsonData:
            item = Item.from_json(objects)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState((QtCore.Qt.Checked if objects['checked']==2 else QtCore.Qt.Unchecked))
            item.setSizeHint(QSize(item.sizeHint().width(), 45))
            self.listWidget.addItem(item)

    # add item no final da lista
    def addItem(self):
        item = Item("Task #"+str(self.listWidget.count()+1))
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)
        item.setSizeHint(QSize(item.sizeHint().width(), 45))
        self.listWidget.addItem(item)

    # limpa lista/textedit/labels com confirmação
    def clearList(self):
        # se lista estiver vazia -> early return
        if self.listWidget.count()==0: return
        response = self.questionDialog('Clear List','Are you sure to clear the list?')
        if response == QMessageBox.No: return
        self.listWidget.clear()
        self.clearTextAndLabels()

    # remove item selecionado da lista
    def removeItem(self):
        row = self.listWidget.currentRow()
        # nenhum item selecionado -> early return
        if(row==-1): return
        # nome do item selecionado
        name = self.listWidget.currentItem().text()
        # confirmando remoção do item
        response = self.questionDialog('Remove Item','Are you sure to remove "'+name+'" from the list?')
        if response == QMessageBox.No: return
        self.listWidget.takeItem(row)
        # se lista ficar vazia limpo text edit/labels
        if(self.listWidget.count()==0): self.clearTextAndLabels()
        # senão atualizo os campos com novo item selecionado
        else: self.updateTxtEdit(self.listWidget.currentItem())

    # limpa text edit/labels
    def clearTextAndLabels(self):
        self.textEdit.blockSignals(True)
        self.textEdit.clear()
        self.textEdit.blockSignals(False)
        self.createdLabel.setText("Created at")
        self.modifiedLabel.setText("Modified at")

    # mostra mesage box com info do projeto
    def about(self):
        msg = QMessageBox()
        msg.setWindowTitle("About")
        msg.setText("Developed by Gabriel Christo\nRelease 1.0\n24/12/2019")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    # overwrite de closeEvent para confirmação de saida
    def closeEvent(self, event):
        reply = self.questionDialog('Quit Application','Are you sure to quit?')
        if reply == QMessageBox.Yes: event.accept()
        else: event.ignore()

    # mostra pergunta ao usuario de sim/nao e retorna resposta
    def questionDialog(self, title, text):
        return QMessageBox.question(self,title,text,QMessageBox.Yes,QMessageBox.No)

    # carrega layouts no splitter e atualiza centralWidget
    def loadSplitter(self):
        w1 = QWidget()
        w2 = QWidget()
        w1.setLayout(self.firstLayout)
        w2.setLayout(self.secondLayout)
        s = QSplitter(Qt.Horizontal)
        s.addWidget(w1)
        s.addWidget(w2)
        s.setCollapsible(0, False)
        s.setCollapsible(1, False)
        s.setStretchFactor(1, 1)
        self.setCentralWidget(s)









		
		
