# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 12:49:16 2019

@author: Vladislav Sláma
"""
from Grid import Grid
from Words import Word
from Settings import language, _compilation, _gen_type
from Dictionary import Dictionary
import numpy as np

class CrossWord(Grid):
    
    def __init__(self,dict_file):
        self._filed = False
        self.crossword = None
        self._words_init = False
        self.database = Dictionary(gen_type=_gen_type)
        self.database.read_database(dict_file)
        self.database.randomize_dictionary()
        self._current = 0
    
    def initialize_grid(self,shape, wtsp=None, shortest=2):
        super().__init__(shape, wtsp=wtsp, shortest=shortest)
        self.crossword = np.chararray(shape,itemsize=1,unicode=True)
        
        self.crossword[:] = "*"
        
        # set whitespaces
        if isinstance(wtsp,list):
            for coor in wtsp:
                self.crossword[coor[0],coor[1]] = "-"
        
        self.identify_words()
        self.init_words()
        self.get_connected_words()
    
    def init_words(self,words = None):
        if words is None:
            word_list = []
            for ii in range(self.Nwords):
                new_word = Word(self.database)
                new_word.init_by_index(ii, self.word2coor, self.word_len)
                word_list.append(new_word)
            self.words = word_list
        
        elif isinstance(words,list):
            self.words = words
        
        else:
            raise IOError("Words should be specified as list of words")
        
        self.Nwords = len(word_list)
        self._words_init = True
        
    
#    def fill_word_indx():
    
    def fill_word_coor(self,coor,chars,force=False):
        if not self._words_init:
            self.init_words()
        
        if np.ndim(coor) == 1:
            if len(chars) == 1:
                char_tmp = "".join(chars)
            else:
                raise IOError("Coordinates should have the same dimension as number of characters")
            
            indxes = self.coor2word[coor[0]][coor[1]]
            for indx in indxes:
                #self.words[indx[0]].chars[indx[1]] = char_tmp 
                self.words[indx[0]].set_char(indx[1],char_tmp, force = force)
            
            self.crossword[coor[0]][coor[1]] = char_tmp
        
        elif np.ndim(coor) == 2:
            if len(chars) == len(coor):
                char_tmp = list(chars)
            else:
                raise IOError("Coordinates should have the same dimension as number of characters")
            
            for ii in range(len(coor)):
                indxes = self.coor2word[coor[ii][0]][coor[ii][1]]
            
                for indx in indxes:
                    self.words[indx[0]].chars[indx[1]] = char_tmp[ii] 
                    #self.words[indx[0]].set_char(indx[1],char_tmp, force=force)
                
                self.crossword[coor[ii][0],coor[ii][1]] = char_tmp[ii]
    
    def fill_word_indx(self,indx,word):
        """ Delete characters corresponding to this word but keep characters 
        from all higher level words in order to maintain the restrictions
        """

        chars = list(word)
        coor = self.word2coor[indx]
        
        #print("Starting filling the word")
        self.fill_word_coor(coor,chars)
    
    def empty_word(self,indx,force = False):
        """ Delete characters corresponding to this word but keep characters 
        from all higher level words in order to maintain the restrictions
        """
        
        for coor in self.word2coor[indx]:
            replace = True
            for indx_filled in self.coor2word[coor[0]][coor[1]]:
                if indx_filled[0] < indx:
                    replace = False
            
            if replace:
                self.fill_word_coor(coor,"*",force = force)
            
#        # FIXME: Only allready filled words
#        if force:
#            for ii in self.connected[indx]:
#                if ii > indx:
#                    self.empty_word(ii)
            
    
    def generate_word(self,indx):
        if indx >= self.Nwords:
            if _compilation:
                    input("Generating word with index larger than number of the words")
            raise IOError("Generating word with index larger than number of the words")
        
        word = self.words[indx].get_new_word()
        if word is -1:
            return False
        else:
            self.fill_word_indx(indx,word)
            return True
        
    def is_duplicate(self,indx):
        duplicate = False
        
        word1 = "".join(self.words[indx].chars)
        for ii in range(indx):
            if self.words[ii].len == self.words[indx].len:
                word2 = "".join(self.words[ii].chars)
                if word1 == word2:
                    duplicate = True
        return duplicate
        

            
    def fill(self):
        count = 0
        largest_len = 0
        largest_cross = None
        while not self._filed:
            if (count)//100000 != (count-1)//100000 and count > 1:
                print("Vyzkouseno kombinaci:",count,"Vyplneno slov:",largest_len,"z",self.Nwords)
                print("Nejblizsi k vyplnene krizovce:")
                print(largest_cross)
            count +=1
            
            if self._current < 0:
                if _compilation:
                    input("Unable to fill specified crossword with given dictionary")
                raise IOError("Unable to fill specified crossword with given dictionary")
            
#            print(self._current,self.Nwords)
#            if self.words[self._current]._has_alternatives and self.words[self._current].alternatives is None:
#            print(self.words[self._current].chars,self.words[self._current]._has_alternatives,self.words[self._current].alternatives)
            successfull = self.generate_word(self._current)
            
            if self.is_duplicate(self._current): # when duplicate empty current word and generate again
                self.empty_word(self._current,force=False)
                continue
            
#            print(cross.crossword) 
            
            if successfull:
                self._current += 1
                if self._current == self.Nwords:
                    self._filed = True
                
                if self._current > largest_len:
                    largest_len = self._current
                    largest_cross = self.crossword.copy()
                    
                continue
            
            else:
                # go back to last related word
                # empty all words from current to the closest
                indx_closest = self.closest[self._current]
                for indx in range(indx_closest+1,self._current+1):
                    self.empty_word(indx,force=True)
                self.empty_word(indx_closest,force=False)
                
                self._current = indx_closest
            

            
                
        # FIXME: Check for duplicate words
    
    def check(self, verbose = False):
        # check if all words exists
        state = True
        if verbose:
            if language == "English":
                print("\nChecking the crossword puzzle correctness:")
            elif language == "Czech":
                print("\nKontrola spravnosti vyplneni krizovky:")
            for word in self.words:
                if self.database.check_presence(word.chars):
                    text = "".join(word.chars)
                    if language == "English":
                        print("Word: {:12} found in dictionary".format(text))
                    elif language == "Czech":
                        print("Slovo: {:12} nalezeno v databazi slov.".format(text))
                else:
                    if language == "English":
                        print("Incorrect word: " + text + ". Please report the bug")
                    elif language == "Czech":
                        print("Nespravne slovo: " + text + ". Prosim nahlas chybu autorovi.")
                    state = False
        return state
                
    
    def plot_filled(self,fontsize=20, filename=None):
        import matplotlib.pyplot as plt
    
        black_sp = np.zeros(self.shape)
        for indx in self.wtsp:
            black_sp[indx[0],indx[1]] = 1.0
        
        plt.figure()
        plt.imshow(black_sp, cmap="Greys",extent = [0,self.shape[0],0,self.shape[1]])
        ax = plt.gca()
        ax.axes.set_xticks(np.arange(self.shape[1]+1))
        ax.axes.set_yticks(np.arange(self.shape[0]+1))
        ax.grid(color='k', linestyle='-', linewidth=2)
        ax.axes.get_xaxis().set_ticklabels([])
        ax.axes.get_yaxis().set_ticklabels([])
        
        offset = [0.1,0.7]
        offset_wrd = [0.3,0.2]
        mask = np.ones(self.shape,dtype = bool)
        count = 1
        
        for kk in range(len(self.word2coor)):
            word = self.word2coor[kk]
            start = word[0][:]
            start[0] = self.shape[0] - start[0] - 1  # Reversed numbering of rows
            if mask[start[0],start[1]]:
                #print(count,start,word)
                plt.text(start[1] + offset[0], start[0] + offset[1], str(count))
                mask[start[0],start[1]] = False
                count +=1
            for ii in range(len(word)):
                start = word[ii]
                start[0] = self.shape[0] - start[0] - 1  # Reversed numbering of rows
                char = self.words[kk].chars[ii]
                plt.text(start[1] + offset_wrd[0], start[0] + offset_wrd[1], 
                         char,fontsize=fontsize)
        
        if filename is not None:
            plt.savefig(filename,dpi=1200)
#        plt.show()
            

'''----------------------- TEST PART --------------------------------'''
if __name__=="__main__":

    print('                TESTS')
    print('-----------------------------------------') 
    
    shape = (6,6)
    wtsp = [[0,0],[0,1],[1,3],[1,5],[2,5],[3,1],[4,0],[4,4],[5,3],[5,4]]
    dict_file = "englishWords.txt"
    
#    cross = CrossWord(dict_file)
#    cross.initialize_grid(shape,wtsp=wtsp,shortest=2)
#    
#    print(cross.mask)
#    cross.identify_words()
#    print(cross.word2coor)
#    for ii in range(cross.shape[0]):
#        print(ii,cross.coor2word[ii]) 
#    print(cross.word_len)
#    
#    cross.generate_word(0)
#    print(cross.words[1].chars)
#    cross.generate_word(1)
#    print(cross.words[0].chars)
#    print(cross.words[1].chars)
#    cross.empty_word(1,force=False)
#    print(cross.words[0].chars)
#    print(cross.words[1].chars)
#    print(cross.words[1]._alter_count)
    
    cross = CrossWord(dict_file)
    cross.initialize_grid(shape,wtsp=wtsp,shortest=3)
    cross.fill()
    print(cross.mask)
    print("")
    print(cross.crossword)
    cross.check(verbose = True)
    cross.plot_grid()
    cross.plot_filled()

    