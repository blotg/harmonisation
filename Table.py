# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re


class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__(0,5)
        self.subjectsList=[]
        self.setColumnWidth(0,120)
        self.setColumnWidth(1,60)
        self.setColumnWidth(2,80)
        self.setColumnWidth(3,50)    
        self.setColumnWidth(4,50)
        self.setHorizontalHeaderLabels(["Élève", "Score", "Sujet", "Note", "Rang"])
        self.itemChanged.connect(self.itemChange)
        self.appendRow()

    def itemChange(self,item):
        if item.column() == 1:
            valeur = 0.
            texte = item.text()
            if "." not in texte:
                texte = texte.replace(",", ".", 1)
            texte = re.search("(\d+\.?\d*)|(\.\d+)", texte)
            if texte:
                valeur = float(texte.group(0))
            item.setText(str(valeur))
            
    def appendRow(self):
        row = self.rowCount()
        super().insertRow(row)
        item = QTableWidgetItem()
        self.setItem(row, 0, item)
        item = QTableWidgetItem(3)
        self.setItem(row, 1, item)
        combo = QComboBox()
        combo.addItems(self.subjectsList)
        self.setCellWidget(row, 2, combo)
        item = QTableWidgetItem()
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        self.setItem(row, 3, item)
        item = QTableWidgetItem()
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        self.setItem(row, 4, item)

    def insertRow(self):
        row = self.currentRow()
        super().insertRow(row)
        item = QTableWidgetItem()
        self.setItem(row, 0, item)
        item = QTableWidgetItem()
        self.setItem(row, 1, item)
        combo = QComboBox()
        combo.addItems(self.subjectsList)
        self.setCellWidget(row, 2, combo)
        item = QTableWidgetItem()
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        self.setItem(row, 3, item)
        item = QTableWidgetItem()
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        self.setItem(row, 4, item)

    def removeRow(self):
        row = self.currentRow()
        super().removeRow(row)

    def addSubject(self, subject):
        self.subjectsList.append(subject)
        for row in range(self.rowCount()):
            self.cellWidget(row,2).addItem(subject)

    def removeSubject(self, i):
        self.subjectsList.pop(i)
        for row in range(self.rowCount()):
            self.cellWidget(row,2).removeItem(i)

    def changeSubject(self, i, subject):
        self.subjectsList[i] = subject
        for row in range(self.rowCount()):
            self.cellWidget(row,2).setItemText(i,subject)
    
    def sizeHint(self):
        return QSize(400, 450)



class TableContainer(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("Saisie des scores")
        layout = QVBoxLayout()
        self.tableWidget = TableWidget()
        layout.addWidget(self.toolBar())
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def toolBar(self):
        toolBar = QToolBar()
        toolBar.addAction("Insérer ligne").triggered.connect(self.tableWidget.insertRow)
        toolBar.addAction("Supprimer ligne").triggered.connect(self.tableWidget.removeRow)
        toolBar.addAction("Insérer ligne à la fin").triggered.connect(self.tableWidget.appendRow)
        return toolBar

    def addSubject(self, subject):
        self.tableWidget.addSubject(subject)

    def removeSubject(self, i):
        self.tableWidget.removeSubject(i)

    def changeSubject(self, i, subject):
        self.tableWidget.changeSubject(i,subject)