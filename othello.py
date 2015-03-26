from tkinter import *
import threading

def drugi(igr):
    if igr == "Črni":
        return "Beli"
    else:
        return "Črni"

def veljavna(barva, di, dj, polje, i, j):
    """Če je poteza na polju (i,j) veljavna, vrne True, sicer vrne False"""
    k=1
    while polje[i+k*di][j+k*dj] == drugi(barva):
        if (i+k*di,di) == (7,1) or (i+k*di,di) == (0,-1) or (j+k*dj,dj) == (7,1) or (j+k*dj,dj) == (0,-1):
            return False
        k+=1
    if polje[i+k*di][j+k*dj] == barva and k>1:
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

def mozne_poteze(barva, polje):
    """Vrne seznam možnih potez, ki jih ima doloèen igralec na doloèenem polju"""
    sez_moznosti=[]
    for j,st in enumerate(polje):
            for i,vr in enumerate(st):
                if polje[i][j] != None:
                    pass
                else:
                    for el in seznam_sosedov(i, j):
                        i1 = el[0]
                        j1 = el[1]
                        di = i1-i
                        dj = j1-j
                        if veljavna(barva, di, dj, polje, i, j) and (i,j) not in sez_moznosti:
                            sez_moznosti.append((i,j))
                        else:
                            pass
    return sez_moznosti

def preobrni1(barva, polje, i, j):
    """Spremeni barve nasprotnikovih žetonov, ki smo jih uklešèili med svoja žetona"""
    seznam = seznam_sosedov(i, j)
    for el in seznam:
        i1 = el[0]
        j1 = el[1]
        if barva == polje[i1][j1] or polje[i1][j1] == None:
            pass
        else:
            di = i1-i
            dj = j1-j
            k=1
            if veljavna(barva, di, dj, polje, i, j):
                while polje[i+k*di][j+k*dj] == drugi(barva):
                    polje[i+k*di][j+k*dj] = barva
##                    if barva == "Beli":
##                        stejcrne-=1
##                        stejbele+=1
##                    else:
##                        stejcrne+=1
##                        stejbele-=1
                    k += 1
            else:
                pass
    return polje

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
        
        self.na_potezi = None #kdo je na potezi

        self.crni = 'človek' #kdo je èrni
        self.beli = 'človek' #kdo je beli

        self.mislec = None  #ne vem, kaj je to      
        self.mislec_poteza = None 
        self.mislec_stop = False

        #napis, ki pove, kdo je na vrsti
        self.napis = StringVar(master, value="Začnimo.")
        Label(master, textvariable=self.napis,font=("Tahoma", 14)).grid(row=0, column=0,sticky=W)

        #število crnih/belih ploščic, ki so na polju
        self.stejcrne = 2
        self.stejbele = 2

        #napis, ki pove, koliko žetonov ima beli/èrni
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
        """Zapre igro"""
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
            return "Črni"
        else:           
            if self.stejcrne + self.stejbele == 64:     
                if self.stejcrne > self.stejbele:
                    return "Črni"
                elif self.stejbele >self.stejcrne:
                    return "Beli"
                else:
                    return "Neodločeno"
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

        #nariše èrte na kanvas
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

        #nariše krogce
        self.canvas.create_oval(150+5, 150+5, 150+45, 150+45, fill="black")
        self.canvas.create_oval(200+5, 200+5, 200+45, 200+45, fill="black")
        self.canvas.create_oval(200+5, 150+5, 200+45, 150+45, fill="white")
        self.canvas.create_oval(150+5, 200+5, 150+45, 200+45, fill="white")
        #posodobi self.zetoni
        self.zetoni[3][3]=self.canvas.create_oval(150+5, 150+5, 150+45, 150+45, fill="black")
        self.zetoni[4][4]=self.canvas.create_oval(200+5, 200+5, 200+45, 200+45, fill="black")
        self.zetoni[4][3]=self.canvas.create_oval(200+5, 150+5, 200+45, 150+45, fill="white")
        self.zetoni[3][4]=self.canvas.create_oval(150+5, 200+5, 150+45, 200+45, fill="white")
        #posodobi self.polje
        self.polje[3][3] = "Črni"
        self.polje[4][4] = "Črni"
        self.polje[3][4] = "Beli"
        self.polje[4][3] = "Beli"

        
        if self.crni == 'računalnik':
            self.racunalnik_odigraj_potezo()

    def povleci(self, poteza):
        """Povleci dano potezo."""
        (i,j) = poteza
        self.polje[i][j] = self.na_potezi
        self.na_potezi = drugi(self.na_potezi)
        self.poteza += 1

    def preklici(self, poteza):
        """Prekliči dano potezo."""
        (i,j) = poteza
        self.polje[i][j] = None
        self.na_potezi = drugi(self.na_potezi)
        self.poteza -= 1

    def odigraj(self, i, j):
        #če je polje prazno in poteza veljavna, se poteza odigra

        #vsebuje True, èe obstaja veljavna poteza na tem polju
        seznam_veljavnosti=[veljavna(self.na_potezi,el[0]-i,el[1]-j,self.polje,i,j) for el in seznam_sosedov(i,j)
                            if self.na_potezi != self.polje[el[0]][el[1]] and self.polje[el[0]][el[1]] != None]
        #print(seznam_veljavnosti)
        
        
        if self.polje[i][j] is None and True in seznam_veljavnosti:
            self.polje[i][j] = self.na_potezi
            if self.na_potezi == "Črni":
                self.narisiCrnega(i,j)
            else:
                self.narisiBelega(i,j)
        
            self.preobrni(i,j)
            #print(self.polje)
            self.na_potezi = drugi(self.na_potezi)

            print(self.na_potezi)
            print(mozne_poteze(self.na_potezi, self.polje))
            self.preskok() #Ne dela.
            
            self.napis.set("Na potezi je " + self.na_potezi)
            self.napiscrni.set("Črni: "+str(self.stejcrne))
            self.napisbeli.set("Beli: "+str(self.stejbele))

            r = self.konec_igre()
            if r == "Neodločeno":
                self.na_potezi = None
                self.napis.set("Neodločeno")
            elif r is not None:
                self.napis.set('Zmagal je ' + r)
            else:
                # Preverimo, ali mora računalnik odigrati potezo
                if ((self.na_potezi == "Črni" and self.crni == "računalnik") or
                    (self.na_potezi == "Beli" and self.beli == "računalnik")):
                    # Namesto, da bi neposredno poklicali self.racunalnik_odigraj_potezo,
                    # to naredimo z zamikom, da se lahko prejšnja poteza sploh nariše.
                    self.canvas.after(100, self.racunalnik_odigraj_potezo)

    
    def racunalnik_odigraj_potezo(self): #kaj se tu dogaja?
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
        #(p, vrednost_p) = self.minimax(9)
        self.mislec_poteza = self.naslednja_poteza()
        self.mislec = None

    def mislec_preveri_konec(self):
        if self.mislec_poteza == None:
            # self.mislec ni končal, preverimo še enkrat čez 0.1 sekunde
            self.canvas.after(100, self.mislec_preveri_konec)
        else:
            # self.mislec je končal, povlečemo potezo
            (i,j) = self.mislec_poteza
            self.odigraj(i,j)

    def vrednost(self):
        '''Oceni vrednost pozicije za igralca. Ta ocena je hevristična (ni nujno pravilna).'''

        igralec = self.na_potezi
        nasprotnik = drugi(self.na_potezi)
        max_igralec = 0 # Največ, kar ima v tej poziciji igralec
        max_nasprotnik = 0 # Največ, kar ima v tej poziciji nasprotnik
        


##        
##            return max_igralec
##        else:
##            return -max_nasprotnik

    def naslednja_poteza(self):
        # pogleda vsak gib in izbere tistega, ki mu prinese najveè žetonov???
        #to ne dela
        najboljsa_poteza = None
        najboljsa_vrednost = -1
        for poteza in mozne_poteze(self.na_potezi, self.polje):
            stanje = self.polje
            x,y = poteza
            print(poteza)
            stanje = preobrni1(self.na_potezi, self.polje, x, y)
            print(stanje)
            k = 0
            for st in stanje:
                for zeton in st:
                    print(zeton)
                    if zeton == self.na_potezi:
                        k = k + 1
            print(k)
            if k > najboljsa_vrednost:
                najboljsa_vrednost = k
                najboljsa_poteza = poteza
                print("*",najboljsa_poteza)
        return najboljsa_poteza 

##    if max_igr >= max_nas:
##        return max_igr
##    else:
##        return -max_nas

##    def minimax(self,globina):
##        # Preverimo, ali je treba končati z razmišljanjem
##        if self.mislec_stop: return (None, 0)
##        if globina == 0 or self.konec_igre() != None:
##            # Dosegli smo globino 0 ali pa je konec igre, vrnemo oceno za vrednost
##            return (None, self.vrednost())
##        else:
##            # Za vsako možno potezo ocenimo, koliko je vredna.
##            # Izberemo najboljšo potezo.
##            p = None # Najboljša do sedaj videna poteza
##            vrednost_p = -4   # Manj kot najmanjša možna vrednost pozicije
##            for i in range(8):
##                for j in range(8):
##                    if self.polje[i][j] == None:
##                        # Polje (i,j) ni zasedeno, lahko igramo
##                        # Naredimo potezo (i,j) in ocenimo rekurzivno
##                        self.polje[i][j] = self.na_potezi
##                        self.na_potezi = drugi_igralec(self.na_potezi)
##                        (q, vrednost_q) = self.minimax(globina-1)
##                        # Izničimo potezo (i,j)
##                        self.polje[i][j] = None
##                        self.na_potezi = drugi_igralec(self.na_potezi)
##                        vrednost_q = -vrednost_q
##                        if vrednost_q > vrednost_p:
##                            # Ta poteza je boljša od poteze p
##                            p = (i,j)
##                            vrednost_p = vrednost_q
##            return (p, vrednost_p)


    def klik(self, event):
        """ko klikneš, se odigra poteza"""
        if ((self.na_potezi == "Črni" and self.crni == "človek") or
            (self.na_potezi == "Beli" and self.beli == "človek")):
            i = int(event.x / 50)
            j = int(event.y / 50)
            self.odigraj(i, j)
                
    def narisiCrnega(self, i, j):
        """Nariše črn žeton"""
        x = i * 50
        y = j * 50
        self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="black")
        self.stejcrne+=1
        self.zetoni[i][j] = self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="black")
        self.polje[i][j] = "Črni"

    def narisiBelega(self, i, j):
        """Nariše bel žeton"""
        x = i * 50
        y = j * 50
        self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="white")
        self.stejbele+=1
        self.zetoni[i][j] = self.canvas.create_oval(x+5, y+5, x+45, y+45, fill="white")
        self.polje[i][j] = "Beli"


    def preobrni(self, i, j):
        """Spremeni barve nasprotnikovih žetonov, ki smo jih uklešèili med svoja žetona"""
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
        """Èe igralec ne more storiti nièesar, ga preskoèi"""
        if mozne_poteze(self.na_potezi, self.polje) == []:
            print("ni ok")
            self.na_potezi = drugi(self.na_potezi)

                    
master = Tk()
aplikacija = Othello(master)
master.resizable(width=FALSE, height=FALSE) 
master.mainloop()       

        
