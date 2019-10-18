# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QToolBar, QListWidgetItem, QGroupBox, QHBoxLayout, QListWidget
from PyQt5.QtCore import QSize, Qt

class ListContainer(QGroupBox):
    def __init__(self, functions):
        super().__init__()
        self.functions = functions
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
        self.functions.addSubject(title)
    def removeItem(self):
        i = self.listWidget.currentRow()
        if i >= 0:
            self.listWidget.takeItem(i)
            self.functions.removeSubject(i)
    def hasChanged(self):
        for i in range(self.listWidget.count()):
            if self.listWidget.item(i).text() != self.functions.subjectsNames[i]:
                self.functions.changeSubject(i, self.listWidget.item(i).text())
    def sizeHint(self):
        return QSize(400, 150)
