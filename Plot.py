# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *#QApplication, QMainWindow, QAction, QHBoxLayout, QVBoxLayout, QTableWidget, QWidget
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class PlotWidget(QChartView):
	def __init__(self):
		chart = QChart()
		chart.createDefaultAxes()
		chart.setTitle("Test")
		super().__init__(chart)
		self.setRenderHint(QPainter.Antialiasing);

class PlotContainer(QGroupBox):
	def __init__(self):
		super().__init__()
		self.setTitle("Paramètres d'harmonisation")
		layout = QVBoxLayout()
		layout.addWidget(PlotWidget())
		self.setLayout(layout)

	def sizeHint(self):
		return QSize(400,300)
