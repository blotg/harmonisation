#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Report():
    def __init__(self,data):
        self.data = data
    def getPreamble(self):
        return ("\documentclass[12,a4paper]{article}"
                "\usepackage{luatextra}"
                "\usepackage{polyglossia}"
                "\setmainlanguage{french}"
                "\usepackage{geometry}"
                "\usepackage{pgfplots}"
                "\geometry{left=1cm,right=1cm,top=1cm,bottom=1.5cm}"
                "\pagestyle{empty}"
                "\setlength\parindent{0pt}")
    def getDocumentText(self):
        text = getPreamble()
        return text