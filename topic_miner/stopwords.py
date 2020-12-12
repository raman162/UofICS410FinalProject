# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 19:32:40 2020

@author: bhara
"""
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
f = open("stopwords.txt", "w")
stopWords = stopwords.words('english')
for word in stopWords:
    f.write(word+"\n")
f.close()
