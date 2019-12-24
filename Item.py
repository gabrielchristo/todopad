
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QListWidgetItem, QWidget
from PyQt5.QtCore import QDateTime, Qt, QVariant

class Item(QListWidgetItem):

        # construtor
        def __init__(self, title, data="", created="", modified=""):
                super(Item, self).__init__()
                self.setText(title)
                self.data = data
                if(len(created)==0): self.created = self.getDateTime()
                else: self.created = created
                if(len(modified)==0): self.modified = self.getDateTime()
                else: self.modified = modified

        # overload do construtor para json
        @classmethod
        def from_json(cls, info):
                return cls(title=info['title'], data=info['data'], created=info['created'], modified=info['modified'])

        # retorna data completa no padrão iso (split by T)
        def getDateTime(self):
                return QDateTime.currentDateTime().toString(Qt.ISODate)

        # atualiza data/modified na E.D.
        def updateData(self, newData, modified):
                self.data = newData
                self.modified = modified
