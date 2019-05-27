# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 18:28:05 2019

@author: Vladislav Sláma
"""
import numpy as np
#from Crossword import language

class Grid():
    """ Class representing crossword puzzle grid
    
    """
    
    def __init__(self,shape, wtsp=None, shortest=2):
        # initialize array mask
        self.mask = np.chararray(shape,itemsize=1,unicode=True)
        self.shape = shape
        self.wtsp = wtsp
        self.words = None
        
        # set whitespaces
        if isinstance(wtsp,list):
            for coor in wtsp:
                self.mask[coor[0],coor[1]] = "W"
        
        self._find_word_start(shortest=shortest)
        
    def _find_word_start(self,shortest = 2):
        self.shortest = shortest
        
        for row in range(self.mask.shape[0]):
            count_row = 0
            for col in range(self.mask.shape[1]-shortest+1):
                if self.mask[row,col] == "W":
                    count_row = 0
                    continue
                elif (count_row == 0):
                    new_word = True
                    for kk in range(col+1,min(self.mask.shape[1],col+shortest)):
                        if self.mask[row,kk] == "W":
                            new_word = False
                    if new_word:
                        self.mask[row,col] = "-"
                    count_row += 1
                else:
                    count_row += 1
        
        for col in range(self.mask.shape[1]):
            count_col = 0
            for row in range(self.mask.shape[0]-shortest+1):
                if self.mask[row,col] == "W":
                    count_col = 0
                    continue
                elif (count_col == 0): 
                    new_word = True
                    for kk in range(row+1,min(self.mask.shape[0],row+shortest)):
                        if self.mask[kk,col] == "W":
                            new_word = False
                    if new_word == True:
                        if self.mask[row,col] == "-":
                            self.mask[row,col] = "+"
                        else:
                            self.mask[row,col] = "|"
                    count_col += 1
                else:
                    count_col += 1
    
    def reset_grid(self,wtsp=None):
        self.mask = np.chararray(self.shape,itemsize=1,unicode=True)
        
        if wtsp is not None:
            self.wtsp = wtsp
            
        # set whitespaces
        if isinstance(self.wtsp,list):
            for coor in self.wtsp:
                self.mask[coor[0],coor[1]] = "W"
    
    
        
    def identify_words(self):
        word_coor = []
        word_count = 0
        
        # identify words in rows
        for row in range(self.mask.shape[0]):
            _is_word = False
            for col in range(self.mask.shape[1]):
                if self.mask[row,col] in ['+','-']:
                    _is_word = True
                    word_coor.append([[row,col]])
                elif self.mask[row,col] == "W":
                    if _is_word:
                        word_count += 1
                    _is_word = False
                elif _is_word:
                    word_coor[word_count].append([row,col])
            if _is_word:
                word_count += 1
                _is_word = False
        
        # identify words in columns
        for col in range(self.mask.shape[1]):
            _is_word = False
            for row in range(self.mask.shape[0]):
                if self.mask[row,col] in ['+','|']:
                    _is_word = True
                    word_coor.append([[row,col]])
                elif self.mask[row,col] == "W":
                    if _is_word:
                        word_count += 1
                    _is_word = False
                elif _is_word:
                    word_coor[word_count].append([row,col])
            if _is_word:
                word_count += 1
                _is_word = False
                
        self.word2coor = word_coor.copy()
        self.Nwords = word_count            
        
        # calculate word lengths 
        self.word_len = []
        for ii in range(self.Nwords):
            Nchar = len(word_coor[ii])
            self.word_len.append(Nchar)
        
        
        
        # sort according to size
        indx_sorted = np.argsort(-np.array(self.word_len))
        self.word2coor = [self.word2coor[i] for i in indx_sorted]
        self.word_len = [self.word_len[i] for i in indx_sorted]
        
        
        # this should be done after sorting the arrays
        # init word grid
        coor_word = []
        for row in range(self.shape[0]):
            coor_word.append([])
            for col in range(self.shape[1]):
                coor_word[row].append([])
        # fill word grid
        for ii in range(self.Nwords):
            for jj in range(len(self.word2coor[ii])):
                coor = self.word2coor[ii][jj]
                coor_word[coor[0]][coor[1]].append([ii,jj])
        self.coor2word = coor_word.copy()
    
    def get_connected_words(self):
        connected = []
        closest = np.zeros(len(self.word_len),dtype="i4")
        for ii in range(len(self.word_len)):
            connected.append([])
        
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                indx = self.coor2word[row][col]
                if len(indx) == 2:
                    connected[indx[0][0]].append(indx[1][0])
                    connected[indx[1][0]].append(indx[0][0])
        
        # sort array of connected words:
        for ii in range(len(self.word_len)):
            connected[ii] = np.sort(connected[ii])
            
            
        
        self.connected = connected
        
        for ii in range(len(self.word_len)):
            for conn_indx in self.connected[ii]:
                if conn_indx < ii:
                    closest[ii]=conn_indx
        self.closest = closest
                    
        
    def plot_grid(self, filename=None):
        import matplotlib.pyplot as plt
    
        black_sp = np.zeros(self.shape)
        for indx in self.wtsp:
            black_sp[indx[0],indx[1]] = 1.0
        

        plt.imshow(black_sp, cmap="Greys",extent = [0,self.shape[0],0,self.shape[1]])
        ax = plt.gca()
        ax.axes.set_xticks(np.arange(self.shape[1]+1))
        ax.axes.set_yticks(np.arange(self.shape[0]+1))
        ax.grid(color='k', linestyle='-', linewidth=2)
        ax.axes.get_xaxis().set_ticklabels([])
        ax.axes.get_yaxis().set_ticklabels([])
        
        offset = [0.1,0.7]
        mask = np.ones(self.shape,dtype = bool)
        count = 1
        for word in self.word2coor:
            start = word[0][:]
            start[0] = self.shape[0] - start[0] - 1  # Reversed numbering of rows
            if mask[start[0],start[1]]:
                #print(count,start,word)
                plt.text(start[1] + offset[0], start[0] + offset[1], str(count))
                mask[start[0],start[1]] = False
                count +=1
        
        if filename is not None:
            plt.savefig(filename,dpi = 1200)
#        plt.show()
        
def write_grid(filename,shape,language = "English"):
    with open(filename,"wt") as f:
        if language == "English": 
            f.write("Generated empty grid of shape: {:}x{:} \n".format(shape[0],shape[1]))
            f.write("Position with black squares are marked by replacing _ with W.\n\n")
        elif language == "Czech" :
            f.write("Vygenerovana mrizka krizovky o rozmerech: {:}x{:} \n".format(shape[0],shape[1]))
            f.write("Oznacte pozice cernych (prazdnych) ctvercu prepsanim _ za W.\n\n")
        for col in range(shape[1]):
            f.write("##")
        f.write("#\n")
        for row in range(shape[0]):
            f.write("#")
            for col in range(shape[1]-1):
                f.write("_|")
            f.write("_#\n") 
        for col in range(shape[1]):
            f.write("##")
        f.write("#\n")
                
def read_grid(filename):
    fid = open(filename,"r")
    lines = fid.read().splitlines()
    fid.close()
    
    # determine shape:
    line = lines[0].replace(" ", "")
    thisline = line.split(":")
    shape_string = thisline[-1].split("x")
    shape = (int(shape_string[0]),int(shape_string[1]))
    #print(shape)
    
    wtsp = []
    
    for ii in range(4,4+shape[0]):
        line = lines[ii]
        row = ii - 4
        thisline = line.split("#")[1].split("|")
        #print(thisline)
        for col in range(shape[1]):
            if thisline[col] == "W":
                wtsp.append([row,col])
    return shape,wtsp
                
        #for col
#                
#        for row in range(self.shape[0]):
#            for col in range(self.shape[1]):
#                indx = self.coor2word[row][col]
#                
#        plt.text(2.1, 5.7, "1")
    
#    def fill_grid(self,coor,chars):
#        if np.ndim(coor) == 1:
            
        
        
        
        
        

'''----------------------- TEST PART --------------------------------'''
if __name__=="__main__":

    print('                TESTS')
    print('-----------------------------------------') 
    
    shape = (6,6)
    wtsp = [[0,0],[0,1],[1,3],[1,5],[2,5],[3,1],[4,0],[4,4],[5,3],[5,4]]
    
    grid = Grid(shape,wtsp=wtsp,shortest=2)
    print(grid.mask)
    grid.identify_words()
    print(grid.word2coor)
    for ii in range(grid.shape[0]):
        print(ii,grid.coor2word[ii]) 
    print(grid.word_len)
    input("Input crossword puzzle grid shape in form (dim1,dim2) (e.g. (4,3) for grid 4x3): ")
    shape = write_grid("TEST_grid.txt",shape)
    input("Change chrossword puzzle grid and press enter: ")
    shape,wtsp_new = read_grid("TEST_grid.txt")
    print(wtsp_new)

