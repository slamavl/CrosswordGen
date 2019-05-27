# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 15:47:39 2019

@author: Vladislav Sláma
"""
import numpy as np
from Settings import _compilation

class Dictionaly_length():
    
    def __init__(self,word_length,gen_type = "Random"):
        self.len = word_length
        self.size = 0
        self._initialized = False
        self.words = None
        self._gen_type = gen_type
        self._last_word = None
    
    def add_word(self,new_word):
        """ Add word to a database
        """
        
        if not isinstance(new_word,str):
            if _compilation:
                input("Error: Words must be added as strings")
            raise IOError("Words must be added as strings")
        if len(new_word) != self.len:
            if _compilation:
                input("Error: Unable to load word '"+new_word+"' to class with word"+ 
                          " length "+str(self.len))
            raise IOError("Unable to load word '"+new_word+"' to class with word"+ 
                          " length "+str(self.len))
        
        if not self._initialized:
            self.words = np.chararray((0,self.len),itemsize=1,unicode=True)
            self._initialized = True
#            self.words[0,:] = list(new_word)

        self.words = np.vstack((self.words,list(new_word)))
        self.size += 1
    
    def new_word(self):
        """ generate new word from the database """
        
        if not self._initialized:
            if _compilation:
                input("Error: No words with with size " + str(self.len) + "in the dictionary")
            raise IOError("No words with with size " + str(self.len) + "in the dictionary")
        
        if self._gen_type == "Systematic":
            if self._last_word is None:
                self._last_word = 0
                return  self.words(self._last_word)
            elif self._last_word < self.size:
                self._last_word += 1
                return self.words(self._last_word)
            else:
                return -1
        elif self._gen_type == "Random":
            indx = np.random.randint(self.size, size=1)[0]
            return self.words[indx]
    
    def find_words(self,word_inp):
        if not self._initialized:
            if _compilation:
                input("Error: No words with with size " + str(self.len) + "in the dictionary")
            raise IOError("No words with with size " + str(self.len) + "in the dictionary")
        
        word = "".join(word_inp) # if word was array of characters
        
        if len(word) != self.len:
            if _compilation:
                input("Error: Unable to find word '"+word+"' in class with word"+ 
                          " length "+str(self.len))
            raise IOError("Unable to find word '"+word+"' in class with word"+ 
                          " length "+str(self.len))
        
        #create mask
        indx_rest = []
        char_rest = []
        for count,char in enumerate(list(word)):
            if char != "*":
                indx_rest.append(count)
                char_rest.append(char)
        
        if indx_rest:
            # find words matchig mask
            word_mask  = np.ascontiguousarray(self.words[:,indx_rest])
            mask = "".join(char_rest)
            view_type = "".join(["U",str(len(indx_rest))])
            indx_match = np.where(word_mask.view(view_type) == mask)[0]
            
            if indx_match.size == 0:
                return -1
            else:
                return self.words[indx_match]
        else:
            if self._gen_type == "Random":
                return self.new_word()
            elif self._gen_type == "Systematic":
                return self.words[:]
    
    def randomize_words(self):
        
        # FIXME: Check if dictionary initialized
        
        indx = np.arange(self.size)
        np.random.shuffle(indx)
        self.words[:] = self.words[indx]
        
        
        
        
    
        

class Dictionary():
    """ Class representing word dictionary
    
    """
    
    def __init__(self,gen_type = "Random"):
        self._initialized = False
        self.len = [Dictionaly_length(0),Dictionaly_length(1)]
        self.Nwords = [0,0]
        self.max_len = 1
        self._gen_type = gen_type
        
    def read_database(self,filename):
        fid  = open(filename,"r")
        lines = fid.read().splitlines()
        fid.close()
        
        for string in lines:
            # get rid of white spaces
            word = string.replace(" ", "")
            Nchar = len(word)
            
            # check if dictionary initialized
            if Nchar>self.max_len:
                for ii in range(Nchar - self.max_len):
                    self.max_len += 1
                    self.len.append(Dictionaly_length(self.max_len,gen_type=self._gen_type))
                    self.Nwords.append(0)
            
            self.len[Nchar].add_word(word)
            self.Nwords[Nchar] +=1
        
        self._initialized = True
    
    def find_words(self,word):
        Nchar = len(word) 
        
        if (Nchar > self.max_len) or (self.Nwords[Nchar] == 0):
            if _compilation:
                input("Error: No word of length " + str(Nchar) + " is in the "+
                          "dictionary. Consider extending dictionary or changing"+
                          "the crosword puzzle grid")
            raise IOError("No word of length " + str(Nchar) + " is in the "+
                          "dictionary. Consider extending dictionary or changing"+
                          "the crosword puzzle grid")
        if Nchar == 1:
            pass
        
        dict_len = self.len[Nchar]
        
        if isinstance(dict_len,Dictionaly_length):
            word_suggestions = dict_len.find_words(word)
        else:
            word_suggestions = -1
        
        return word_suggestions
    
    def check_presence(self,word):
        Nchar = len(word) 
        
        if (Nchar > self.max_len) or (self.Nwords[Nchar] == 0):
            if _compilation:
                input("Error: No word of length " + str(Nchar) + " is in the "+
                          "dictionary. Consider extending dictionary or changing"+
                          "the crosword puzzle grid")
            raise IOError("No word of length " + str(Nchar) + " is in the "+
                          "dictionary. Consider extending dictionary or changing"+
                          "the crosword puzzle grid")
        res = self.find_words(word)
        if len(res) == 1:
            return True
    
    def randomize_dictionary(self):
        for ii in range(self.max_len):
            if self.len[ii].size > 1:
                self.len[ii].randomize_words()
        

'''----------------------- TEST PART --------------------------------'''
if __name__=="__main__":

    print('                TESTS')
    print('-----------------------------------------') 
    
    database = Dictionary()
    database.read_database("englishWords.txt")
    words = database.find_words("*il")
    print(words)
    words = database.find_words("ai*")
    print(words)
    words = database.find_words("aid")
    print(words)
    database.len[3].randomize_words()
    words = database.find_words("*i*")
    print(words)
    