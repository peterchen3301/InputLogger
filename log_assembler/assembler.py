# -*- coding: utf-8 -*-
"""
This is a program that assembles input logs to string of words

@author: Hsing-Yu Chen
"""

from collections import deque
import json

class Log_assembler():
    
    def __init__(self, keylog_path, mouselog_path, save_dir ):

        keylog, mouselog = self.read_log_txt(keylog_path, mouselog_path)
            
        wordmap = self.assemble( keylog, mouselog )
        #print(wordmap)
        
        json_map = self.build_dict(wordmap)
        #print(dic_list)
        
        #self.save_file_txt( input_str, save_dir )
        self.save_file_json( json_map, save_dir )
            
    def assemble(self, keylog, mouselog):
    
        inputs = deque()
        prev_time = '0000-00-00T00:00:00-00'
        
        while True:
            line = keylog.readline()    
            if not line: 
                break
            
            lineData = list(filter(None,line.split(" ")))
            key, this_time = lineData[-2], lineData[0]
    
            if len(key) > 1:   
                if lineData[-2] in ["SPACE","Key.enter"]:
                    inputs.append(" ")
                if lineData[-2] == "Key.backspace":
                    inputs.pop()
            else:
                inputs.append( ( lineData[-2], self.time_difference( prev_time, this_time ) ) )
                
            prev_time = this_time
            
        inputs.append(" ")
            
        wordmap, word, time_intvls = [], [], []
        for input_element in inputs:
            if input_element != " ":
                word.append( input_element[0] )
                time_intvls.append( input_element[1] )
            elif word and time_intvls:
                wordmap.append( ( "".join(word), sum(time_intvls[1:])/len(time_intvls) ) )   
                word, time_intvls = [], []
        
        return wordmap 
    
    def time_difference(self, prev_time, this_time ):
        
        prev_timelist, this_timelist = self.time_convert(prev_time), self.time_convert(this_time)
        mul, diff = [ 60*60, 60, 1, 0.01 ], 0
        for i in range(4):
            diff += (this_timelist[i] - prev_timelist[i]) * mul[i]
        return diff
            
    def time_convert(self, time ):
        
        timelist = time.split("T")[-1].split(":")
        timelist += timelist.pop().split("-")
        return [int(t) for t in timelist]
        
    def save_file_txt(self, txt_str, save_path):
                
        with open( save_path + "//assembled.txt", "w") as rfile:
            rfile.write( txt_str ) 
            rfile.close() 
            
    def save_file_json(self, json_str, save_path):
                
        with open( save_path + "//assembled.json", "w") as json_file:
            json.dump(json_str, json_file)
    
    def read_log_txt(self, keylog_path, mouselog_path):
                
        keylog, mouselog = open(keylog_path,"r"), open(mouselog_path,"r")
        if "KeyboardLogger Started" not in keylog.readline():
            raise FileNotFoundError("Error loading KeyboardLogger file")            
        if "MouseLogger Started" not in mouselog.readline():
            raise FileNotFoundError("Error loading MouseLogger file")  
        return (keylog, mouselog)
        
    def build_dict(self, wordmap ):
        
        json_list = []
        for word, average_time in wordmap:
            obj = {
                "word" : word,
                "avg_input_time" : average_time
                }
            json_list.append( json.dumps(obj) )
        
        return json_list
        
            
            
        
        
        
        
        
