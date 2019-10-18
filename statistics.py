# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QGridLayout, QLabel, QWidget, QPushButton
from PyQt5.QtCore import QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

class StatGrid(QGridLayout):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.textMean = "Moyenne : {:.2f}"
        self.textStd = "Écart-type : {:.2f}"
        self.textMed = "Médiane : {:.2f}"
        self.textIqr = "Écart inter quartiles : {:.2f}"
        self.itemMean=QLabel("")
        self.itemStd=QLabel("")
        self.itemMed=QLabel("")
        self.itemIqr=QLabel("")
        self.addWidget(self.itemMean, 0,0)
        self.addWidget(self.itemStd, 0,1)
        self.addWidget(self.itemMed, 1,0)
        self.addWidget(self.itemIqr, 1,1)
        self.data.changed.connect(self.refresh)
    def refresh(self):
        stats = self.data.getStatsMarks()
        self.itemMean.setText(self.textMean.format(stats["mean"]))
        self.itemStd.setText(self.textStd.format(stats["std"]))
        self.itemMed.setText(self.textMed.format(stats["median"]))
        self.itemIqr.setText(self.textIqr.format(stats["iqr"]))
        
class HistogramChart(FigureCanvas):
    def __init__(self,data):
        self.figure = Figure()
        super().__init__(self.figure)
        self.data = data
        self.data.changed.connect(self.refresh)
    def refresh(self):
        marks, bins = self.data.getHistMarks()
        ax = self.figure.add_subplot(111)
        ax.clear()
        if len(marks) != 0:
            ax.bar(bins[:-1], marks, align='edge', width=bins[-1]/10)
        ax.set_xlim(0, self.data.getStatsMarks()["max"])
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        self.draw()
    def resizeEvent(self, event):
        super().resizeEvent(event)
        height = self.size().height()
        width = self.size().width()
        if height != 0 and width != 0:
            left = 55./width
            right = 1 - 15./width
            bottom = 30./height
            top = 1 - 10./height
            if top > bottom and left < right:
                self.figure.subplots_adjust(left=left, right=right, top=top, bottom=bottom, wspace=0, hspace=0)
    def sizeHint(self):
        return QSize(400,300)

class StatContainer(QGroupBox):
    def __init__(self, data):
        super().__init__()
        self.setTitle("Statistiques")
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(HistogramChart(data))
        mainLayout.addLayout(StatGrid(data))
        self.setLayout(mainLayout)
