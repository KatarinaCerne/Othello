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

        meni = Menu(menu)
        menu.add_cascade(label="Igra", menu=meni)
        meni.add_command(label="Črni=Človek, Beli=Človek", command=lambda: self.igra("človek", "človek"))
        meni.add_command(label="Črni=Človek, Beli=Računalnik", command=lambda: self.igra("človek", "računalnik"))
        meni.add_command(label="Črni=Računalnik, Beli=Človek", command=lambda: self.igra("računalnik", "človek"))
        meni.add_command(label="Črni=Računalnik, Beli=Računalnik", command=lambda: self.igra("računalnik", "računalnik"))

##        menu.add_command(label="Izhod", command=self.zapri)

        self.na_potezi = None

        self.crni = 'človek'
        self.beli = 'človek'

        self.napis = StringVar(master, value="Začnimo.")
        Label(master, textvariable=self.napis).grid(row=0, column=0)

        self.canvas = Canvas(master, width=400, height=400)
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
        self.canvas.create_line(50,0,50,400)
        self.canvas.create_line(100,0,100,400)
        self.canvas.create_line(150,0,150,400)
        self.canvas.create_line(200,0,200,400)
        self.canvas.create_line(250,0,250,400)
        self.canvas.create_line(300,0,300,400)
        self.canvas.create_line(350,0,350,400)
        self.canvas.create_line(0,50,400,50)
        self.canvas.create_line(0,100,400,100)
        self.canvas.create_line(0,150,400,150)
        self.canvas.create_line(0,200,400,200)
        self.canvas.create_line(0,250,400,250)
        self.canvas.create_line(0,300,400,300)
        self.canvas.create_line(0,350,400,350)

        self.canvas.create_oval(150+5, 150+5, 150+45, 150+45, fill="black")
        self.canvas.create_oval(200+5, 200+5, 200+45, 200+45, fill="black")
        self.canvas.create_oval(200+5, 150+5, 200+45, 150+45)
        self.canvas.create_oval(150+5, 200+5, 150+45, 200+45)

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
            i = int(event.x / 50)
            j = int(event.y / 50)
            self.odigraj(i, j)
                
    def narisiCrnega(self, i, j):
        x = i * 50
        y = j * 50
        self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="black")

    def narisiBelega(self, i, j):
        x = i * 50
        y = j * 50
        self.canvas.create_oval(x+5, y+5, x+45, y+45)

##    for otrok in okvir.winfo_children():
##        otrok.grid_configure(padx=4, pady=2)
   

master = Tk()
Othello(master)
master.resizable(width=FALSE, height=FALSE) 
master.mainloop()       

        
