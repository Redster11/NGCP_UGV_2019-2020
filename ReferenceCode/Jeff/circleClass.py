# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 11:48:36 2019

@author: Sector House 2814
"""
import math

class myCircle:
    def __init__(self,r):       #same explanition as rectangleClass
        if(r > 0):
            self.radius = r
        else:
            self.radius = 1
        self.diameter = 2*self.radius
    
    def calcArea(r):            #calulates area based on input parameter from outside class
        return math.pi*r*r
    
    def calcCircumerence(r):    #calulates perimeter based on input parameter from outside class
        return 2*math.pi*r
    

    

    

        