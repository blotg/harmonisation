# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *#QApplication, QMainWindow, QAction, QHBoxLayout, QVBoxLayout, QTableWidget, QWidget
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from sys import float_info

class PlotWidget(QChartView):
    def __init__(self, f):
        self.chart = QChart()
        self.setFunction(f)
        self.chart.setMargins(QMargins(0,0,0,0));
        self.chart.layout().setContentsMargins(0, 0, 0, 0);
        super().__init__(self.chart)
        self.setRenderHint(QPainter.Antialiasing);
    def setFunction(self,f):
        self.f = f
    def setParametersList(self, parametersList):
        self.parametersList = parametersList
        self.refresh()
    def refresh(self):
        self.chart.removeAllSeries()
        for p in self.parametersList:
            scoreMax = 36
            series = QLineSeries()
            N = 100
            increasing = True
            maxi = -float_info.max
            for x in range(N+1):
                y = self.f(x,*p["parameters"])
                if y > maxi:
                    maxi = y
                else:
                    increasing = False
                series.append(x,y)
            self.chart.addSeries(series)
            if increasing:
                series.setName(p["name"])
            else:
                series.setName(p["name"]+"⚠")
        self.chart.createDefaultAxes()
        if self.chart.axes():
            self.chart.axes()[0].setTitleText("Score")
            self.chart.axes()[1].setTitleText("Note")
    def sizeHint(self):
        return QSize(400,400)

class Form(QTabWidget):
    changed = pyqtSignal(object)
    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
    def addSubject(self,nom):
        tab = QWidget()
        layout = QFormLayout()
        for (p,v) in self.parameters:
            doubleSpinBox = QDoubleSpinBox()
            doubleSpinBox.setMinimum(-float_info.max)
            doubleSpinBox.setMaximum(float_info.max)
            doubleSpinBox.valueChanged.connect(self.valueChanged)
            doubleSpinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
            if v:
                doubleSpinBox.setValue(v)
            layout.addRow(p, doubleSpinBox)
        tab.setLayout(layout)
        self.addTab(tab,nom)
        self.valueChanged()
    def removeSubject(self,i):
        self.removeTab(i)
        self.valueChanged()
    def changeSubject(self,i,name):
        self.setTabText(i,name)
        self.valueChanged()
    def values(self):
        L = []
        for i in range(self.count()):
            tab = self.widget(i)
            l = []
            for j in range(tab.layout().rowCount()):
                l.append(tab.layout().itemAt(j,1).widget().value())
            L.append({"name":self.tabText(i), "parameters":l})
        return L    
    def valueChanged(self):
        self.changed.emit(self.values())
    def sizeHint(self):
        return QSize(0,0)

class ParametersContainer(QGroupBox):
    def __init__(self, f, parameters):
        super().__init__()
        self.setTitle("Paramètres d'harmonisation")
        layout = QVBoxLayout()
        self.form = Form(parameters)
        self.plot = PlotWidget(f)
        self.form.changed.connect(self.plot.setParametersList)
        layout.addWidget(self.form)
        layout.addWidget(self.plot)
        self.setLayout(layout)
        self.form.values()
    def sizeHint(self):
        return QSize(400,400)

