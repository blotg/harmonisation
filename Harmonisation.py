#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QSplitter, QAction#, QMainWindow, QAction, QHBoxLayout, QVBoxLayout, QTableWidget, QWidget
#from PyQt5.QtChart import *
#from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from Table import TableContainer
from Parameters import ParametersContainer
from Statistics import StatContainer
from List import ListContainer
import code
from inspect import signature, _empty

def parameters(f):
    sig = signature(f)
    l = []
    for parameter in sig.parameters:
        default = 0
        if sig.parameters[parameter].default != _empty :
            default = sig.parameters[parameter].default
        l.append((parameter,default))
    return l

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Harmonisation")
        
        self.setF("""def f(score, lamdba1, lambda2=2):
                        return score**2*lamdba1/lambda2""")
        

        self.createMenu()
        self.setCentralWidget(self.mainWidget())

        self.show()
        
    def setF(self,textF):
        namespace = {}
        exec(textF,namespace)
        self.f = namespace["f"]

    def createMenu(self):
        exitAction = QAction("&Quitter", self)
        exitAction.triggered.connect(self.close)

        menu = self.menuBar()
        fileMenu = menu.addMenu("&Fichier")
        fileMenu.addAction(exitAction)

    def mainWidget(self):
        mainSplitter = QSplitter()

        leftSplitter = QSplitter(Qt.Vertical)
        
        listContainer = ListContainer()
        tableContainer = TableContainer()
        listContainer.added.connect(tableContainer.addSubject)
        listContainer.removed.connect(tableContainer.removeSubject)
        listContainer.changed.connect(tableContainer.changeSubject)
        
        leftSplitter.addWidget(listContainer)
        leftSplitter.addWidget(tableContainer)

        rightSplitter = QSplitter(Qt.Vertical)
        rightSplitter.addWidget(ParametersContainer(self.f,parameters(self.f)[1:]))
        rightSplitter.addWidget(StatContainer())

        mainSplitter.addWidget(leftSplitter)
        mainSplitter.addWidget(rightSplitter)
        return mainSplitter


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

