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
#        self.setF("""def f(x, alpha=1, beta=1, Y=20, X=100):
#                        a = Y/X**3*(alpha-2+beta)
#                        b = Y/X**2*(3-beta-2*alpha)
#                        c = alpha*Y/X
#                        d = 0
#                        return a*x**3+b*x**2+c*x+d""")
        self.setF("""def f(x, a=1, b=0):
                        return a*x+b""")
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
        parametersContainer = ParametersContainer(self.f,parameters(self.f)[1:])
        listContainer.added.connect(parametersContainer.form.addSubject)
        listContainer.removed.connect(parametersContainer.form.removeSubject)
        listContainer.changed.connect(parametersContainer.form.changeSubject)
        statContainer = StatContainer()
        rightSplitter.addWidget(parametersContainer)
        rightSplitter.addWidget(statContainer)
        mainSplitter.addWidget(leftSplitter)
        mainSplitter.addWidget(rightSplitter)
        return mainSplitter

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

