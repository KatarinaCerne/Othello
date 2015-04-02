POS_INFINITY = 100000000000
NEG_INFINITY = -POS_INFINITY

import random

BELI = "Beli"
CRNI = "Črni"

def drugi(igr):
    if igr == CRNI:
        return BELI
    else:
        return CRNI

class Alphabeta():

    def __init__(self, igra, igralec, globina = 5):
        self.igra = igra 
        self.igralec = igralec # Ali je to igralec ali nasprotnik
        self.globina = globina

    def igraj(self):
        self.pozicije = 0 # Štejemo, koliko pozicij smo pregledali
        (p, vrednost_p) = self.alphabeta(self.globina, NEG_INFINITY, POS_INFINITY, self.igralec)
        #print ("\nAlphabeta: globina {0}, stevilo pozicij {1}, vrednost igre {2}\n".format(self.globina, self.pozicije, vrednost_p))
        return p

    def alphabeta(self, globina, alpha, beta, igralec):
        self.pozicije += 1 # Povečaj število pregledanih pozicij
        if globina == 0 or self.igra.konec()!=None:
            # Dosegli smo globino 0 ali pa je konec igre, vrnemo oceno za vrednost
            vrednost = self.igra.vrednost()
            if not igralec: vrednost = -vrednost
            return (None, vrednost)
        else:
            if igralec:
              # Na potezi je igralec, vrednost igre maksimiziramo
                p = None                  # Najboljša do sedaj videna poteza
                vrednost_p = NEG_INFINITY # Vrednost do sedaj najboljše videne poteze
                mozne_poteze_igralca = self.igra.poteze(self.igra.na_potezi)
                random.shuffle(mozne_poteze_igralca)
                for poteza in mozne_poteze_igralca:
                    self.igra.povleci(poteza)
                    (q, vrednost_q) = self.alphabeta(globina-1, alpha, beta, False)
                    self.igra.preklici(poteza)
                    if vrednost_q > vrednost_p:
                        p = poteza
                        vrednost_p = vrednost_q
                    alpha = max (alpha, vrednost_p)
                    if beta <= alpha:
                        # Ne splača se gledati naprej, ker bo samo še slabše
                        # kot pa to, kar si lahko garantiramo zdaj
                        return (p, vrednost_p)
                return (p, vrednost_p) # vrnemo najboljšo najdeno potezo
            else:
              # Na potezi je nasprotnik, vrednost igre minimiziramo
                p = None                  # Najboljša do sedaj videna poteza
                vrednost_p = POS_INFINITY # Vrednost do sedaj najboljše videne poteze
                mozne_poteze_nasprotnika = self.igra.poteze(self.igra.na_potezi)
                
                for poteza in mozne_poteze_nasprotnika:
                    self.igra.povleci(poteza)
                    (q, vrednost_q) = self.alphabeta(globina-1, alpha, beta, True)
                    self.igra.preklici(poteza)
                    if vrednost_q < vrednost_p:
                        p = poteza
                        vrednost_p = vrednost_q
                    beta = min (beta, vrednost_p)
                    if beta <= alpha:
                        return (p, vrednost_p)
                return (p, vrednost_p) # vrnemo najboljšo najdeno potezo
