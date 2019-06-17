# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import *#QApplication, QMainWindow, QAction, QHBoxLayout, QVBoxLayout, QTableWidget, QWidget
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Table import TableContainer
from Plot import PlotContainer
from Statistics import StatContainer
from List import ListContainer

class App(QMainWindow):

	def __init__(self):
		super().__init__()
		self.setWindowTitle("Harmonisation")

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
		leftSplitter.addWidget(ListContainer())
		leftSplitter.addWidget(TableContainer())

		rightSplitter = QSplitter(Qt.Vertical)
		rightSplitter.addWidget(PlotContainer())
		rightSplitter.addWidget(StatContainer())

		mainSplitter.addWidget(leftSplitter)
		mainSplitter.addWidget(rightSplitter)
		return mainSplitter
		

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
 
