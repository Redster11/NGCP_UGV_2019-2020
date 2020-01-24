# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:38:13 2019

@author: Sector House 2814
"""

class myRectangle:
    def __init__(self, h, w):
        if(h <=0 ):
            self.height = 1
        else:
            self.height = h
        self.width = w
        self.area = self.calcArea()
        self.perimeter = self.calcPerimeter()
        
    def calcArea(self):
        return self.width*self.height
    
    def calcPerimeter(self):
        return 2*self.width + 2*self.height
        