from tkinter import *
from zacetek import *

class Othello:
 

    def __init__(self, root):
        root.title('Othello')

        okvir = Frame(root, padx=10, pady=10)
        okvir.configure(background="#59BD7A")
        okvir.grid(column=0, row=0)

##        seznam = [[Button(okvir, bg="green", width=3) for x in range(6)] for y in range(6)]
##        x = 0
##        y = 0
##        for podsez in seznam:
##            for el in podsez:
##                el.grid(column=x, row=y)
##                x=x+1
##            y=y+1
##            x=0
        for x in range(6):
            for y in range(6):
                Button(okvir, bg="green", width=3).grid(column=x+1, row=y+1)

    
        for otrok in okvir.winfo_children():  
            otrok.grid_configure(padx=4, pady=2)
        
master = Tk()
Othello(master)
master.resizable(width=FALSE, height=FALSE) 
master.mainloop()    
