# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ListContainer(QGroupBox):
    changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setTitle("Liste des sujets")
        mainLayout = QHBoxLayout()
        self.listWidget = QListWidget()
        self.listWidget.itemChanged.connect(self.hasChanged)
        mainLayout.addWidget(self.listWidget)
        mainLayout.addWidget(self.toolBar())
        self.setLayout(mainLayout)

    def toolBar(self):
        toolBar = QToolBar()
        toolBar.setOrientation(Qt.Vertical)
        toolBar.addAction("Sujet supplémentaire").triggered.connect(self.addItem)
        toolBar.addAction("Supprimer sujet").triggered.connect(self.removeItem)
        return toolBar

    def addItem(self):
        item = QListWidgetItem("Sujet {:d}".format(self.listWidget.count()+1))
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.listWidget.addItem(item)
        self.hasChanged()

    def removeItem(self):
        self.listWidget.takeItem(self.listWidget.currentRow())
        self.hasChanged()

    def hasChanged(self):
        stringList=[]
        for i in range(self.listWidget.count()):
            stringList.append(self.listWidget.item(i).text())
        print(stringList)
        self.changed.emit(stringList)

    def sizeHint(self):
        return QSize(400,150)

