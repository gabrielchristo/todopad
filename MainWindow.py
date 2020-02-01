
from PyQt5 import QtCore, QtWidgets, QtGui, QtPrintSupport, uic
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QSplitter, QTextEdit, QMainWindow, QMessageBox, QFileDialog, QAbstractItemView, QCalendarWidget
from PyQt5.QtCore import pyqtSlot, Qt, QDir, QFile, QSize, QDateTime, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtPrintSupport import QPrinter
from Item import *
import json
import Resources

class MainWindow(QMainWindow):

    # construtor
    def __init__(self):
        super(MainWindow, self).__init__()
        # interface e splitter
        uiFile = QtCore.QFile(":/Ui_MainWindow.ui")
        uiFile.open(QtCore.QFile.ReadOnly)
        uic.loadUi(uiFile, self)
        uiFile.close()
        self.loadSplitter()
        self.setWindowTitle("Todopad")
        self.setWindowIcon(QIcon(':/app.ico'))
        # connects
        self.connects()
        # current path do app
        self.path = QDir.currentPath()
        # desativando html no text edit
        self.textEdit.setAcceptRichText(False)
        # font size do text edit
        self.textEdit.setFontPointSize(10)
        # ativando drag and drop interno da lista
        self.listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        # inicializando objeto do calendario
        self.calendar = QCalendarWidget()
        self.calendar.setWindowTitle('Calendar')
        self.calendar.setWindowIcon(QIcon(':/app.ico'))
        self.calendar.setGridVisible(True)
        # controle de versao da aplicacao para escrita no json
        self.version = "1.1"
        
    # connects
    def connects(self):
        # clique em item da lista -> atualiza text edit
        self.listWidget.itemClicked.connect(self.updateTxtEdit)
        # mudança no text edit -> atualiza data/modified do current item
        self.textEdit.textChanged.connect(self.updateItemData)
        # botão de salvar -> salva lista atual como json verificando o path
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.triggered.connect(self.saveJson)
        # botao de salvar como -> salva lista atual como json em outro arquivo
        self.actionSaveAs.setShortcut("Ctrl+Alt+S")
        self.actionSaveAs.triggered.connect(self.saveJson)
        # botao calendar -> abre janela com calendario
        self.actionCalendar.triggered.connect(self.showCalendar)
        # botao de exportar pdf -> salva pdf com nome do item atual e modified
        self.pdfButton.clicked.connect(self.saveToPDF)
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
    @pyqtSlot(QListWidgetItem)
    def updateTxtEdit(self, crrtItem: QListWidgetItem):
        self.textEdit.blockSignals(True)
        self.textEdit.setText(crrtItem.data)
        self.textEdit.blockSignals(False)
        # atualizando labels
        self.createdLabel.setText("Created at "+crrtItem.created.replace('T',' '))
        self.modifiedLabel.setText("Modified at "+crrtItem.modified.replace('T',' '))

    # atualiza E.D. data/modified e label modified do currentItem (se existir)
    @pyqtSlot()
    def updateItemData(self):
        # se item da lista for invalido -> limpo o text edit e early return
        if(not self.hasSelectedItem()):
            self.clearTextAndLabels()
            return
        # atualizando dados e label modified em tempo real
        item = self.listWidget.currentItem()
        item.updateData(self.textEdit.toPlainText(), item.getDateTime())
        self.modifiedLabel.setText("Modified at "+item.modified.replace('T',' '))

    # salva lista atual em json
    @pyqtSlot()
    def saveJson(self):
            # primeiro objeto do json é data de save do arquivo
            objects = [{"saveDate" : QDateTime.currentDateTime().toString(Qt.ISODate), "version": self.version}]
            # varrendo list widget
            for i in range(self.listWidget.count()):
                item = self.listWidget.item(i)
                dict = {}
                dict["title"] = item.text()
                dict["data"] = item.data
                dict["created"] = item.created
                dict["modified"] = item.modified
                dict["checked"] = item.checkState()
                objects.append(dict)
            # se sender for o botao de save e algum arquivo ja tiver sido aberto -> salvo em cima do mesmo
            if(self.sender() == self.actionSave and self.path != QDir.currentPath()):
                with open(self.path, 'w') as json_file: json.dump(objects, json_file, indent = 4, sort_keys=True)
            # senao abro dialogo para obter nome do novo arquivo
            else:
                filename = QFileDialog.getSaveFileName(self, 'Save JSON file', self.path, "JSON File (*.json)")
                # cancelo operação -> early return
                if (len(filename[0])==0): return
                # atualizando path
                self.path = filename[0]
                # salvando novo arquivo
                with open(self.path, 'w') as json_file: json.dump(objects, json_file, indent = 4, sort_keys=True)
            # mensagem no status bar
            self.statusBar.showMessage("File saved at "+self.path, 3000)

    # carrega json na interface
    @pyqtSlot()
    def loadJson(self):
        filename = QFileDialog.getOpenFileName(self, 'Open JSON file', self.path, "JSON File (*.json)")
        # cancelo operação -> early return
        if (len(filename[0])==0): return
        # limpando lista/textedit/labels (sem confirmação)
        self.listWidget.clear()
        self.clearTextAndLabels()
        # atualizando path
        self.path = filename[0]
        with open(filename[0], 'r') as json_file: jsonData = json.load(json_file)
        # para cado objeto no jsonArray crio um item com dados correspondentes
        for objects in jsonData:
            # se for object com saveDate eu pulo o mesmo (e mantenho compatibilidade com versao 1.0 do json)
            if 'saveDate' in objects: continue
            # se for item da lista crio o mesmo
            else:
                item = Item.from_json(objects)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState((QtCore.Qt.Checked if objects['checked']==2 else QtCore.Qt.Unchecked))
                item.setSizeHint(QSize(item.sizeHint().width(), 45))
                self.listWidget.addItem(item)
        # mensagem no status bar
        self.statusBar.showMessage("Loaded file at "+self.path, 3000)

    # adiciona novo item ao final da lista
    @pyqtSlot()
    def addItem(self):
        item = Item("Task #"+str(self.listWidget.count()+1))
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)
        item.setSizeHint(QSize(item.sizeHint().width(), 45))
        self.listWidget.addItem(item)

    # limpa lista/textedit/labels (com confirmação)
    @pyqtSlot()
    def clearList(self):
        # se lista estiver vazia -> early return
        if self.listWidget.count()==0:
            self.statusBar.showMessage("Task list is already empty", 3000)
            return
        # senao chamo dialogo de confirmacao
        response = self.questionDialog('Clear List', 'Are you sure to clear the list?')
        if response == QMessageBox.No: return
        # se resposta for sim limpo lista/textedit/labels
        self.listWidget.clear()
        self.clearTextAndLabels()
        # resetando path (evitar overwrite em algum json aberto anteriormente)
        self.path = QDir.currentPath()

    # remove item selecionado da lista
    @pyqtSlot()
    def removeItem(self):
        # early return se nenhum item estiver selecionado
        if(not self.hasSelectedItem()): return
        # nome do item selecionado
        name = self.listWidget.currentItem().text()
        # confirmando remoção do item
        response = self.questionDialog('Remove Item','Are you sure to remove "'+name+'" from the list?')
        # early return se resposta for nao
        if response == QMessageBox.No: return
        # se resposta for sim -> retirando item atual da lista
        self.listWidget.takeItem(self.listWidget.currentRow())
        # se lista ficar vazia limpo text edit/labels e reseto o path
        if(self.listWidget.count()==0):
            self.clearTextAndLabels()
            self.path = QDir.currentPath()
        # senão atualizo os campos com novo item selecionado
        else: self.updateTxtEdit(self.listWidget.currentItem())

    # limpa text edit/labels
    def clearTextAndLabels(self):
        self.textEdit.blockSignals(True)
        self.textEdit.clear()
        self.textEdit.blockSignals(False)
        self.createdLabel.setText("Created at")
        self.modifiedLabel.setText("Modified at")

    # mostra message box com info do projeto
    @pyqtSlot()
    def about(self):
        msg = QMessageBox()
        msg.setWindowTitle("About Todopad")
        msg.setText("<h3>Developed by <a href='https://github.com/gabrielchristo/todopad'>Gabriel Christo</a></h3><p>Version 1.1</p><p>01/02/2020</p>")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.button(QMessageBox.Ok).setCursor(Qt.PointingHandCursor)
        msg.setWindowIcon(QIcon(':/app.ico'))
        msg.exec()

    # overwrite de closeEvent para confirmação de saida
    def closeEvent(self, event):
        reply = self.questionDialog('Quit Application','Are you sure to quit?')
        if reply == QMessageBox.Yes: event.accept()
        else: event.ignore()

    # mostra pergunta ao usuario de sim/nao e retorna resposta
    def questionDialog(self, title, text):
        return QMessageBox.question(self, title, text, QMessageBox.Yes, QMessageBox.No) 

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

    # salva conteudo do item selecionado como pdf
    @pyqtSlot()
    def saveToPDF(self):
        # early return se nao tiver item selecionado
        if(not self.hasSelectedItem()): return
        # obtendo item atual
        item = self.listWidget.currentItem()
        # pegando nome do arquivo pdf e salvando o pdf
        filename = QFileDialog.getSaveFileName(self, 'Save to PDF', self.path+QDir.separator()+item.text()+"-"+item.modified.replace(":","-"), "PDF File (*.pdf)")
        if filename[0]:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setPageSize(QPrinter.A4)
            printer.setColorMode(QPrinter.Color)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setFullPage(True)
            printer.setOrientation(QPrinter.Portrait)
            printer.setOutputFileName(filename[0])
            self.textEdit.print_(printer)

    # verifica se tem algum item selecionado no list widget
    def hasSelectedItem(self):
        if(self.listWidget.currentRow() == -1):
            self.statusBar.showMessage("No task selected in the list", 3000)
            return False
        else: return True

    # mostra widget de calendario
    @pyqtSlot()
    def showCalendar(self):
        # early return se calendario ja estiver visivel
        if(self.calendar.isVisible()): return
        # se nao estiver visivel mostro o mesmo
        self.calendar.show()
        self.calendar.setFocus()
