# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox, QGroupBox, QVBoxLayout, QToolBar
from PyQt5.QtCore import QSize, Qt
import re


class TableWidget(QTableWidget):
    def __init__(self, data):
        super().__init__(0,5)
        self.data = data
        self.data.functions.subjectAdded.connect(self.addSubject)
        self.data.functions.subjectRemoved.connect(self.removeSubject)
        self.data.functions.subjectChanged.connect(self.changeSubject)
        self.data.changed.connect(self.fillData)
        self.setColumnWidth(0,120)
        self.setColumnWidth(1,60)
        self.setColumnWidth(2,80)
        self.setColumnWidth(3,50)    
        self.setColumnWidth(4,50)
        self.setHorizontalHeaderLabels(["Élève", "Score", "Sujet", "Note", "Rang"])
        self.cellChanged.connect(self.cellChange)
        self.appendRow()
    def cellChange(self,row, column):
        self.blockSignals(True)
        if column == 1:
            self.item(row,1).setText("{:.2f}".format(self.scoreAt(row)))
            self.data.setScore(row,self.scoreAt(row))
        self.blockSignals(False)
    def addRow(self,row):
        self.blockSignals(True)
        super().insertRow(row)
        item = QTableWidgetItem()
        self.setItem(row, 0, item)
        item = QTableWidgetItem()
        self.setItem(row, 1, item)
        combo = QComboBox()
        combo.addItems(self.data.functions.subjectsNames)
        combo.currentIndexChanged.connect(lambda : self.data.setChoosenSubject(row,self.subjectAt(row)))
        self.setCellWidget(row, 2, combo)
        item = QTableWidgetItem()
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        self.setItem(row, 3, item)
        item = QTableWidgetItem()
        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
        self.setItem(row, 4, item)
        self.updateData()
        self.blockSignals(False)
    def scoreAt(self, row):
        value = 0.
        item = self.item(row,1)
        text = item.text()
        if "." not in text:
            text = text.replace(",", ".", 1)
        text = re.search("(\d+\.?\d*)|(\.\d+)", text)
        if text:
            value = float(text.group(0))
        return value
    def subjectAt(self, row):
        return self.cellWidget(row,2).currentIndex()
    def updateData(self):
        scores = []
        choosenSubjects = []
        for row in range(self.rowCount()):
            scores.append(self.scoreAt(row))
            choosenSubjects.append(self.subjectAt(row))
        self.data.setData(scores,choosenSubjects)
    def appendRow(self):
        self.addRow(self.rowCount())
    def insertRow(self):
        self.addRow(self.currentRow())
    def removeRow(self):
        row = self.currentRow()
        super().removeRow(row)
    def addSubject(self):
        name = self.data.functions.subjectsNames[-1]
        for row in range(self.rowCount()):
            self.cellWidget(row,2).addItem(name)
    def removeSubject(self, i):
        for row in range(self.rowCount()):
            self.cellWidget(row,2).removeItem(i)
    def changeSubject(self, i):
        for row in range(self.rowCount()):
            self.cellWidget(row,2).setItemText(i,self.data.functions.subjectsNames[i])
    def fillData(self):
        for row in range(self.rowCount()):
            self.item(row,3).setText("{:.1f}".format(self.data.marks[row]))
            self.item(row,4).setText("{:d}".format(self.data.ranks[row]))
    def keyPressEvent(self,event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.currentRow() + 1 < self.rowCount():
                self.setCurrentCell(self.currentRow() + 1, self.currentColumn())
    def sizeHint(self):
        return QSize(400, 550)

class TableContainer(QGroupBox):
    def __init__(self, data):
        super().__init__()
        self.setTitle("Saisie des scores")
        layout = QVBoxLayout()
        self.tableWidget = TableWidget(data)
        layout.addWidget(self.toolBar())
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)
    def toolBar(self):
        toolBar = QToolBar()
        toolBar.addAction("Insérer ligne").triggered.connect(self.tableWidget.insertRow)
        toolBar.addAction("Supprimer ligne").triggered.connect(self.tableWidget.removeRow)
        toolBar.addAction("Insérer ligne à la fin").triggered.connect(self.tableWidget.appendRow)
        return toolBar