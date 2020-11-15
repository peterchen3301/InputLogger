# -*- coding: utf-8 -*-
"""
This is to parse the assembled wordlist and classify them

@author: Hsing-Yu Chen
@edit date: 202/11/15
"""

import json
import collections
import nltk
nltk.download('averaged_perceptron_tagger')

with open( "..//logfile//assembled.json", 'r' ) as logfile:
   word_pool = json.load(logfile)

words, word_list = [], collections.defaultdict(dict)
for w in word_pool:
    word_info = json.loads(w)
    this_word = word_info["word"]
    
    if this_word in word_list:
        word_list[this_word]["count"] += 1
    else:
        word_list[this_word]["avg_input_time"] = word_info["avg_input_time"]
        word_list[this_word]["count"] = 1
    
    words.append(word_info["word"])
    

for tag in nltk.pos_tag(words):
    word_list[tag[0]]["property"] = tag[1]
    
with open( "..//logfile//word_pool.json", "w") as json_file:
    json.dump(word_list, json_file)