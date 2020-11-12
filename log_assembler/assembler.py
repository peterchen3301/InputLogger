# -*- coding: utf-8 -*-
"""
This is a program that assembles input logs to string of words

@author: Hsing-Yu Chen
"""

from collections import deque

keylog = open("..//logfile//keyboard_log.txt", "r")
if "KeyboardLogger Started" not in keylog.readline():
    raise FileNotFoundError("Error loading KeyboardLogger file")

mouselog = open("..//logfile//mouse_log.txt", "r")
if "MouseLogger Started" not in mouselog.readline():
    raise FileNotFoundError("Error loading MouseLogger file")
    
inputs = deque()

while True:
    
    line = keylog.readline()    
    if not line: 
        break

    lineData = list(filter(None,line.split(" ")))
    key = lineData[-2]
    
    if len(key) > 1:   
        if lineData[-2] in ["SPACE","Key.enter"]:
            inputs.append(" ")
        if lineData[-2] == "Key.backspace":
            inputs.pop()
    else:
        inputs.append( lineData[-2] )
    
rfile = open('..//logfile//assembled.txt', 'w') 
rfile.write( "".join(inputs) ) 
rfile.close() 



