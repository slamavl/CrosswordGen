# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 20:10:55 2019

@author: Vladislav Sláma
"""

from Crossword import CrossWord
from Settings import language,dict_file
from Grid import write_grid, read_grid

cross = CrossWord(dict_file)

if language == "English":
    text = ["Do you wish to generate new crossword grid file (yes/no): "]
    text.append("Input crossword puzzle grid shape in form dim1xdim2 (e.g. 4x3): ")
    text.append("Now you should change the grid in the file Grid.txt according to your wishes.")
    text.append("Change chrossword puzzle grid and press enter: ")
    text.append("Specify length of shortest possible word in cossword: ")
    text.append("Crossword succesfully generated. Press eneter to finish.")
elif language == "Czech":
    text = ["Vygenerovat novou mrizku pro krizovku (stavajici bude prepsana) (ano/ne): "]
    text.append("Vloz velikost mrizky pro krizovku ve tvaru dim1xdim2 (napr. 4x3): ")
    text.append("Nyni muzete upravit mrizku v souboru Grid.txt podle vasich predstav.")
    text.append("Zmen mrizku a potom stiskni enter: ")
    text.append("Zadej delku nejkratsiho slova pro krizovku (zalezi na pouzitem slovniku): ")
    text.append("Krizovka vygenerovana. Stiskni Enter pro ukonceni. ")

_new = input(text[0])
if _new == "yes" or _new == "ano":
    shape = input(text[1])
    shape = shape.replace(" ", "")#.replace('(', "").replace(')', "")
    shape = shape.split("x")
    shape = (int(shape[0]),int(shape[1]))
    write_grid("Grid.txt",shape,language=language)
    print(text[2])
    input(text[3])
shortest = input(text[4])
shortest = int(shortest) 
shape,wtsp= read_grid("Grid.txt")
cross.initialize_grid(shape,wtsp=wtsp,shortest=shortest)
if language == "English":
    first_word = input("Input the first word of len " + 
                       str(cross.words[0].len) + " (if not specified random " +
                       "word will be used): ")
elif language == "Czech":
    first_word = input("Zadej prvni slovo krizovky delky " + 
                   str(cross.words[0].len) + " (pokud nechas prazdne tak " +
                   "bude pouzito nahodne slovo): ")
if len(first_word) == 0:
    first_word = None
cross.fill(first_word=first_word)
#    print(cross.mask)
#    print("")
#    print(cross.crossword)
cross.check(verbose = True)
if first_word is None:
    cross.plot_grid(filename='Crossword_empty.png')
    cross.plot_filled(filename='Crossword_filled.png')
else:
    cross.plot_grid(filename='Crossword_empty.png',res_highlight=True)
    cross.plot_filled(filename='Crossword_filled.png',res_highlight=True)
shortest = input(text[5])