# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class StatContainer(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle("Statistiques")
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.chartWidget())
        bottomLayout = QGridLayout()
        bottomLayout.addWidget(QLabel("Moyenne"), 0,0)
        bottomLayout.addWidget(QLabel("Écart-type"), 0,1)
        bottomLayout.addWidget(QLabel("Médiane"), 1,0)
        bottomLayout.addWidget(QLabel("Écart inter quartiles"), 1,1)
        mainLayout.addLayout(bottomLayout)
        self.setLayout(mainLayout)

    def chartWidget(self):
        chart = QChart()
        chart.createDefaultAxes()
        chart.setTitle("Test")
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing);
        return chartView

    def sizeHint(self):
        return QSize(400,300)


