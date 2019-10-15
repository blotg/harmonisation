# -*- coding: utf-8 -*-

from inspect import signature, _empty
from PyQt5.QtCore import pyqtSignal, QObject
from Data import defaultStats

class Functions(QObject):
    changed = pyqtSignal()
    functionChanged = pyqtSignal()
    subjectAdded = pyqtSignal()
    subjectRemoved = pyqtSignal(int)
    subjectChanged = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.subjectsNames = []
        self.parametersList = []
        self.f = lambda x:x
        self.defaultParameters = []
        self.parametersNames = []
        self.stats = []
    def setFFromText(self, text):
        namespace = {}
        exec(text,namespace)
        self.f = namespace["f"]
        sig = signature(self.f)
        self.defaultParameters = []
        self.parametersNames = []
        for parameter in list(sig.parameters)[2:]:
            default = 0 if sig.parameters[parameter].default == _empty else sig.parameters[parameter].default
            self.defaultParameters.append(default)
            self.parametersNames.append(parameter)
        self.parametersList = []
        for i in range(len(self.subjectsNames)):
            self.parametersList.append(self.defaultParameters)
        for i in range(len(self.subjectsNames)):
            self.stats.append(defaultStats)
        self.functionChanged.emit()
        self.changed.emit()
    def evaluate(self,subject,x):
        return self.f(x, self.stats[subject], *self.parametersList[subject])
    def addSubject(self,name):
        self.subjectsNames.append(name)
        self.parametersList.append(self.defaultParameters)
        self.stats.append(defaultStats)
        self.subjectAdded.emit()
        self.changed.emit()
    def changeSubject(self,i,name):
        self.subjectsNames[i] = name
        self.subjectChanged.emit(i)
        self.changed.emit()
    def removeSubject(self,i):
        self.subjectsNames.pop(i)
        self.parametersList.pop(i)
        self.subjectRemoved.emit(i)
        self.stats.pop(i)
        self.changed.emit()
    def setParameters(self,subject,parameters):
        self.parametersList[subject] = parameters
        self.changed.emit()
    def setStats(self,stats):
        self.stats=stats
        self.changed.emit()
    def subjectsNumber(self):
        return len(self.subjectsNames)
    def parametersNumber(self):
        return len(self.parametersNames)
