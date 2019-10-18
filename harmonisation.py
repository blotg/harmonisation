#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QSplitter, QAction
from PyQt5.QtCore import Qt
from table import TableContainer
from parameters import ParametersContainer
from statistics import StatContainer
from subjectsList import ListContainer
from functions import Functions
from data import Data

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Harmonisation")
        self.functions = Functions()
        self.functions.setFFromText("""def f(x, stats, alpha=1, beta=1, note_max=20):
                                        if stats['max'] == 0:
                                            return 0
                                        a = note_max/stats['max']**3*(alpha-2+beta)
                                        b = note_max/stats['max']**2*(3-beta-2*alpha)
                                        c = alpha*note_max/stats['max']
                                        d = 0
                                        return a*x**3+b*x**2+c*x+d""")
#        self.setF("""def f(x, a=1, b=0):
#                        return a*x+b""")
        self.data = Data(self.functions)
        self.createMenu()
        self.setCentralWidget(self.mainWidget())
        self.show()
    def createMenu(self):
        exitAction = QAction("&Quitter", self)
        exitAction.triggered.connect(self.close)
        menu = self.menuBar()
        fileMenu = menu.addMenu("&Fichier")
        fileMenu.addAction(exitAction)
    def mainWidget(self):
        mainSplitter = QSplitter()
        leftSplitter = QSplitter(Qt.Vertical)
        listContainer = ListContainer(self.functions)
        tableContainer = TableContainer(self.data)
        leftSplitter.addWidget(listContainer)
        leftSplitter.addWidget(tableContainer)
        rightSplitter = QSplitter(Qt.Vertical)
        parametersContainer = ParametersContainer(self.functions)
        statContainer = StatContainer(self.data)
        rightSplitter.addWidget(parametersContainer)
        rightSplitter.addWidget(statContainer)
        mainSplitter.addWidget(leftSplitter)
        mainSplitter.addWidget(rightSplitter)
        return mainSplitter

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

