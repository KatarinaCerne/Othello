from tkinter import *
import threading

def drugi(igr):
    if igr == "Črni":
        return "Beli"
    else:
        return "Črni"

class Othello:
    def __init__(self, master):

##        root.title('Othello')
##
##        okvir = Frame(root, padx=10, pady=10)
##        okvir.configure(background="#F2F7BB")
##        okvir.grid(column=0, row=0)

        menu = Menu(master)
        master.config(menu=menu)

##        meni = Menu(menu)
##        menu.add_cascade(label="Igra", menu=meni)
##        igra_menu.add_command(label="Črni=Človek, Beli=Človek", command=lambda: self.igra("človek", "človek"))
##        igra_menu.add_command(label="Črni=Človek, Beli=Računalnik", command=lambda: self.igra("človek", "računalnik"))
##        igra_menu.add_command(label="Črni=Računalnik, Beli=Človek", command=lambda: self.igra("računalnik", "človek"))
##        igra_menu.add_command(label="Črni=Računalnik, Beli=Računalnik", command=lambda: self.igra("računalnik", "računalnik"))

##        menu.add_command(label="Izhod", command=self.zapri)

        self.na_potezi = None

        self.crni = 'človek'
        self.beli = 'človek'

        self.napis = StringVar(master, value="Začnimo.")
        Label(master, textvariable=self.napis).grid(row=0, column=0)

        self.canvas = Canvas(master, width=800, height=800)
        self.canvas.grid(row=1, column=0, columnspan=2)
        self.canvas.bind('<Button-1>', self.klik)

        self.polje = [[None for i in range(8)] for j in range(8)]

        self.igra('človek', 'človek')

    def igra(self, crni, beli):
        self.crni = crni
        self.beli = beli

        self.na_potezi = "Črni"
        self.napis.set("Na potezi je črni.")
        
        self.canvas.delete(ALL)
        self.canvas.create_line(100,0,100,800)
        self.canvas.create_line(200,0,200,800)
        self.canvas.create_line(300,0,300,800)
        self.canvas.create_line(400,0,400,800)
        self.canvas.create_line(500,0,500,800)
        self.canvas.create_line(600,0,600,800)
        self.canvas.create_line(700,0,700,800)
        self.canvas.create_line(0,100,800,100)
        self.canvas.create_line(0,200,800,200)
        self.canvas.create_line(0,300,800,300)
        self.canvas.create_line(0,400,800,400)
        self.canvas.create_line(0,500,800,500)
        self.canvas.create_line(0,600,800,600)
        self.canvas.create_line(0,700,800,700)

    def odigraj(self, i, j):
        if self.polje[i][j] is None:
            self.polje[i][j] = self.na_potezi
            if self.na_potezi == "Črni":
                self.narisiCrnega(i,j)
            else:
                self.narisiBelega(i,j)
            self.na_potezi = drugi(self.na_potezi)
            self.napis.set("Na potezi je " + self.na_potezi)


    def klik(self, event):
        if ((self.na_potezi == "Črni" and self.crni == "človek") or
            (self.na_potezi == "Beli" and self.beli == "človek")):
            i = int(event.x / 100)
            j = int(event.y / 100)
            self.odigraj(i, j)
                
    def narisiCrnega(self, i, j):
        x = i * 100
        y = j * 100
        self.canvas.create_oval(x+5, y+5, x+95, y+95, fill="black")

    def narisiBelega(self, i, j):
        x = i * 100
        y = j * 100
        self.canvas.create_oval(x+5, y+5, x+95, y+95)

##    for otrok in okvir.winfo_children():
##        otrok.grid_configure(padx=4, pady=2)
   

master = Tk()
Othello(master)
master.resizable(width=FALSE, height=FALSE) 
master.mainloop()       

        
