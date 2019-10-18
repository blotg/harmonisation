# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTabWidget, QFormLayout, QDoubleSpinBox, QAbstractSpinBox, QGroupBox, QVBoxLayout
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import pyqtSignal, QSize, QMargins
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sys import float_info

class PlotWidget(FigureCanvas):
    def __init__(self, functions):
        self.figure = Figure()
        super().__init__(self.figure)
        self.functions = functions
        self.functions.changed.connect(self.refresh)
    def refresh(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        globalMaxScore = 0
        legend = []
        for i in range(self.functions.subjectsNumber()):
            scoreMax = self.functions.stats[i]["max"]
            if scoreMax > globalMaxScore:
                globalMaxScore = scoreMax
            N = 100
            maxi = -float_info.max
            xList = [scoreMax*i/N for i in range(N+1)]
            yList = [self.functions.evaluate(i,x) for x in xList]
            increasing = True
            for y in yList:
                if y > maxi:
                    maxi = y
                else:
                    increasing = False
            if increasing :
                legend.append(self.functions.subjectsNames[i])
            else:
                legend.append(self.functions.subjectsNames[i]+"⚠")
            ax.plot(xList,yList)
        ax.legend(legend)
        ax.set_xlabel("Score")
        ax.set_ylabel("Note")
        ax.set_xlim(0, globalMaxScore)
        self.draw()
    def resizeEvent(self, event):
        super().resizeEvent(event)
        height = self.size().height()
        width = self.size().width()
        if height != 0 and width != 0:
            left = 55./width
            right = 1 - 15./width
            bottom = 50./height
            top = 1 - 10./height
            if top > bottom and left < right:
                self.figure.subplots_adjust(left=left, right=right, top=top, bottom=bottom, wspace=0, hspace=0)
    def sizeHint(self):
        return QSize(400,400)

class Form(QTabWidget):
    changed = pyqtSignal(object)
    def __init__(self, functions):
        super().__init__()
        self.functions = functions
        self.functions.subjectAdded.connect(self.addSubject)
        self.functions.subjectChanged.connect(self.changeSubject)
        self.functions.subjectRemoved.connect(self.removeSubject)
        self.functions.functionChanged.connect(self.reinitiate)
    def addSubject(self):
        tab = QWidget()
        layout = QFormLayout()
        i = self.functions.subjectsNumber()-1
        for j in range(self.functions.parametersNumber()):
            doubleSpinBox = QDoubleSpinBox()
            doubleSpinBox.setMinimum(-float_info.max)
            doubleSpinBox.setMaximum(float_info.max)
            doubleSpinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
            doubleSpinBox.setValue(self.functions.defaultParameters[j])
            doubleSpinBox.valueChanged.connect(lambda : self.functions.setParameters(i,self.values(i)))
            layout.addRow(self.functions.parametersNames[j], doubleSpinBox)
        tab.setLayout(layout)
        self.addTab(tab,self.functions.subjectsNames[i])
    def removeSubject(self,i):
        self.removeTab(i)
    def changeSubject(self,i,name):
        self.setTabText(i,name)
    def reinitiate(self):
        while self.count() != 0:
            self.removeTab(0)
        for i in range(self.functions.subjecstNumber()):
            tab = QWidget()
            layout = QFormLayout()
            for j in range(len(self.functions.parametersNumber())):
                doubleSpinBox = QDoubleSpinBox()
                doubleSpinBox.setMinimum(-float_info.max)
                doubleSpinBox.setMaximum(float_info.max)
                doubleSpinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
                doubleSpinBox.setValue(self.functions.defaultParameters[j])
                doubleSpinBox.valueChanged.connect(lambda : self.functions.setParameters(i,self.values(i)))
                layout.addRow(self.functions.parametersNames[j], doubleSpinBox)
            tab.setLayout(layout)
            self.addTab(tab,self.functions.subjectsNames[i])
    def values(self, i):
        tab = self.widget(i)
        l = []
        for j in range(tab.layout().rowCount()):
            l.append(tab.layout().itemAt(j,1).widget().value())
        return l
    def valueChanged(self):
        self.changed.emit(self.values())
    def sizeHint(self):
        return QSize(0,0)

class ParametersContainer(QGroupBox):
    def __init__(self, functions):
        super().__init__()
        self.setTitle("Paramètres d'harmonisation")
        layout = QVBoxLayout()
        self.form = Form(functions)
        self.plot = PlotWidget(functions)
        layout.addWidget(self.form)
        layout.addWidget(self.plot)
        self.setLayout(layout)

