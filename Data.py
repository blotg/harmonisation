#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject
from scipy.stats import rankdata
import numpy as np

defaultStats = {"max":0., "min":0., "mean":0., "std":0., "median":0., "iqr":0.}

class Data(QObject):
    changed = pyqtSignal()
    def __init__(self,functions):
        super().__init__()
        self.functions = functions
        self.scores = []
        self.choosenSubjects = []
        self.ranks = []
        self.marks = []
        self.functions.changed.connect(self.recompute)
    def recompute(self):
        self.marks = [0.] * len(self.scores)
        for i in range(len(self.scores)):
            subject = self.choosenSubjects[i]
            score = self.scores[i]
            if subject >= 0:
                self.marks[i] = self.functions.evaluate(subject,score)
        self.ranks = rankdata(-np.array(self.marks),method='min').tolist()
        self.changed.emit()
    def setScore(self,i,score):
        self.scores[i] = score
        self.functions.setStats(self.getStatsScores())
        self.recompute()
    def setChoosenSubject(self,i,subject):
        print("OK")
        self.choosenSubjects[i] = subject
        self.functions.setStats(self.getStatsScores())
        self.recompute()
    def setData(self, scores, choosenSubjects):
        self.scores = scores
        self.choosenSubjects = choosenSubjects
        self.functions.setStats(self.getStatsScores())
    def getStatsScores(self):
        stats = {}
        npScores = np.array(self.scores)
        npChoosenSubjects = np.array(self.choosenSubjects)
        result = []
        for i in range(len(self.functions.subjectsNames)):
            stats = defaultStats.copy()
            subScores = npScores[npChoosenSubjects == i]
            if len(subScores) != 0:
                stats["max"] = subScores.max()
                stats["min"] = subScores.min()
                stats["mean"] = subScores.mean()
                stats["std"] = subScores.std()
                stats["median"] = np.median(subScores)
                q75, q25 = np.percentile(subScores, [75,25])
                stats["iqr"] = q75 - q25
            result.append(stats)
        return result
    def getStatsMarks(self):
        stats = {}
        npMarks = np.array(self.marks)
        stats = defaultStats.copy()
        if len(npMarks) != 0:
            stats["max"] = npMarks.max()
            stats["min"] = npMarks.min()
            stats["mean"] = npMarks.mean()
            stats["std"] = npMarks.std()
            stats["median"] = np.median(npMarks)
            q75, q25 = np.percentile(npMarks, [75,25])
            stats["iqr"] = q75 - q25
        return stats
    def getHistMarks(self,N=10):
        hist = np.histogram(self.marks, range=(0,self.getStatsMarks()["max"]))
        return (hist[0][:], hist[1][:])
