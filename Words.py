# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 08:39:28 2019

@author: Vladislav Sláma
"""
import numpy as np 
from Dictionary import Dictionary

class Word():
    def __init__(self,database):
        self.len = 0
        self.index  = None
        self.chars = None
        self._has_alternatives = False
        self._alter_count = 0
        self.alternatives = None
        self.Nalt = 0
        self.coor = None
        self._filled = False
        self._initialized = False
        if isinstance(database,Dictionary):
            self.database = database
    
    def init_by_index(self,word_indx, word2coor, word_len):
        self.len = word_len[word_indx]
        self.coor = word2coor[word_indx]
        self.index = word_indx
        self.chars = np.chararray(self.len,itemsize=1,unicode=True)
        self.chars[:] = "*"
        self._initialized = True
        
    def set_char(self,indx,char,force = False):
        if indx >= self.len:
            raise IOError("Trying to imput character at position " + str(indx)+
                          " for word with length ",str(self.len))
        if "".join(char) == "*" and (self.chars[indx] != "*"):
            self.chars[indx] = "*"
            if force: 
                self.alternatives = None
                self._has_alternatives = False
                self._alter_count = 0
                self.Nalt = 0
            self._filled = False
        elif (self.chars[indx] != "*") and (self.chars[indx] != char):
            raise IOError("Trying to rewrite letter with different one")
        else:
            self.chars[indx] = "".join(char)
            
    def get_new_word(self):
        # fill the grid and the grig will fill all word parts
        
        if self._has_alternatives:
#            if self.chars[0] != self.alternatives[0][0] and self.index == 3:
#                print(self.index,self.chars,self.alternatives)
#                raise IOError("Wrong alternatives")
            # continue systematicaly with other words
            if self._alter_count < self.Nalt:
                word = self.alternatives[self._alter_count]
                self._alter_count += 1
                return word
            else:
                self.alternatives = None
                self._has_alternatives = False
                self._alter_count = 0
                self.Nalt = 0
                return -1
        else:
            suggestions = self.database.find_words(self.chars)
            if np.ndim(suggestions) == 1:
                return suggestions
            elif np.ndim(suggestions) == 2:
                self.alternatives = suggestions
                self._has_alternatives = True
                self._alter_count = 1
                self.Nalt = len(suggestions)
                return (self.alternatives[0])
            else:
                return -1
