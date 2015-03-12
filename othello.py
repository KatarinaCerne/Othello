from tkinter import *
import threading

def drugi(igr):
    if igr == "Črni":
        return "Beli"
    else:
        return "Črni"

def veljavna(barva, di, dj, polje, i, j):
    """Če je poteza veljavna, vrne True, sicer vrne False"""
    k=1
    while polje[i+k*di][j+k*dj] == drugi(barva):
        if (i+k*di,di) == (7,1) or (i+k*di,di) == (0,-1) or (j+k*dj,dj) == (7,1) or (j+k*dj,dj) == (0,-1):
            return False
        k+=1
    if polje[i+k*di][j+k*dj] == barva:
        return True
    else:
        return False

def seznam_sosedov(i, j) :
    """Vrne seznam sosedov polja s koordinatami (i,j)"""
    if i == 0:
        if j == 0:
            return [[i+1,j],[i+1,j+1],[i,j+1]]
        elif j == 7:
            return [[i+1,j],[i+1,j-1],[i,j-1]]
        else:
            return [[i,j-1],[i+1,j-1],[i+1,j],[i+1,j+1],[i,j+1]]
    elif i == 7:
        if j == 0:
            return [[i-1,j],[i-1,j+1],[i,j+1]]
        elif j == 7:
            return [[i-1,j],[i-1,j-1],[i,j-1]]
        else:
            return [[i,j-1],[i-1,j-1],[i-1,j],[i-1,j+1],[i,j+1]]
    else:
        if j == 0:
            return [[i-1,j],[i-1,j+1],[i,j+1],[i+1,j+1],[i+1,j]]
        elif j == 7:
            return [[i-1,j],[i-1,j-1],[i,j-1],[i+1,j-1],[i+1,j]]
        else:
            return [[i-1, j],[i+1, j],[i-1,j+1],[i,j+1],[i+1,j+1],[i-1,j-1],[i,j-1],[i+1,j-1]]

def ni_poteze(barva, polje):
    for i,st in enumerate(polje):
            for j,vr in enumerate(st):
                if vr != None:
                    pass
                else:
                    for el in seznam_sosedov(i, j):
                        i1 = el[0]
                        j1 = el[1]
                        di = i1-i
                        dj = j1-j
                        if veljavna(barva, di, dj, polje, i, j):
                            return False
                        else:
                            pass
    return True

class Othello:
    def __init__(self, master):

        master.title('Othello')

        #meni#
        menu = Menu(master)
        master.config(menu=menu)

        meni = Menu(menu)
        menu.add_cascade(label="Igra", menu=meni)
        meni.add_command(label="Črni=Človek, Beli=Človek", command=lambda: self.igra("človek", "človek"))
        meni.add_command(label="Črni=Človek, Beli=Računalnik", command=lambda: self.igra("človek", "računalnik"))
        meni.add_command(label="Črni=Računalnik, Beli=Človek", command=lambda: self.igra("računalnik", "človek"))
        meni.add_command(label="Črni=Računalnik, Beli=Računalnik", command=lambda: self.igra("računalnik", "računalnik"))

        menu.add_command(label="Izhod", command=self.zapri)
        ######
        
        self.na_potezi = None

        self.crni = 'človek'
        self.beli = 'človek'

        self.mislec = None        
        self.mislec_poteza = None 
        self.mislec_stop = False

        self.napis = StringVar(master, value="Začnimo.")
        Label(master, textvariable=self.napis,font=("Tahoma", 14)).grid(row=0, column=0,sticky=W)

        #število crnih in belih ploščic, ki so na polju
        self.stejcrne = 2
        self.stejbele = 2

        self.napiscrni = StringVar(master, value="")
        self.napisbeli = StringVar(master, value="")
        Label(master, textvariable=self.napiscrni,font=("Tahoma", 14)).grid(row=3, column=0,sticky=W)
        Label(master, textvariable=self.napisbeli,font=("Tahoma", 14)).grid(row=3, column=1,sticky=E)

        self.canvas = Canvas(master, width=400, height=400, background="#97CAB1")
        self.canvas.grid(row=2, column=0, columnspan=2)
        self.canvas.bind('<Button-1>', self.klik)

        #seznam, ki vsebuje elemente "None"(prazno polje), "Črni" in "Beli"
        self.polje = [[None for i in range(8)] for j in range(8)]
        #seznam, ki vsebuje krogce(žetone)
        self.zetoni = [[None for i in range(8)] for j in range(8)]

        self.igra('človek', 'človek')

    def zapri(self):
        if self.mislec != None:
            self.mislec_stop = True
            self.mislec.join()
        self.canvas.master.destroy()

    def konec_igre(self):
        '''Ugotovi, ali je konec igre. Vrne None (igre ni konec),
           niz 'neodločeno' (rezultat je neodločen), ali pa zmagovalca'''
        if self.stejcrne == 0:
            return "Beli"
        elif self.stejbele == 0:
            return "Èrni"
        else:           
            if self.stejcrne + self.stejbele == 64:     
                if self.stejcrne > self.stejbele:
                    return "Èrni"
                elif self.stejbele >self.stejcrne:
                    return "Beli"
                else:
                    return "Neodloèeno"
            else:
                return None

    def igra(self, crni, beli):
        #nariše polje in nastavi igro na zacetek
        self.crni = crni
        self.beli = beli

        if self.mislec != None:
            self.mislec_stop = True
            self.mislec.join()

        #seznam, ki vsebuje elemente "None"(prazno polje), "Črni" in "Beli"
        self.polje = [[None for i in range(8)] for j in range(8)]
        #seznam, ki vsebuje krogce(žetone)
        self.zetoni = [[None for i in range(8)] for j in range(8)]

        self.stejcrne = 2
        self.stejbele = 2       

        #nastavi, da začne črni
        self.na_potezi = "Črni"
        self.napis.set("Na potezi je črni.")

        #nastavi napise za število črnih/belih žetonov
        self.napiscrni.set("Črni: "+str(self.stejcrne))
        self.napisbeli.set("Beli: "+str(self.stejbele))
        
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
        self.canvas.create_oval(200+5, 150+5, 200+45, 150+45, fill="white")
        self.canvas.create_oval(150+5, 200+5, 150+45, 200+45, fill="white")
        self.zetoni[3][3]=self.canvas.create_oval(150+5, 150+5, 150+45, 150+45, fill="black")
        self.zetoni[4][4]=self.canvas.create_oval(200+5, 200+5, 200+45, 200+45, fill="black")
        self.zetoni[4][3]=self.canvas.create_oval(200+5, 150+5, 200+45, 150+45, fill="white")
        self.zetoni[3][4]=self.canvas.create_oval(150+5, 200+5, 150+45, 200+45, fill="white")
        self.polje[3][3] = "Črni"
        self.polje[4][4] = "Črni"
        self.polje[3][4] = "Beli"
        self.polje[4][3] = "Beli"

        
        if self.crni == 'računalnik':
            self.racunalnik_odigraj_potezo()

    def odigraj(self, i, j):
        #če je polje prazno in poteza veljavna, se poteza odigra
        seznam_veljavnosti=[veljavna(self.na_potezi,el[0]-i,el[1]-j,self.polje,i,j) for el in seznam_sosedov(i,j)
                            if self.na_potezi != self.polje[el[0]][el[1]] and self.polje[el[0]][el[1]] != None]
        
        if self.polje[i][j] is None and True in seznam_veljavnosti:
            self.polje[i][j] = self.na_potezi
            if self.na_potezi == "Črni":
                self.narisiCrnega(i,j)
            else:
                self.narisiBelega(i,j)
            self.preobrni(i,j)
            self.na_potezi = drugi(self.na_potezi)
            self.napis.set("Na potezi je " + self.na_potezi)
            self.napiscrni.set("Črni: "+str(self.stejcrne))
            self.napisbeli.set("Beli: "+str(self.stejbele))

            r = self.konec_igre()
            if r == "Neodloèeno":
                self.na_potezi = None
                self.napis.set("Neodločeno")
            elif r is not None:
                self.napis.set('Zmagal je ' + r)
            else:
                # Preverimo, ali mora računalnik odigrati potezo
                if ((self.na_potezi == 'X' and self.igralec_x == 'računalnik') or
                    (self.na_potezi == 'O' and self.igralec_o == 'računalnik')):
                    # Namesto, da bi neposredno poklicali self.racunalnik_odigraj_potezo,
                    # to naredimo z zamikom, da se lahko prejšnja poteza sploh nariše.
                    self.canvas.after(100, self.racunalnik_odigraj_potezo)

    
    def racunalnik_odigraj_potezo(self):
        '''Računalnik odigra naslednjo potezo.'''
        # Naredimo vzporedno vlakno
        self.mislec_poteza = None
        self.mislec_stop = False
        self.mislec = threading.Thread(target=self.razmisljaj)
        # Poženemo vzporedno vlakno
        self.mislec.start()
        # Čez 0.1 sekunde preverimo, ali je self.mislec končal
        self.canvas.after(100, self.mislec_preveri_konec)

    def razmisljaj(self):
        (p, vrednost_p) = self.minimax(9)
        self.mislec_poteza = p
        self.mislec = None

    def mislec_preveri_konec(self):
        if self.mislec_poteza == None:
            # self.mislec ni končal, preverimo še enkrat čez 0.1 sekunde
            self.canvas.after(100, self.mislec_preveri_konec)
        else:
            # self.mislec je končal, povlečemo potezo
            (i,j) = self.mislec_poteza
            self.odigraj_potezo(i,j)

    def vrednost(self):
        '''Oceni vrednost pozicije za igralca. Ta ocena je hevristična (ni nujno pravilna).'''
        # Denimo, da imamo
        #  3 = igralec ima trojko (je zmagal)
        #  2 = igralec ima dvojko (in nima trojke)
        #  1 = igralec ima enojko (in nima dvojke ali trojke)
        #  0 = nihče nima ničesar
        # -1 = nasprotnik ima enojko
        # -2 = nasprotnik ima dvojko
        # -3 = nasprotnik ima trojko
        igralec = self.na_potezi
        nasprotnik = drugi_igralec(self.na_potezi)
        max_igralec = 0 # Največ, kar ima v tej poziciji igralec
        max_nasprotnik = 0 # Največ, kar ima v tej poziciji nasprotnik
        for t in trojke:
            # Za vsako trojko preštejemo, koliko je v njej znakov igralca in koliko znakov nasprotnika
            igr = 0
            nas = 0
            for (i,j) in t:
                if self.polje[i][j] == igralec: igr = igr + 1
                if self.polje[i][j] == nasprotnik: nas = nas + 1
            if nas == 0: max_igralec = max(igr, max_igralec)
            if igr == 0: max_nasprotnik = max(nas, max_nasprotnik)
        if max_igralec >= max_nasprotnik:
            return max_igralec
        else:
            return -max_nasprotnik

    def minimax(self,globina):
        # Preverimo, ali je treba končati z razmišljanjem
        if self.mislec_stop: return (None, 0)
        if globina == 0 or self.konec_igre() != None:
            # Dosegli smo globino 0 ali pa je konec igre, vrnemo oceno za vrednost
            return (None, self.vrednost())
        else:
            # Za vsako možno potezo ocenimo, koliko je vredna.
            # Izberemo najboljšo potezo.
            p = None # Najboljša do sedaj videna poteza
            vrednost_p = -4   # Manj kot najmanjša možna vrednost pozicije
            for i in (0,1,2):
                for j in (0,1,2):
                    if self.polje[i][j] == None:
                        # Polje (i,j) ni zasedeno, lahko igramo
                        # Naredimo potezo (i,j) in ocenimo rekurzivno
                        self.polje[i][j] = self.na_potezi
                        self.na_potezi = drugi_igralec(self.na_potezi)
                        (q, vrednost_q) = self.minimax(globina-1)
                        # Izničimo potezo (i,j)
                        self.polje[i][j] = None
                        self.na_potezi = drugi_igralec(self.na_potezi)
                        vrednost_q = -vrednost_q
                        if vrednost_q > vrednost_p:
                            # Ta poteza je boljša od poteze p
                            p = (i,j)
                            vrednost_p = vrednost_q
            return (p, vrednost_p)


    def klik(self, event):
        #ko klikneš, se odigra poteza
        if ((self.na_potezi == "Črni" and self.crni == "človek") or
            (self.na_potezi == "Beli" and self.beli == "človek")):
            i = int(event.x / 50)
            j = int(event.y / 50)
            self.odigraj(i, j)
                
    def narisiCrnega(self, i, j):
        #doda črn žeton
        x = i * 50
        y = j * 50
        self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="black")
        self.stejcrne+=1
        self.zetoni[i][j] = self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="black")

    def narisiBelega(self, i, j):
        #doda bel žeton
        x = i * 50
        y = j * 50
        self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="white")
        self.stejbele+=1
        self.zetoni[i][j] = self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="white")


    def preobrni(self, i, j):
        #spremeni barve žetonov
        barva = self.na_potezi
        seznam = seznam_sosedov(i, j)
        for el in seznam:
            i1 = el[0]
            j1 = el[1]
            if barva == self.polje[i1][j1] or self.polje[i1][j1] == None:
                pass
            else:
                di = i1-i
                dj = j1-j
                k=1
                if veljavna(barva, di, dj, self.polje, i, j):
                    while self.polje[i+k*di][j+k*dj] == drugi(barva):
                        self.polje[i+k*di][j+k*dj] = barva
                        if barva == "Beli":
                            self.canvas.itemconfig(self.zetoni[i+k*di][j+k*dj], fill="white")
                            self.stejcrne-=1
                            self.stejbele+=1
                        else:
                            self.canvas.itemconfig(self.zetoni[i+k*di][j+k*dj], fill="black")
                            self.stejcrne+=1
                            self.stejbele-=1
                        k += 1
                else:
                    pass
    def preskok(self):
        if ni_poteze(barva, polje):
           self.na_potezi = drugi(self.na_potezi) 

                    
master = Tk()
aplikacija = Othello(master)
master.resizable(width=FALSE, height=FALSE) 
master.mainloop()       

        
