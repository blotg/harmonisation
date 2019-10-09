# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ListContainer(QGroupBox):
    added = pyqtSignal(str)
    removed = pyqtSignal(int)
    changed = pyqtSignal(int,str)
    def __init__(self):
        super().__init__()
        self.subjectsList = []
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
        title = "Sujet {:d}".format(self.listWidget.count()+1)
        item = QListWidgetItem(title)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.listWidget.addItem(item)
        self.subjectsList.append(title)
        self.added.emit(title)
    def removeItem(self):
        i = self.listWidget.currentRow()
        if i >= 0:
            self.listWidget.takeItem(i)
            self.subjectsList.pop(i)
            self.removed.emit(i)
    def hasChanged(self):
        for i in range(self.listWidget.count()):
            if self.listWidget.item(i).text() != self.subjectsList[i]:
                self.changed.emit(i,self.listWidget.item(i).text())
                self.subjectsList[i] = self.listWidget.item(i).text()
    def sizeHint(self):
        return QSize(400,150)
    