from tkinter import *
import threading
from alphabeta import Alphabeta

POS_INFINITY = 100000000000
NEG_INFINITY = -POS_INFINITY

BELI = "Beli"
CRNI = "Črni"

navodila = ["Othello ali reversi je strateška igra na igralni deski z 8 × 8 polji, kot pri šahovnici ",
            "za dva igralca. Igralca potrebujeta za igro črne in bele figure.\n\n", "Pravila igre:\n\n",
            "Na začetku ima vsak izmed igralcev na plošči dva žetona. ", "Igralca nato izmenično polagata žetone na ploščo. ",
            "Pri vsaki potezi mora biti žeton postavljen poleg nasprotnikovega žetona (lahko vodoravno, navpično ali diagonalno). ",
            "Položeni žeton mora v vsaki potezi ujeti enega ali več nasprotnikovih žetonov med enega ali več svojih žetonov, ",
            "ki so položeni v katerikoli smeri od pravkar položenega. ",
            "Ujetim nasprotnikovim žetonom igralec tako spremeni barvo. ",
            "Če igralec, ki pride na potezo, ne more storiti ničesar (t.j. ne more ujeti nasprotnikovih žetonov med dva svoja), ",
            "mora prepustiti potezo nasprotniku. " "Igralca nadaljujeta s postopkom igranja, dokler ne zapolnita vseh polj, ",
            "ali dokler se ne zgodi, da nobeden izmed njiju ne more narediti veljavne poteze.\n\n",
            "Za pomoč so v aplikaciji polja, kamor je možno postaviti žeton, označena z zeleno piko.\n\n",
            "Namig:\n\n", "Žetona, ki je postavljen v kot igralne deske, nasprotni igralec ne more ujeti oz. mu spremeniti barvo.",
            "Zato je priporočljivo zasesti čimveč kotov.", "Dobre so tudi pozicije ob robovih."]
  

HEVRISTIKA = [[20, -3, 11, 8, 8, 11, -3, 20],
              [-3, -7, -4, 1, 1, -4, -7, -3],
              [11, -4, 2, 2, 2, 2, -4, 11],
              [8, 1, 2, 1, 1, 2, 1, 8],
              [8, 1, 2, 1, 1, 2, 1, 8],
              [11, -4, 2, 2, 2, 2, -4, 11],
              [-3, -7, -4, 1, 1, -4, -7, -3],
              [20, -3, 11, 8, 8, 11, -3, 20]]


def drugi(igr):
    if igr == CRNI:
        return BELI
    else:
        return CRNI

def veljavna(barva, di, dj, polje, i, j):
    """Če je poteza v smeri (di,dj) na polju (i,j) veljavna, vrne True, sicer vrne False"""
    #parametra di in dj predstavljata spremembo koordinate i in koordinate j
    #npr. če je di==1 in dj==1, se pomikamo po diagonali proti desnemu spodnjemu
    #robu plošče in preverjamo, ali je v tej smeri poteza veljavna
    k = 1
    while (0 <= i + k * di <= 7) and (0 <= j + k * dj <= 7) and polje[i+k*di][j+k*dj] == drugi(barva):
        k += 1
    if (0 <= i +k * di <= 7) and (0 <= j + k * dj <= 7):
        return polje[i+k*di][j+k*dj] == barva and k>1
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

class Igra():
    """Razred, ki predstavlja trenutno stanje igre."""
    def __init__(self):
        self.na_potezi = CRNI # kdo je na potezi
        
        #število črnih/belih ploščic, ki so na polju
        self.stejcrne = 2
        self.stejbele = 2

        self.vrednost_crnih = 2
        self.vrednost_belih = 2

        self.crni = 'človek' #kdo je črni
        self.beli = 'človek' #kdo je beli

        self.slovar = {CRNI:self.crni, BELI:self.beli}

        self.pass_poteze = 0
        
        #seznam, ki vsebuje elemente "None"(prazno polje), CRNI in BELI
        self.polje = [[None for i in range(8)] for j in range(8)]
        #začetne žetone doda v self.polje
        self.polje[3][3] = CRNI
        self.polje[4][4] = CRNI
        self.polje[3][4] = BELI
        self.polje[4][3] = BELI
        self.prejsnja_stanja = []

    def __repr__(self):
        s = ""
        for j in range(8):
            t = ""
            for i in range(8):
                c = self.polje[i][j]
                if c == CRNI: t += " X "
                elif c == BELI: t += " O "
                else: t += " . "
            s += t + "\n"
        return ("\nNa potezi je {0}.\nbele = {1}, crne = {2}\nprejsnja_stanja = {3}\n{4}".format(
              self.na_potezi, self.stejbele, self.stejcrne, len(self.prejsnja_stanja),s))

    def konec(self):
        '''Ugotovi, ali je konec igre. Vrne None (igre ni konec),
           niz 'Neodločeno' (rezultat je neodločen), ali pa zmagovalca.'''

        if self.poteze(CRNI)== self.poteze(BELI)==[] or self.pass_poteze >= 2 or self.stejbele+self.stejcrne == 64:
            if self.stejcrne > self.stejbele:
                return CRNI
            elif self.stejbele >self.stejcrne:
                return BELI
            else:
                return "Neodločeno"
        else:
            return None
    
    def vrednost(self):
        """Ocena za trenutno vrednost igre. Če je igre konec, mora biti ta ocena natančna,
           sicer je to nek približek."""
        if self.konec()!= None:
            if self.na_potezi == CRNI:
                return self.stejcrne - self.stejbele 
            else:
                return self.stejbele - self.stejcrne
            
        poteze_crnega = len(self.poteze(CRNI))
        poteze_belega = len(self.poteze(BELI))
        if self.poteze(CRNI) == ["pass"]:
            poteze_crnega = 0
        elif self.poteze(BELI) == ["pass"]:
            poteze_belega = 0
            
        if self.na_potezi == CRNI:
            return self.vrednost_crnih - self.vrednost_belih + poteze_crnega - poteze_belega
        else:
            return self.vrednost_belih - self.vrednost_crnih + poteze_belega - poteze_crnega
        

    def poteze(self, barva):
        """Vrni seznam moznih potez v trenutni poziciji."""
        sez_moznosti=[]
        for j in range(len(self.polje)):
            for i in range(len(self.polje[j])):
                if self.polje[i][j] == None:
                    for (i1,j1) in seznam_sosedov(i, j):
                        di = i1-i
                        dj = j1-j
                        if veljavna(barva, di, dj, self.polje, i, j) and (i,j) not in sez_moznosti:
                            sez_moznosti.append((i,j))
        if sez_moznosti ==[]:
            sez_moznosti =["pass"]
        return sez_moznosti

    def povleci(self, poteza, canvas = None, zetoni = None):
        """Povleci potezo poteza, predpostaviti smemo, da je veljavna."""
        # Preden potezo povlecemo, trenutno stanje spravimo
        polje = [self.polje[i][:] for i in range(8)] # KOPIJA polja
        self.prejsnja_stanja.append([self.na_potezi, self.stejcrne, self.stejbele, self.vrednost_crnih, self.vrednost_belih, polje, self.pass_poteze])
        # naredimo potezo
        if poteza == "pass":
            self.na_potezi = drugi(self.na_potezi)
            self.pass_poteze +=1
        else:
            (i,j) = poteza
            self.polje[i][j] = self.na_potezi
            self.pass_poteze = 0           
        
            # Popravimo stevec crnih in belih
            if self.na_potezi == CRNI:
                self.stejcrne += 1
                self.vrednost_crnih += HEVRISTIKA[i][j]
            else:
                self.stejbele += 1
                self.vrednost_belih += HEVRISTIKA[i][j]
            # ukleščeni žetoni spremenijo barvo
            self.preobrni(i, j, canvas, zetoni)
            # Zdaj je na potezi drugi (pozor, to ni nujno res v pravem Othellu)
            self.na_potezi = drugi(self.na_potezi)
            self.preskok()
        #print ("Trenutno stanje: {0}".format(self))

    def preobrni(self, i, j, canvas = None, zetoni = None):
        """Spremeni barve nasprotnikovih žetonov, ki smo jih ukleščili med svoja žetona"""
        barva = self.na_potezi
        seznam = seznam_sosedov(i, j)
        for (i1, j1) in seznam:
          if self.polje[i1][j1] == drugi(barva):
              di = i1-i
              dj = j1-j
              if veljavna(barva, di, dj, self.polje, i, j):
                  k = 1
                  while self.polje[i+k*di][j+k*dj] == drugi(barva):
                      self.polje[i+k*di][j+k*dj] = barva
                      if barva == BELI:
                          if canvas: canvas.itemconfig(zetoni[i+k*di][j+k*dj], fill="white")
                          self.stejcrne-=1
                          self.stejbele+=1
                          self.vrednost_belih += HEVRISTIKA[i+k*di][j+k*dj]
                          self.vrednost_crnih -= 1
                      else:
                          if canvas: canvas.itemconfig(zetoni[i+k*di][j+k*dj], fill="black")
                          self.stejcrne+=1
                          self.stejbele-=1
                          self.vrednost_crnih += HEVRISTIKA[i+k*di][j+k*dj]
                          self.vrednost_belih -= 1                          
                      k += 1

    def preklici(self, poteza):
        """Preklici zandjo potezo."""
        self.na_potezi, self.stejcrne, self.stejbele, self.vrednost_crnih, self.vrednost_belih, self.polje, self.pass_poteze = self.prejsnja_stanja.pop()

    def preskok(self):
        """Če igralec ne more storiti ničesar (nobena poteza ni veljavna), ga preskoči"""
        if self.slovar[self.na_potezi] == "človek":
            if self.poteze(self.na_potezi) == ["pass"]:                
                #print("zgodil se je preskok----------------------------------------------------------------------------------------------")
                self.na_potezi = drugi(self.na_potezi)            

class Othello:
    """Razred za glavno aplikacijo."""
    def __init__(self, master):

        master.title('Othello')

        #meni#
        menu = Menu(master)
        master.config(menu=menu)

        meni1 = Menu(menu)
        menu.add_cascade(label="Igra", menu=meni1)
        meni1.add_command(label="Črni=Človek, Beli=Človek", command=lambda: self.zacni_igro("človek", "človek"))
        meni1.add_command(label="Črni=Človek, Beli=Računalnik", command=lambda: self.zacni_igro("človek", "računalnik"))
        meni1.add_command(label="Črni=Računalnik, Beli=Človek", command=lambda: self.zacni_igro("računalnik", "človek"))
        meni1.add_command(label="Črni=Računalnik, Beli=Računalnik", command=lambda: self.zacni_igro("računalnik", "računalnik"))

        meni2 = Menu(menu)
        menu.add_cascade(label="Navodila", menu=meni2)
        meni2.add_command(label="Pravila igre", command=self.narisi_toplevel)

        meni3 = Menu(menu)
        menu.add_cascade(label="Izhod", menu=meni3)
        meni3.add_command(label="Izhod iz igre", command=self.zapri)
        ######

        self.igra = None # Igre ne igramo trenutno

        #napis, ki pove, kdo je na vrsti
        self.napis = StringVar(master, value="Začnimo.")
        Label(master, textvariable=self.napis,font=("Tahoma", 14)).grid(row=0, column=0,sticky=W)


        #napis, ki pove, koliko žetonov ima beli/črni
        self.napiscrni = StringVar(master, value="")
        self.napisbeli = StringVar(master, value="")
        Label(master, textvariable=self.napiscrni,font=("Tahoma", 14)).grid(row=3, column=0,sticky=W)
        Label(master, textvariable=self.napisbeli,font=("Tahoma", 14)).grid(row=3, column=1,sticky=E)

        self.canvas = Canvas(master, width=400, height=400, background="#97CAB1")
        self.canvas.grid(row=2, column=0, columnspan=2)
        self.canvas.bind('<Button-1>', self.klik)
        
        #seznam, ki vsebuje krogce(žetone) od tkinter
        self.zetoni = [[None for i in range(8)] for j in range(8)]

        #seznam, ki vsebuje pike, ki označujejo možne poteze
        self.pike = [[None for i in range(8)] for j in range(8)]

        self.mislec = None  
        self.mislec_poteza = None
        self.mislec_stop = False

        self.zacni_igro('človek', 'človek')

    def narisi_toplevel(self):
        toplevel = Toplevel(master, width=40, height=40, takefocus = True)
        toplevel.title("Pravila igre")
        toplevel.resizable(width=False, height=False)
        navodilo = ""
        for element in navodila:
            navodilo+=element
        izpis = Text(toplevel)
        izpis.insert(INSERT,navodilo)
        izpis.grid(row=0, column=0, columnspan=2, sticky = W)
        izpis.config(wrap=WORD)
        izpis.config(state=DISABLED)
            
    def zapri(self):
        """Zapre igro"""
        if self.mislec != None:
            self.mislec_stop = True
            self.mislec.join()
        self.canvas.master.destroy()

    def zacni_igro(self, crni, beli):
        # Ustvari novo igro
        self.igra = Igra()

        #nariše polje in nastavi igro na začetek
        self.igra.crni = crni
        self.igra.beli = beli
        self.igra.slovar = {CRNI:self.igra.crni, BELI:self.igra.beli}
        
        #Če racunalnik se vedno misli, mu povemo, naj neha in počakamo, da neha
        if self.mislec != None:
            self.mislec_stop = True
            self.mislec.join()

        #seznam, ki vsebuje krogce(žetone)
        self.zetoni = [[None for i in range(8)] for j in range(8)]

        #seznam, ki vsebuje pike, ki označujejo možne poteze
        self.pike = [[None for i in range(8)] for j in range(8)]

        #nastavi, da začne črni
        if self.igra.crni == "človek":
            self.napis.set("Na potezi je Črni.")
        else:
            self.napis.set("Črni razmišlja. Ne bodite nestrpni!")

        #nastavi napise za število črnih/belih žetonov
        self.napiscrni.set("Črni: "+str(self.igra.stejcrne))
        self.napisbeli.set("Beli: "+str(self.igra.stejbele))

        #nariše črte na kanvas
        self.canvas.delete(ALL)
        for i in range(8):
            self.canvas.create_line(i*50,0,i*50,400, fill="black", width=2)
            self.canvas.create_line(0,i*50,400,i*50, fill="black", width=2)
        
        #nariše začetne žetone
        self.canvas.create_oval(150+5, 150+5, 150+45, 150+45, fill="black")
        self.canvas.create_oval(200+5, 200+5, 200+45, 200+45, fill="black")
        self.canvas.create_oval(200+5, 150+5, 200+45, 150+45, fill="white")
        self.canvas.create_oval(150+5, 200+5, 150+45, 200+45, fill="white")
        #začetne žetone doda v self.zetoni
        self.zetoni[3][3]=self.canvas.create_oval(150+5, 150+5, 150+45, 150+45, fill="black")
        self.zetoni[4][4]=self.canvas.create_oval(200+5, 200+5, 200+45, 200+45, fill="black")
        self.zetoni[4][3]=self.canvas.create_oval(200+5, 150+5, 200+45, 150+45, fill="white")
        self.zetoni[3][4]=self.canvas.create_oval(150+5, 200+5, 150+45, 200+45, fill="white")

        self.pomoc()
        
        if self.igra.crni == 'računalnik':
            self.racunalnik_odigraj_potezo()
            
    def odigraj(self, poteza):
        """Če je polje prazno in poteza veljavna, se poteza odigra."""
        #print(self.igra.na_potezi, "povlekel potezo ", poteza)
        if poteza == "pass":
            self.igra.povleci(poteza, canvas=self.canvas, zetoni=self.zetoni)
            
            if self.igra.slovar[self.igra.na_potezi] == "človek":
                self.napis.set("Na potezi je " + self.igra.na_potezi)
            else:
                self.napis.set(self.igra.na_potezi + " razmišlja. Ne bodite nestrpni!")
                
            self.pomoc()
            
        else:
            i,j=poteza[0],poteza[1]
            je_veljavna = False
            for (dx, dy) in [(-1,0), (1,0), (0,-1), (0,1), (1,1), (1,-1), (-1,1), (-1,-1)]:
                je_veljavna = veljavna(self.igra.na_potezi, dx, dy, self.igra.polje, i, j)
                if je_veljavna: break

            if self.igra.polje[i][j] is None and je_veljavna:
                if self.igra.na_potezi == CRNI:
                    self.narisiCrnega(i,j)
                else:
                    self.narisiBelega(i,j)
                self.igra.povleci((i,j), canvas=self.canvas, zetoni=self.zetoni)
                
                if self.igra.slovar[self.igra.na_potezi] == "človek":
                    self.napis.set("Na potezi je " + self.igra.na_potezi)
                else:
                    self.napis.set(self.igra.na_potezi + " razmišlja. Ne bodite nestrpni!")

                self.napiscrni.set("Črni: "+str(self.igra.stejcrne))
                self.napisbeli.set("Beli: "+str(self.igra.stejbele))
                
                self.pomoc()
                
        r = self.igra.konec()
        if r == "Neodločeno":
            self.igra.na_potezi = None
            self.napis.set("Neodločeno")
        elif r is not None:
            self.napis.set('Zmagal je ' + r)
        else:
            # Preverimo, ali mora računalnik odigrati potezo
            if ((self.igra.na_potezi == CRNI and self.igra.crni == "računalnik") or
                (self.igra.na_potezi == BELI and self.igra.beli == "računalnik")):
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
        self.mislec_poteza = Alphabeta(self.igra, True, globina = 4).igraj()
        self.mislec = None # Pobrišemo objekt, ki predstavlja vlakno

    def mislec_preveri_konec(self):
        if self.mislec_poteza == None:
            # self.mislec ni končal, preverimo še enkrat čez 0.1 sekunde
            self.canvas.after(100, self.mislec_preveri_konec)
        else:
            # self.mislec je končal, povlečemo potezo
            poteza = self.mislec_poteza
            self.odigraj(poteza)

    def klik(self, event):
        """Ko klikneš, se odigra poteza"""
        if ((self.igra.na_potezi == CRNI and self.igra.crni == "človek") or
            (self.igra.na_potezi == BELI and self.igra.beli == "človek")):
            i = int(event.x / 50)
            j = int(event.y / 50)
            self.konec_pomoci()
            self.odigraj((i, j))

    def narisiCrnega(self, i, j):
        """Nariše črn žeton"""
        x = i * 50
        y = j * 50
        self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="black")
        self.zetoni[i][j] = self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="black")

    def narisiBelega(self, i, j):
        """Nariše bel žeton"""
        x = i * 50
        y = j * 50
        self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="white")
        self.zetoni[i][j] = self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="white")

    def pomoc(self):
        if (self.igra.na_potezi == CRNI and self.igra.crni == "človek") or (self.igra.na_potezi == BELI and self.igra.beli == "človek"):
            for poteza in self.igra.poteze(self.igra.na_potezi):
                if poteza == "pass":
                    pass
                else:
                    i,j=poteza[0],poteza[1]
                    pika = self.canvas.create_oval(i*50+20, j*50+20, i*50+25, j*50+25, fill="green")
                    self.pike[i][j] = pika
                
    def konec_pomoci(self):
        for podseznam in self.pike:
            for element in podseznam:
                if element != None :
                    self.canvas.delete(element)
        self.pike = [[None for i in range(8)] for j in range(8)]
                


master = Tk()
aplikacija = Othello(master)
master.resizable(width=FALSE, height=FALSE)
master.mainloop()


