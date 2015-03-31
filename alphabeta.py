import random

POS_INFINITY = 100000000000
NEG_INFINITY = -POS_INFINITY

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
        self.igralec = igralec # Ali je to igralec ali nasprotnik?
        self.globina = globina


    def igraj(self):
        self.pozicije = 0 # Štejemo, koliko pozicij smo pregledali
        (p, vrednost_p) = self.alphabeta(self.globina, NEG_INFINITY, POS_INFINITY, self.igralec)
        # Izpišemo statistike
        print ("\nAlphabeta: globina {0}, stevilo pozicij {1}, vrednost igre {2}\n".format(self.globina, self.pozicije, vrednost_p))
        return p

    def alphabeta(self, globina, alpha, beta, igralec):
        self.pozicije += 1 # Povečaj število pregledanih pozicij
        if globina == 0 or self.igra.konec() != None:
            # Dosegli smo globino 0 ali pa je konec igre, vrnemo oceno za vrednost
            vrednost = self.igra.vrednost()
            if not igralec:
                vrednost = -vrednost
            print(self.igra.poteze(self.igra.na_potezi))
            return (None, vrednost)
        else:
            if igralec:
                # Na potezi je igralec, vrednost igre maksimiziramo
                p = None                  # Najboljša do sedaj videna poteza
                vrednost_p = NEG_INFINITY # Vrednost do sedaj najboljše videne poteze
                mozne_poteze = self.igra.poteze(self.igra.na_potezi)
                #print(self.igra.poteze(self.igra.na_potezi))
                if mozne_poteze == []:
                    self.igra.na_potezi = drugi(self.igra.na_potezi)
                    (q, vrednost_q) = self.alphabeta(globina-1, alpha, beta, False)
                print("------------if-----------")
                print(mozne_poteze, self.igra.na_potezi)
                random.shuffle(mozne_poteze)
                for poteza in mozne_poteze:
                    self.igra.povleci(poteza)
                    print("igram", poteza)
                    (q, vrednost_q) = self.alphabeta(globina-1, alpha, beta, False)#tale False. poglej ga. ni kul. kaj če nima potez?
                    print(vrednost_q)                                                       #info: če nima poteze, je vrednost -1000000000 oz 100000000
                    self.igra.preklici(poteza)
                    if vrednost_q > vrednost_p:
                        p = poteza
                        vrednost_p = vrednost_q
                    alpha = max (alpha, vrednost_p)
                    if beta <= alpha:
                        # Ne splaca se gledati naprej, ker bo samo se slabse
                        # kot pa to, kar is lahko garantiramo zdaj
                        return (p, vrednost_p)
                return (p, vrednost_p) # vrnemo najboljšo najdeno potezo
            else:
                # Na potezi je nasprotnik, vrednost igre minimiziramo
                p = None                  # Najboljša do sedaj videna poteza
                vrednost_p = POS_INFINITY # Vrednost do sedaj najboljše videne poteze
                mozne_poteze = self.igra.poteze(self.igra.na_potezi)
                if mozne_poteze == []:
                    self.igra.na_potezi = drugi(self.igra.na_potezi)
                    (q, vrednost_q) = self.alphabeta(globina-1, alpha, beta, True)
                print("------------else-----------")
                print(mozne_poteze, self.igra.na_potezi)
                for poteza in self.igra.poteze(self.igra.na_potezi):
                    self.igra.povleci(poteza)
                    (q, vrednost_q) = self.alphabeta(globina-1, alpha, beta, True)#tale True. poglej ga.
                    self.igra.preklici(poteza)
                if vrednost_q < vrednost_p:
                    p = poteza
                    vrednost_p = vrednost_q
                beta = min (beta, vrednost_p)
                if beta <= alpha:
                    return (p, vrednost_p)
            return (p, vrednost_p) # vrnemo najboljšo najdeno potezo
