# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:38:13 2019

@author: Sector House 2814
"""

class myRectangle:
    def __init__(self, h, w):       #acts as default constructor and makes variable accessible to entire class
        if(h <=0 ):                 #must add 'self' to parameters so python knows you are using class variables
            self.height = 1
        else:
            self.height = h
        self.width = w
        self.area = self.calcArea()
        self.perimeter = self.calcPerimeter()
        
    def calcArea(self):             #calculates area within class only
        return self.width*self.height
    
    def calcPerimeter(self):        #calculates perimeter within class only
        return 2*self.width + 2*self.height
        