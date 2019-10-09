# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *#QApplication, QMainWindow, QAction, QHBoxLayout, QVBoxLayout, QTableWidget, QWidget
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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
            series.setName(p["name"])
            N = 100
            for i in range(N):
                series.append(i,self.f(i,*p["parameters"]))
            self.chart.addSeries(series)
        self.chart.createDefaultAxes()
        self.chart.axes()[0].setTitleText("Score")
        self.chart.axes()[1].setTitleText("Note")
        
    def sizeHint(self):
        return QSize(400,400)

class Form(QTabWidget):
    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        
    def addItem(self,nom):
        tab = QWidget()
        layout = QFormLayout()
        for (p,v) in self.parameters:
            doubleSpinBox = QDoubleSpinBox()
            doubleSpinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
            if v:
                doubleSpinBox.setValue(v)
            layout.addRow(p, doubleSpinBox)
        tab.setLayout(layout)
        self.addTab(tab,nom)
        QApplication.processEvents()
    
    def sizeHint(self):
        return QSize(0,0)

    def values(self):
        L = []
        for i in range(self.count()):
            tab = self.widget(i)
            l = []
            for j in range(tab.layout().rowCount()):
                l.append(tab.layout().itemAt(j,1).widget().value())
            L.append({"name":self.tabText(i), "parameters":l})
        print(L)

class ParametersContainer(QGroupBox):
    def __init__(self, f, parameters):
        super().__init__()
        self.setTitle("Paramètres d'harmonisation")
        layout = QVBoxLayout()
        self.form = Form(parameters)
        self.form.addItem("kgb")
        layout.addWidget(self.form)
        self.plot = PlotWidget(f)
        self.plot.setParametersList([{"name":"a","parameters":[2,3]},{"name":"b","parameters":[7,2]}])
        layout.addWidget(self.plot)
        self.setLayout(layout)
        self.form.values()

    def sizeHint(self):
        return QSize(400,400)

